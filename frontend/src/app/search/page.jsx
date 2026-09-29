"use client";

import React from "react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { PriorArtSearch } from "@/components/PriorArtSearch";
import { useApp } from "@/context/AppContext";

export default function SearchPage() {
  const { jurisdiction, setJurisdiction, language, setLanguage } = useApp();

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
      
      <div className="flex-1 flex flex-row w-full relative z-10">
        <Sidebar />
        <main className="flex-1 min-w-0 py-6 px-4 transition-all duration-300">
          <PriorArtSearch language={language} />
        </main>
      </div>

      <Footer />
    </div>
  );
}


