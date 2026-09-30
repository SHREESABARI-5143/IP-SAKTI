"use client";

import React, { useState, useRef, useEffect } from "react";
import { sendQuery } from "@/lib/api";
import {
  Send,
  BookOpen,
  Copy,
  Check,
  ShieldAlert,
  Shield,
  Leaf,
  Globe,
  MessageSquare,
} from "lucide-react";
import { SourcesPanel } from "./SourcesPanel";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

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
    setMessages((prev) => {
      if (prev.length === 1 && prev[0].id === "init") {
        return [
          {
            id: "init",
            sender: "bot",
            text: GREETINGS[language] || GREETINGS.en,
            sources: [],
          },
        ];
      }
      return prev;
    });
  }, [language]);

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
          text: t(language, "chatError"),
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
    <div className="flex flex-col h-full w-full max-w-6xl 2xl:max-w-7xl mx-auto px-3 sm:px-6 pt-3 sm:pt-4 pb-2.5">
      {/* Header bar */}
      <div className="flex items-center justify-between gap-3 mb-2.5 px-1 pb-2.5 border-b border-emerald-100/70 shrink-0">
        <div className="flex items-center gap-2.5 sm:gap-3">
          <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-emerald-100 to-teal-100 flex items-center justify-center text-emerald-800 shadow-2xs border border-emerald-200/60">
            <MessageSquare className="w-4.5 h-4.5 text-emerald-700" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base sm:text-lg font-bold text-slate-900 font-manrope">AI Legal Assistant</h1>
              <span className="text-[10px] font-mono font-semibold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full border border-emerald-200 hidden sm:inline-block">
                RAG Active
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">
              Statutory-grounded retrieval • Live links to India Code, IP India &amp; WIPO Lex
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] sm:text-xs font-semibold shadow-2xs transition-colors duration-300 ${
              jurisdiction === "international"
                ? "bg-blue-50 text-blue-900 border border-blue-200/90"
                : "bg-emerald-50 text-emerald-800 border border-emerald-200/90"
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full animate-pulse ${
                jurisdiction === "international" ? "bg-blue-500" : "bg-emerald-500"
              }`}
            />
            <span className="uppercase">{jurisdiction} Jurisdiction</span>
          </span>
        </div>
      </div>

      {/* Messages scroll area */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-1 sm:pr-2 pb-3 min-h-0">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} animate-in fade-in duration-200`}
          >
            <div
              className={`rounded-2xl p-4 sm:p-6 space-y-3.5 transition-all ${
                msg.sender === "user"
                  ? jurisdiction === "international"
                    ? "max-w-xl md:max-w-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-sky-600 text-white shadow-md rounded-br-none shadow-blue-500/15"
                    : "max-w-xl md:max-w-2xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md rounded-br-none shadow-emerald-500/15"
                  : jurisdiction === "international"
                    ? "w-full max-w-4xl lg:max-w-5xl 2xl:max-w-6xl bg-white border border-blue-100/90 text-slate-800 rounded-bl-none shadow-sm hover:shadow-md"
                    : "w-full max-w-4xl lg:max-w-5xl 2xl:max-w-6xl bg-white border border-emerald-100 text-slate-800 rounded-bl-none shadow-sm hover:shadow-md"
              }`}
            >
              {/* Bot header */}
              {msg.sender === "bot" && (
                <div
                  className={`flex items-center justify-between border-b pb-2.5 mb-2 ${
                    jurisdiction === "international" ? "border-blue-50" : "border-emerald-50"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {jurisdiction === "international" ? (
                      <Globe className="w-4 h-4 text-blue-600" />
                    ) : (
                      <Leaf className="w-4 h-4 text-emerald-600" />
                    )}
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
                {t(language, "chatLoading")}
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick suggestions */}
      <div className="py-2 flex items-center gap-1.5 overflow-x-auto text-xs no-scrollbar shrink-0">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider shrink-0 mr-1 hidden sm:inline">
          {t(language, "suggested")}
        </span>
        {[
          { labelKey: "sugg1Label", queryKey: "sugg1Query" },
          { labelKey: "sugg2Label", queryKey: "sugg2Query" },
          { labelKey: "sugg3Label", queryKey: "sugg3Query" },
          { labelKey: "sugg4Label", queryKey: "sugg4Query" },
        ].map((p) => (
          <button
            key={p.labelKey}
            onClick={() => setInputQuery(t(language, p.queryKey))}
            className="px-3 py-1.5 bg-white/90 hover:bg-emerald-50 text-slate-700 hover:text-emerald-900 rounded-full border border-slate-200/90 hover:border-emerald-300 shrink-0 transition-all font-medium shadow-2xs text-[11px] cursor-pointer hover:scale-[1.02]"
          >
            💡 {t(language, p.labelKey)}
          </button>
        ))}
      </div>

      {/* Floating Responsive Input Bar */}
      <form onSubmit={handleSend} className="relative mt-1 shrink-0">
        <div
          className={`relative flex items-center bg-white rounded-2xl border shadow-sm transition-all ${
            jurisdiction === "international"
              ? "border-blue-200/90 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-400/20"
              : "border-emerald-200/90 focus-within:border-emerald-500 focus-within:ring-2 focus-within:ring-emerald-400/20"
          }`}
        >
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={t(language, "inputPlaceholder")}
            className="w-full bg-transparent pl-4 sm:pl-5 pr-14 py-3.5 sm:py-4 text-xs sm:text-sm text-slate-800 placeholder-slate-400 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!inputQuery.trim() || loading}
            className={`absolute right-2 sm:right-2.5 p-2 sm:p-2.5 text-white rounded-xl shadow-xs transition-all disabled:opacity-40 cursor-pointer hover:scale-105 active:scale-95 ${
              jurisdiction === "international"
                ? "bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 disabled:hover:from-blue-600 shadow-blue-500/20"
                : "bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 disabled:hover:from-emerald-600 shadow-emerald-500/20"
            }`}
            aria-label="Send Query"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>

      {/* Institutional Legal Disclaimer Note */}
      <div className="mt-2 text-center text-[11px] text-slate-400 flex items-center justify-center gap-1.5 font-medium shrink-0">
        <Shield className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
        <span className="line-clamp-1">
          {t(language, "statutoryDisclaimer")}
        </span>
      </div>

      {/* Sources panel drawer */}
      <SourcesPanel
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        sources={selectedSources}
      />
    </div>
  );
};
