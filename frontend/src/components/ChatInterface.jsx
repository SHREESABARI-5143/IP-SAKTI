"use client";

import React, { useState, useRef, useEffect } from "react";
import { sendQuery } from "@/lib/api";
import {
  Send,
  BookOpen,
  Copy,
  Check,
  ShieldAlert,
  Leaf,
  MessageSquare,
} from "lucide-react";
import { SourcesPanel } from "./SourcesPanel";
import { useApp } from "@/context/AppContext";

const GREETINGS = {
  en: "Welcome! I am IP-SAKTI Sahayak, your source-cited, jurisdiction-aware AI assistant for Ayurveda IP law and regulatory guidance. How can I assist you today?",
  hi: "नमस्ते! मैं IP-SAKTI सहायक हूँ। मैं आयुर्वेद, आईपी कानून (पेटेंट, जीआई, ट्रेडमार्क, जैव विविधता) तथा आयुष नियमों के लिए आपका स्रोत-सत्यापित एआई सहायक हूँ। आप अपना प्रश्न पूछ सकते हैं।",
  sa: "नमस्ते! अहम् IP-SAKTI सहायकः अस्मि। आयुर्वेदशास्त्रे, बौद्धिक-सम्पत्ति-विधौ (Patents, TK, GI, Biodiversity) च भवतः साहाय्यार्थं सज्जोऽस्मि। स्वप्रश्नं पृच्छतु।",
  ta: "வணக்கம்! நான் IP-SAKTI சகாயக். ஆயுர்வேத ஐபி சட்டங்கள், காப்புரிமை மற்றும் ஆயுஷ் ஒழுங்குமுறை விதிகளுக்கான உங்கள் நம்பகமான சட்ட வழிகாட்டி. உங்கள் கேள்வியைக் கேளுங்கள்.",
  te: "నమస్కారం! నేను IP-SAKTI సహాయక్. ఆయుర్వేద మేధో సంపత్తి చట్టాలు, పేటెంట్లు మరియు ఆయుష్ నియంత్రణలపై మీ విశ్వసనీయ సహాయకుడిని. మీ ప్రశ్నను అడగండి.",
  mr: "नमस्कार! मी IP-SAKTI सहाय्यक आहे. आयुर्वेद, आयपी कायदे (पेटंट, जीआय, जैवविविधता) आणि आयुष नियमांसाठी आपला स्रोत-सत्यापित सहाय्यक. आपला प्रश्न विचारा.",
  bn: "নমস্কার! আমি IP-SAKTI সহায়ক। আয়ুর্বেদ আইপি আইন, পেটেন্ট এবং আয়ুশ বিধিমালার জন্য আপনার যাচাইকৃত সহকারী। আপনার প্রশ্ন জিজ্ঞাসা করুন।",
};

