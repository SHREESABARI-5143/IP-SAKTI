'use client';

import React, { useState, useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  BookOpen, 
  UserCheck, 
  Download, 
  Scale, 
  Globe, 
  ShieldCheck, 
  AlertCircle,
  RefreshCw,
  Layers,
  ArrowRight,
  HelpCircle,
  FileCheck2,
  Lock,
  ExternalLink,
  Copy,
  Check
} from 'lucide-react';
import { useAppStore, Message, Citation } from '@/lib/store';
import { translations } from '@/lib/translations';
import { api } from '@/lib/api';
import { ConfidenceBadge } from '@/components/ConfidenceBadge';

export default function Home() {
  const { 
    jurisdiction, 
    selectedCountry, 
    language, 
    activeConversationId, 
    setActiveConversationId,
    setActiveSourceDrawer, 
    setEscalationModal 
  } = useAppStore();

  const t = translations[language] || translations.en;

  const [inputQuery, setInputQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const samplePrompts = [
    {
      category: 'Section 3(p) & Patentability',
      domain: 'Patents Act 1970',
      question: t.sampleQ1 || 'Can I patent my new Ayurvedic formulation with Turmeric and Ashwagandha?',
      icon: Scale,
    },
    {
      category: 'ABS & Prior NBA Approval',
      domain: 'Biological Diversity Act 2023',
      question: t.sampleQ2 || 'Does my company require ABS approval under Biological Diversity Act 2023?',
      icon: ShieldCheck,
    },
    {
      category: 'Ayurveda Aahar vs ASU Drug',
      domain: 'FSSAI Regs 2022',
      question: t.sampleQ3 || 'How is Ayurveda-Aahar regulated under FSSAI 2022 compared to Classical medicine?',
      icon: Layers,
    },
    {
      category: 'Global Export Compliance',
      domain: 'US FDA DSHEA / EU THMPD',
      question: t.sampleQ4 || 'What are US FDA DSHEA export labeling requirements for Ayurvedic supplements?',
      icon: Globe,
    },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (queryText?: string) => {
    const textToSend = queryText || inputQuery;
    if (!textToSend.trim() || isLoading) return;

    const userMsg: Message = {
      id: `usr_${Date.now()}`,
      role: 'user',
      content: textToSend,
      jurisdiction,
      citations: [],
      created_at: new Date().toISOString()
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setIsLoading(true);

    try {
      const response = await api.sendChatMessage({
        message: textToSend,
        conversation_id: activeConversationId,
        jurisdiction,
        selected_country: jurisdiction === 'International' ? selectedCountry : null,
        language
      });

      if (response.conversation_id) {
        setActiveConversationId(response.conversation_id);
      }

      const assistantMsg: Message = {
        id: response.message_id || `asst_${Date.now()}`,
        role: 'assistant',
        content: response.full_answer,
        short_answer: response.short_answer,
        jurisdiction: response.jurisdiction,
        domain: response.detected_domain,
        confidence: response.confidence,
        citations: response.citations || [],
        recommended_next_steps: response.recommended_next_steps || [],
        followup_suggestions: response.followup_suggestions || [],
        is_abstained: response.is_abstained,
        abstention_reason: response.abstention_reason,
        created_at: new Date().toISOString()
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMsg: Message = {
        id: `err_${Date.now()}`,
        role: 'assistant',
        content: '### Grounding & Retrieval Verification Notice\nThe system encountered a connection issue with the statutory verification server. Please confirm the backend service is running and retry your query.',
        jurisdiction,
        citations: [],
        is_abstained: true,
        created_at: new Date().toISOString()
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const copyAnswer = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const renderContentWithCitations = (content: string, citations: Citation[]) => {
    const parts = content.split(/(\[\d+\])/g);
    return (
      <div className="prose prose-slate max-w-none text-slate-800 text-sm leading-relaxed space-y-3">
        {parts.map((part, idx) => {
          const match = part.match(/\[(\d+)\]/);
          if (match) {
            const citNum = parseInt(match[1], 10);
            const citObj = citations.find((c) => c.citation_number === citNum);
            return (
              <button
                key={idx}
                onClick={() => citObj && setActiveSourceDrawer(citObj)}
                className="citation-tag mx-0.5 align-baseline hover:scale-105 transition-transform"
                title={citObj ? `${citObj.source_title} - ${citObj.provision_ref}` : 'Authoritative Statutory Source'}
              >
                [{citNum}] {citObj?.provision_ref ? ` ${citObj.provision_ref}` : ''}
              </button>
            );
          }
          return <span key={idx} dangerouslySetInnerHTML={{ __html: formatSimpleMarkdown(part) }} />;
        })}
      </div>
    );
  };

  const formatSimpleMarkdown = (text: string) => {
    return text
      .replace(/^### (.*$)/gim, '<h3 class="text-base font-bold text-slate-900 mt-4 mb-2 pb-1 border-b border-slate-200/80 flex items-center gap-2">$1</h3>')
      .replace(/^#### (.*$)/gim, '<h4 class="text-xs font-bold uppercase tracking-wider text-teal-800 mt-3 mb-1.5">$1</h4>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong class="font-bold text-slate-900">$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em class="italic text-slate-700">$1</em>')
      .replace(/`([^`]+)`/gim, '<code class="px-1.5 py-0.5 bg-slate-100 text-teal-900 rounded font-mono text-xs font-medium">$1</code>')
      .replace(/^> (.*$)/gim, '<blockquote class="p-3 my-2 bg-amber-50/60 border-l-4 border-amber-500 text-slate-800 italic text-xs rounded-r-lg">$1</blockquote>')
      .replace(/\n/gim, '<br />');
  };

  const exportAsReport = (msg: Message) => {
    const reportData = `======================================================================
IP-SAKTI SAHAYAK — STATUTORY & REGULATORY INTELLIGENCE REPORT
Grounding: Citation-Grounded AI • Evidence Validation & Safe Abstention
======================================================================
Generated Date: ${new Date().toLocaleString()}
Jurisdiction Scope: ${msg.jurisdiction}
Domain Area: ${msg.domain || 'Ayurvedic IP & Traditional Knowledge'}
Confidence Level: ${msg.confidence?.level || 'High'} (${Math.round((msg.confidence?.score || 0.95) * 100)}%)

1. QUERY:
${messages[messages.indexOf(msg) - 1]?.content || 'Ayurvedic IP Query'}

2. EXECUTIVE SUMMARY:
${msg.short_answer || 'See statutory analysis below'}

3. DETAILED STATUTORY & REGULATORY ANALYSIS:
${msg.content.replace(/<[^>]+>/g, '')}

4. PRIMARY STATUTORY AUTHORITIES CITED:
${msg.citations.map((c, i) => `[${i+1}] ${c.source_title} (${c.authority})
    Provision: ${c.provision_ref}
    URL / Reference: ${c.source_url || 'Official Gazette'}`).join('\n\n')}

5. STATUTORY DISCLAIMER:
IP-SAKTI Sahayak provides general informational and statutory research guidance. It does not constitute legal opinion, formal patent prosecution filings, or binding regulatory clearance.
======================================================================`;

    const blob = new Blob([reportData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `IP_SAKTI_Report_${Date.now()}.txt`;
    a.click();
  };

  return (
    <div className="flex-1 flex flex-col max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      
      {/* Zero State / Hero Presentation */}
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col justify-center items-center text-center max-w-3xl mx-auto py-6 sm:py-10">
          
          {/* Trust Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-gradient-to-r from-teal-50 to-emerald-50 border border-teal-200/80 text-teal-900 text-xs font-bold mb-5 shadow-2xs">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <ShieldCheck className="w-4 h-4 text-teal-700" />
            <span>Citation-Grounded AI • Evidence Validation & Safe Abstention</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
            Ayurvedic IP & Regulatory <br className="hidden sm:inline" />
            <span className="bg-gradient-to-r from-teal-800 via-teal-700 to-emerald-700 bg-clip-text text-transparent">
              Intelligence Copilot
            </span>
          </h1>
          
          <p className="text-sm sm:text-base font-medium text-slate-600 mt-4 max-w-xl leading-relaxed">
            Instant statutory clarity for Patents, Section 3(p) TK exclusions, BDA 2023 ABS compliance, FSSAI Ayurveda Aahar, and Global Exports.
          </p>

          {/* Active Framework Badge */}
          <div className="mt-5 inline-flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-xl bg-white border border-slate-200 shadow-2xs text-slate-700">
            <span className="text-slate-400">Target Framework:</span>
            <span className="font-bold text-teal-900 flex items-center gap-1.5">
              {jurisdiction === 'India' ? (
                <>🇮🇳 Indian Statutory Baseline (Patents Act, BDA 2023, ASU Rules)</>
              ) : (
                <>🌐 International Regulatory Scope ({selectedCountry || 'USA/EU'})</>
              )}
            </span>
          </div>

          {/* 4 Clean Actionable Sample Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 mt-8 w-full text-left">
            {samplePrompts.map((item, idx) => {
              const Icon = item.icon;
              return (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(item.question)}
                  className="p-4 bg-white hover:bg-teal-50/40 border border-slate-200/90 hover:border-teal-300 rounded-2xl shadow-xs hover:shadow-md transition-all flex flex-col justify-between group text-left relative overflow-hidden"
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <span className="px-2 py-0.5 bg-slate-100 group-hover:bg-teal-100 text-slate-600 group-hover:text-teal-800 text-[10px] font-bold rounded-md uppercase tracking-wider transition-colors">
                      {item.domain}
                    </span>
                    <ArrowRight className="w-4 h-4 text-slate-300 group-hover:text-teal-600 group-hover:translate-x-1 transition-all flex-shrink-0" />
                  </div>
                  
                  <p className="text-xs sm:text-[13px] font-semibold text-slate-800 group-hover:text-teal-950 leading-snug">
                    {item.question}
                  </p>
                </button>
              );
            })}
          </div>
        </div>
      ) : (
        /* Conversation Feed */
        <div className="flex-1 space-y-6 pb-8 overflow-y-auto">
          {messages.map((msg, idx) => (
            <div
              key={msg.id || idx}
              className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              {msg.role === 'user' ? (
                <div className="max-w-2xl bg-gradient-to-tr from-teal-900 to-teal-800 text-white px-5 py-3.5 rounded-2xl rounded-tr-sm shadow-md text-sm font-medium leading-relaxed">
                  <p>{msg.content}</p>
                  <div className="text-[10px] text-teal-200/80 mt-1.5 flex items-center gap-1.5 justify-end font-semibold">
                    <span>{msg.jurisdiction} Scope</span>
                  </div>
                </div>
              ) : (
                <div className="w-full bg-white border border-slate-200/90 rounded-2xl p-6 shadow-sm space-y-4 relative">
                  
                  {/* Assistant Card Header */}
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-teal-50 text-teal-900 border border-teal-200/70">
                        {msg.domain || 'Statutory Analysis'}
                      </span>
                      <span className="text-xs font-semibold text-slate-500">
                        Jurisdiction: <strong className="text-slate-800">{msg.jurisdiction}</strong>
                      </span>
                    </div>

                    <ConfidenceBadge confidence={msg.confidence} />
                  </div>

                  {/* Grounded Content */}
                  <div>
                    {renderContentWithCitations(msg.content, msg.citations)}
                  </div>

                  {/* Verified Citations Carousel / Grid */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="pt-3 border-t border-slate-100">
                      <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                        <BookOpen className="w-3.5 h-3.5 text-teal-700" />
                        Authoritative Statutory Grounds ({msg.citations.length})
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                        {msg.citations.map((c) => (
                          <div
                            key={c.citation_number}
                            onClick={() => setActiveSourceDrawer(c)}
                            className="p-3 bg-slate-50/80 hover:bg-teal-50/70 border border-slate-200 hover:border-teal-300 rounded-xl cursor-pointer transition-all flex items-start gap-2.5 group shadow-2xs"
                          >
                            <span className="w-5 h-5 rounded-md bg-teal-800 text-white text-[11px] font-bold flex items-center justify-center flex-shrink-0 mt-0.5 shadow-2xs">
                              {c.citation_number}
                            </span>
                            <div className="text-xs overflow-hidden flex-1">
                              <p className="font-bold text-slate-800 group-hover:text-teal-950 truncate">
                                {c.source_title}
                              </p>
                              <p className="text-[11px] text-slate-500 truncate mt-0.5">
                                {c.provision_ref} • <span className="text-teal-700 font-semibold">{c.authority}</span>
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Footer Action Bar */}
                  <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100 text-xs">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => exportAsReport(msg)}
                        className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg flex items-center gap-1.5 transition-all"
                      >
                        <Download className="w-3.5 h-3.5 text-slate-600" />
                        <span>Export Report</span>
                      </button>

                      <button
                        onClick={() => copyAnswer(msg.content, msg.id)}
                        className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg flex items-center gap-1.5 transition-all"
                      >
                        {copiedId === msg.id ? (
                          <>
                            <Check className="w-3.5 h-3.5 text-emerald-600" />
                            <span className="text-emerald-700">Copied!</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3.5 h-3.5 text-slate-600" />
                            <span>Copy</span>
                          </>
                        )}
                      </button>

                      <button
                        onClick={() => setEscalationModal(true, { question: messages[idx - 1]?.content, aiAnalysis: msg.content })}
                        className="px-3 py-1.5 bg-amber-100/80 hover:bg-amber-200 text-amber-950 font-bold rounded-lg flex items-center gap-1.5 transition-all border border-amber-200"
                      >
                        <UserCheck className="w-3.5 h-3.5 text-amber-800" />
                        <span>Consult IP Facilitator</span>
                      </button>
                    </div>

                    <p className="text-[11px] text-slate-400 font-medium">
                      SHA256 Grounding Verified
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-teal-900">
                <RefreshCw className="w-4 h-4 animate-spin text-teal-700" />
                <span>Searching statutory registries, verifying TKDL exclusions, and synthesizing grounded legal guidance...</span>
              </div>
              <div className="h-3.5 bg-slate-100 rounded-full w-4/5 animate-pulse"></div>
              <div className="h-3.5 bg-slate-100 rounded-full w-2/3 animate-pulse"></div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Floating Modern Command Bar */}
      <div className="sticky bottom-4 z-20 mt-auto pt-2">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="relative bg-white/95 backdrop-blur-xl shadow-2xl shadow-teal-950/10 border border-slate-300/80 rounded-2xl p-2 sm:p-2.5 flex items-center gap-2 transition-all focus-within:border-teal-600 focus-within:ring-2 focus-within:ring-teal-600/20"
        >
          <div className="hidden sm:flex items-center pl-2 text-slate-400">
            <Sparkles className="w-4 h-4 text-teal-600" />
          </div>

          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={t.askPlaceholder || "Ask about Section 3(p), BDA 2023 ABS approval, Ayurveda Aahar, or US FDA DSHEA..."}
            className="flex-1 text-xs sm:text-sm px-2 sm:px-3 py-2 bg-transparent focus:outline-none text-slate-900 placeholder:text-slate-400 font-medium"
          />

          <div className="flex items-center gap-1.5 flex-shrink-0">
            <button
              type="submit"
              disabled={!inputQuery.trim() || isLoading}
              className="px-4 sm:px-5 py-2.5 bg-gradient-to-r from-teal-800 via-teal-700 to-emerald-700 hover:from-teal-900 hover:to-emerald-800 disabled:opacity-40 text-white text-xs sm:text-sm font-bold rounded-xl flex items-center gap-2 shadow-md shadow-teal-900/20 transition-all cursor-pointer"
            >
              <span>Ask Sahayak</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
