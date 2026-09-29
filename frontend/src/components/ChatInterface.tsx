"use client";

import React, { useState, useRef, useEffect } from "react";
import { sendQuery, QueryResponse, SourceReference } from "@/lib/api";
import {
  Send,
  Sparkles,
  BookOpen,
  Copy,
  Check,
  ShieldAlert,
  Leaf,
  MessageSquare,
} from "lucide-react";
import { SourcesPanel } from "./SourcesPanel";
import { SupportedLanguage } from "./LanguageSelector";

interface Message {
  id: string;
  sender: "user" | "bot";
  text: string;
  confidence?: "HIGH" | "MEDIUM" | "LOW";
  sources?: SourceReference[];
  disclaimer?: string;
}

interface ChatInterfaceProps {
  jurisdiction: "india" | "international" | "both";
  language: SupportedLanguage;
}

const GREETINGS: Record<SupportedLanguage, string> = {
  en: "Welcome! I am IP-SAKTI Sahayak, your source-cited, jurisdiction-aware AI assistant for Ayurveda IP law and regulatory guidance. How can I assist you today?",
  hi: "नमस्ते! मैं IP-SAKTI सहायक हूँ। मैं आयुर्वेद, आईपी कानून (पेटेंट, जीआई, ट्रेडमार्क, जैव विविधता) तथा आयुष नियमों के लिए आपका स्रोत-सत्यापित एआई सहायक हूँ। आप अपना प्रश्न पूछ सकते हैं।",
  sa: "नमस्ते! अहम् IP-SAKTI सहायकः अस्मि। आयुर्वेदशास्त्रे, बौद्धिक-सम्पत्ति-विधौ (Patents, TK, GI, Biodiversity) च भवतः साहाय्यार्थं सज्जोऽस्मि। स्वप्रश्नं पृच्छतु।",
  ta: "வணக்கம்! நான் IP-SAKTI சகாயக். ஆயுர்வேத ஐபி சட்டங்கள், காப்புரிமை மற்றும் ஆயுஷ் ஒழுங்குமுறை விதிகளுக்கான உங்கள் நம்பகமான சட்ட வழிகாட்டி. உங்கள் கேள்வியைக் கேளுங்கள்.",
  te: "నమస్కారం! నేను IP-SAKTI సహాయక్. ఆయుర్వేద మేధో సంపత్తి చట్టాలు, పేటెంట్లు మరియు ఆయుష్ నియంత్రణలపై మీ విశ్వసనీయ సహాయకుడిని. మీ ప్రశ్నను అడగండి.",
  mr: "नमस्कार! मी IP-SAKTI सहाय्यक आहे. आयुर्वेद, आयपी कायदे (पेटंट, जीआय, जैवविविधता) आणि आयुष नियमांसाठी आपला स्रोत-सत्यापित सहाय्यक. आपला प्रश्न विचारा.",
  bn: "নমস্কার! আমি IP-SAKTI সহায়ক। আয়ুর্বেদ আইপি আইন, পেটেন্ট এবং আয়ুশ বিধিমালার জন্য আপনার যাচাইকৃত সহকারী। আপনার প্রশ্ন জিজ্ঞাসা করুন।",
};

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  jurisdiction,
  language,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      sender: "bot",
      text: GREETINGS[language] || GREETINGS.en,
    },
  ]);
  const [inputQuery, setInputQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedSources, setSelectedSources] = useState<SourceReference[]>([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState<boolean>(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (e: React.FormEvent) => {
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
      const res: QueryResponse = await sendQuery(userText, jurisdiction, language);
      setMessages((prev) => [
        ...prev,
        {
          id: botMsgId,
          sender: "bot",
          text: res.answer,
          confidence: res.confidence,
          sources: res.sources,
          disclaimer: res.disclaimer,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: botMsgId,
          sender: "bot",
          text:
            language === "hi"
              ? "क्षमा करें, आपके अनुरोध को संसाधित करते समय एक त्रुटि हुई। कृपया पुनः प्रयास करें।"
              : "Apologies, an error occurred while retrieving sources. Please try again.",
          confidence: "LOW",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDrawer = (sources: SourceReference[]) => {
    setSelectedSources(sources);
    setIsDrawerOpen(true);
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4.25rem)] max-w-5xl mx-auto p-2 sm:p-4">

      {/* Page heading */}
      <div className="flex items-center gap-3 mb-3 px-1">
        <div className="w-9 h-9 rounded-xl bg-emerald-100 flex items-center justify-center">
          <MessageSquare className="w-5 h-5 text-emerald-700" />
        </div>
        <div>
          <h1 className="t-card-heading text-slate-900">AI Legal Assistant</h1>
          <p className="t-small text-slate-500">Source-cited answers • Real statutory corpus</p>
        </div>
      </div>

      {/* Messages scroll area */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-1 pb-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} animate-in fade-in duration-200`}
          >
            <div
              className={`max-w-2xl rounded-2xl p-4 sm:p-5 space-y-3 ${
                msg.sender === "user"
                  ? "bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg shadow-emerald-500/20 rounded-br-none"
                  : "bg-white border border-emerald-100 text-slate-800 rounded-bl-none shadow-md hover:shadow-lg transition-shadow"
              }`}
            >
              {/* Bot header */}
              {msg.sender === "bot" && (
                <div className="flex items-center justify-between border-b border-emerald-50 pb-2 mb-2">
                  <div className="flex items-center gap-2">
                    <Leaf className="w-4 h-4 text-emerald-600" />
                    <span className="t-label text-slate-700">IP-SAKTI Sahayak</span>
                  </div>

                  {msg.confidence && (
                    <span
                      className={`t-label px-2.5 py-0.5 rounded-full border ${
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

              {/* Text */}
              <div className={`t-body leading-relaxed whitespace-pre-line ${msg.sender === "user" ? "text-white" : "text-slate-800"}`}>
                {msg.text}
              </div>

              {/* Disclaimer */}
              {msg.disclaimer && (
                <div className="flex items-start gap-2 text-xs text-amber-700 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
                  <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5 text-amber-500" />
                  <span>{msg.disclaimer}</span>
                </div>
              )}

              {/* Bot actions */}
              {msg.sender === "bot" && (
                <div className="flex items-center justify-between pt-2 border-t border-emerald-50 text-xs text-slate-400">
                  {msg.sources && msg.sources.length > 0 ? (
                    <button
                      onClick={() => handleOpenDrawer(msg.sources!)}
                      className="flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg border border-emerald-200 transition text-[11px] font-semibold"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>View {msg.sources.length} Cited Sources</span>
                    </button>
                  ) : (
                    <span className="text-[11px] text-slate-400">Statutory Search Active</span>
                  )}

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => copyToClipboard(msg.text, msg.id)}
                      className="p-1 hover:text-slate-700 transition"
                      title="Copy response"
                    >
                      {copiedId === msg.id ? (
                        <Check className="w-3.5 h-3.5 text-emerald-600" />
                      ) : (
                        <Copy className="w-3.5 h-3.5" />
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
              <span className="text-xs font-semibold text-slate-500">
                {language === "hi"
                  ? "कानूनी धाराओं और टीकेडीएल प्राथमिक कला को खोजा जा रहा है..."
                  : "Retrieving verified legal sections & statutes..."}
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick prompts */}
      <div className="py-2 flex items-center gap-2 overflow-x-auto text-[13px]">
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
        ].map((p) => (
          <button
            key={p.label}
            onClick={() => setInputQuery(language === "hi" ? p.hi : p.en)}
            className="t-small px-3.5 py-1.5 bg-white hover:bg-emerald-50 text-slate-600 hover:text-emerald-700 rounded-full border border-slate-200 hover:border-emerald-200 shrink-0 transition font-medium shadow-xs"
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Input bar */}
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
          className="w-full bg-white border border-emerald-200 focus:border-emerald-500 rounded-2xl pl-4 pr-12 py-3.5 t-body text-slate-800 placeholder-slate-400 focus:outline-none shadow-md focus:shadow-lg transition"
        />
        <button
          type="submit"
          disabled={!inputQuery.trim() || loading}
          className="absolute right-2.5 top-2.5 p-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white rounded-xl shadow-md transition disabled:opacity-40"
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