export const ChatInterface = ({
  jurisdiction,
  language,
}) => {
  const { addChatHistory } = useApp();
  const [messages, setMessages] = useState([
    {
      id: "init",
      sender: "bot",
      text: GREETINGS[language] || GREETINGS.en,
      sources: [],
    },
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedSources, setSelectedSources] = useState([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputQuery.trim() || loading) return;

    const userText = inputQuery.trim();
    const userMsgId = `usr_${Date.now()}`;
    const botMsgId = `bot_${Date.now()}`;

    setMessages((prev) => [
      ...prev,
      { id: userMsgId, sender: "user", text: userText },
    ]);
    setInputQuery("");
    setLoading(true);

    try {
      const res = await sendQuery(userText, jurisdiction, language);
      setMessages((prev) => [
        ...prev,
        {
          id: botMsgId,
          sender: "bot",
          text: res.answer,
          confidence: res.confidence,
          sources: res.sources || [],
          disclaimer: res.disclaimer,
        },
      ]);
      if (addChatHistory) {
        addChatHistory({
          query: userText,
          jurisdiction,
          confidence: res.confidence,
          answerPreview: res.answer?.slice(0, 90),
        });
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: botMsgId,
          sender: "bot",
          text:
            language === "hi"
              ? "क्षमा करें, आधिकारिक स्रोतों को प्राप्त करते समय त्रुटि हुई। कृपया पुनः प्रयास करें।"
              : "Apologies, an error occurred while retrieving official legal sources. Please try again.",
          confidence: "LOW",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDrawer = (sources) => {
    setSelectedSources(sources);
    setIsDrawerOpen(true);
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4.25rem)] w-full max-w-7xl 2xl:max-w-[1500px] mx-auto px-3 sm:px-6 lg:px-8 py-3 sm:py-5">
      {/* Header bar */}
      <div className="flex items-center justify-between gap-3 mb-3 px-1">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-800 shadow-xs">
            <MessageSquare className="w-5 h-5 text-emerald-700" />
          </div>
          <div>
            <h1 className="t-card-heading text-slate-900 font-bold">AI Legal Assistant</h1>
            <p className="t-small text-slate-500 hidden sm:block">
              Citation-grounded retrieval • Live official government links (India Code, IP India, WIPO Lex)
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 shadow-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            {jurisdiction?.toUpperCase()} JURISDICTION
          </span>
        </div>
      </div>

      {/* Messages scroll area */}
      <div className="flex-1 overflow-y-auto space-y-5 pr-1.5 pb-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} animate-in fade-in duration-200`}
          >
            <div
              className={`rounded-2xl p-4 sm:p-6 space-y-3.5 transition-all ${
                msg.sender === "user"
                  ? "max-w-xl md:max-w-2xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md rounded-br-none"
                  : "w-full max-w-4xl lg:max-w-5xl 2xl:max-w-6xl bg-white border border-emerald-100 text-slate-800 rounded-bl-none shadow-sm hover:shadow-md"
              }`}
            >
              {/* Bot header */}
              {msg.sender === "bot" && (
                <div className="flex items-center justify-between border-b border-emerald-50 pb-2.5 mb-2">
                  <div className="flex items-center gap-2">
                    <Leaf className="w-4 h-4 text-emerald-600" />
                    <span className="t-label text-slate-800 font-bold">IP-SAKTI Sahayak</span>
                  </div>

                  {msg.confidence && (
                    <span
                      className={`t-label px-2.5 py-0.5 rounded-full border text-xs font-semibold ${
                        msg.confidence === "HIGH"
                          ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                          : msg.confidence === "MEDIUM"
                          ? "bg-amber-50 text-amber-700 border-amber-200"
                          : "bg-red-50 text-red-700 border-red-200"
                      }`}
                    >
                      {msg.confidence} CONFIDENCE
                    </span>
                  )}
                </div>
              )}

              {/* Message body */}
              <div className={`t-body leading-relaxed whitespace-pre-line text-sm sm:text-base ${msg.sender === "user" ? "text-white" : "text-slate-800"}`}>
                {msg.text}
              </div>

              {/* Prominent Live Official Citation Links attached directly to response */}
              {msg.sender === "bot" && msg.sources && msg.sources.length > 0 && (
                <div className="pt-3 border-t border-emerald-50 space-y-2">
                  <div className="text-xs font-bold text-slate-700 flex items-center gap-1.5 uppercase tracking-wider">
                    <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Grounded Official Citations &amp; Real Act Links ({msg.sources.length}):</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
                    {msg.sources.map((src, sIdx) => (
                      <div
                        key={sIdx}
                        className="p-3 rounded-xl bg-slate-50/80 hover:bg-emerald-50/50 border border-slate-200 hover:border-emerald-300 transition flex flex-col justify-between space-y-2"
                      >
                        <div>
                          <div className="text-xs font-bold text-slate-900 line-clamp-1">{src.doc_title}</div>
                          <div className="text-[11px] font-semibold text-emerald-700 line-clamp-1">{src.section_title}</div>
                          {src.effective_date && (
                            <div className="text-[10px] text-slate-500 mt-0.5">📅 {src.effective_date}</div>
                          )}
                        </div>

                        <div className="flex items-center justify-between pt-1 border-t border-slate-100">
                          <span className="text-[10px] font-mono text-slate-500">
                            Match {Math.round((src.relevance_score || 0) * 100)}%
                          </span>
                          {src.url ? (
                            <a
                              href={src.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 hover:text-emerald-900 bg-white hover:bg-emerald-100 px-2 py-0.5 rounded border border-emerald-200 shadow-2xs transition"
                            >
                              Official Portal ↗
                            </a>
                          ) : (
                            <span className="text-[10px] text-slate-400 font-mono">{src.section_id}</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Disclaimer */}
              {msg.disclaimer && (
                <div className="flex items-start gap-2 text-xs text-amber-700 bg-amber-50 p-3 rounded-xl border border-amber-200">
                  <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5 text-amber-600" />
                  <span>{msg.disclaimer}</span>
                </div>
              )}

              {/* Bot actions */}
              {msg.sender === "bot" && (
                <div className="flex items-center justify-between pt-2 border-t border-emerald-50 text-xs text-slate-400">
                  {msg.sources && msg.sources.length > 0 ? (
                    <button
                      onClick={() => handleOpenDrawer(msg.sources)}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg border border-emerald-200 transition text-xs font-semibold"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>Explore Full Legal Excerpts ({msg.sources.length})</span>
                    </button>
                  ) : (
                    <span className="text-[11px] text-slate-400">Statutory Knowledge Graph Active</span>
                  )}

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => copyToClipboard(msg.text, msg.id)}
                      className="p-1.5 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-md transition"
                      title="Copy response"
                    >
                      {copiedId === msg.id ? (
                        <Check className="w-4 h-4 text-emerald-600" />
                      ) : (
                        <Copy className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-emerald-100 shadow-md p-4 rounded-2xl flex items-center gap-3">
              <div className="w-4 h-4 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
              <span className="text-xs font-semibold text-slate-600">
                {language === "hi"
                  ? "आधिकारिक सरकारी पोर्टल (India Code, IP India) और प्राथमिक कला से सत्यापन किया जा रहा है..."
                  : "Grounding citations with real statutory portals & legal knowledge graph..."}
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick suggestions */}
      <div className="py-2.5 flex items-center gap-2 overflow-x-auto text-[13px] no-scrollbar">
        {[
          {
            label: "💡 Section 3(p) TK Bar",
            en: "Can I patent a classical Ayurvedic formulation under Section 3(p)?",
            hi: "क्या मैं शास्त्रीय आयुर्वेदिक दवा का पेटेंट करा सकता हूँ?",
          },
          {
            label: "💡 NBA & ABS Approval",
            en: "What are NBA approval requirements under Biological Diversity Act?",
            hi: "आयुष उत्पाद के लिए एनबीए बायो-रिसोर्स स्वीकृति कैसे लें?",
          },
          {
            label: "💡 AYUSH Aahar vs Drug",
            en: "Difference between AYUSH Aahar FSSAI vs Drug License",
            hi: "आयुष आहार और दवा लाइसेंस में क्या अंतर है?",
          },
          {
            label: "💡 Rule 158-B Licensing",
            en: "What are the clinical trial requirements under Rule 158-B of D&C Rules?",
            hi: "औषधि और प्रसाधन नियम 158-B के तहत लाइसेंस की क्या आवश्यकताएं हैं?",
          },
        ].map((p) => (
          <button
            key={p.label}
            onClick={() => setInputQuery(language === "hi" ? p.hi : p.en)}
            className="t-small px-3.5 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 rounded-full border border-slate-200 hover:border-emerald-300 shrink-0 transition font-medium shadow-2xs"
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Responsive Input bar */}
      <form onSubmit={handleSend} className="relative mt-1">
        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          placeholder={
            language === "hi"
              ? "आयुष आईपी या विनियामक प्रश्न पूछें..."
              : "Ask an Ayurveda IP or regulatory question..."
          }
          className="w-full bg-white border border-emerald-200 focus:border-emerald-500 rounded-2xl pl-5 pr-14 py-4 t-body text-slate-800 placeholder-slate-400 focus:outline-none shadow-sm focus:shadow-md transition text-sm sm:text-base"
        />
        <button
          type="submit"
          disabled={!inputQuery.trim() || loading}
          className="absolute right-3 top-3 p-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl shadow-md transition disabled:opacity-40 disabled:hover:from-emerald-600"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>

      {/* Sources panel drawer */}
      <SourcesPanel
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        sources={selectedSources}
      />
    </div>
  );
};
