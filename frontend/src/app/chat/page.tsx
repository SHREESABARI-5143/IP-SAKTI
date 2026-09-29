"use client";

import React, { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { ChatInterface } from "@/components/ChatInterface";
import { SupportedLanguage } from "@/components/LanguageSelector";

export default function ChatPage() {
  const [jurisdiction, setJurisdiction] = useState<"india" | "international" | "both">("india");
  const [language, setLanguage] = useState<SupportedLanguage>("en");

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/50 relative">
      {/* Continuous slight-visible Ayurvedic background */}
      <div
        className="fixed inset-0 bg-cover bg-center pointer-events-none opacity-[0.16] z-0"
        style={{ backgroundImage: "url('/ayurveda_hero_bg.jpg')" }}
      />
      <div className="fixed inset-0 bg-white/80 pointer-events-none z-0" />

      <Navbar
        jurisdiction={jurisdiction}
        onJurisdictionChange={setJurisdiction}
        language={language}
        onLanguageChange={setLanguage}
      />
      <main className="flex-1 relative z-10">
        <ChatInterface jurisdiction={jurisdiction} language={language} />
      </main>
      <Footer />
    </div>
  );
}
