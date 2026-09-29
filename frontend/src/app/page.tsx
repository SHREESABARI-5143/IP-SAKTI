"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { SupportedLanguage } from "@/components/LanguageSelector";
import {
  Sparkles,
  ArrowRight,
  CheckCircle2,
  Globe,
  Shield,
  BookOpen,
  Scale,
  Microscope,
  Users,
  Zap,
  Lock,
  BadgeCheck,
  ChevronRight,
  Database,
  Brain,
} from "lucide-react";
import {
  KhalvaIcon,
  TalapatraIcon,
  TulsiLeafIcon,
  LotusIcon,
  KalashIcon,
  AyurvedaNyayaIcon,
} from "@/components/AyurvedicIcons";
import { AyurvedicMandala } from "@/components/AyurvedicMandala";

export default function Home() {
  const [jurisdiction, setJurisdiction] = useState<"india" | "international" | "both">("india");
  const [language, setLanguage] = useState<SupportedLanguage>("en");

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/50 relative">
      {/* ═══════ CONTINUOUS SLIGHTLY VISIBLE AYURVEDIC BACKGROUND ACROSS ENTIRE PAGE ═══════ */}
      <div
        className="fixed inset-0 bg-cover bg-center pointer-events-none opacity-[0.20] z-0 transition-opacity duration-1000"
        style={{ backgroundImage: "url('/ayurveda_hero_bg.jpg')" }}
      />
      <div className="fixed inset-0 bg-gradient-to-b from-white/70 via-white/85 to-white/70 pointer-events-none z-0" />

      {/* Navbar with 7-Language Selector */}
      <Navbar
        jurisdiction={jurisdiction}
        onJurisdictionChange={setJurisdiction}
        language={language}
        onLanguageChange={setLanguage}
      />

      <main className="flex-1 w-full relative z-10">
        {/* ═══════ HERO SECTION WITH VISIBLE AYURVEDIC BACKGROUND & VEDIC MANDALA ANIMATION ═══════ */}
        <section className="relative overflow-hidden min-h-[620px] flex items-center border-b border-emerald-100/60">
          {/* Mild Ayurvedic Background Image with slightly higher visibility */}
          <div
            className="absolute inset-0 bg-cover bg-top pointer-events-none opacity-[0.40] transition-opacity duration-700"
            style={{ backgroundImage: "url('/ayurveda_hero_bg.jpg')" }}
          />

          {/* Soft center radial wash allowing the Ayurvedic texture to stay visible while keeping text ultra-crisp */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background:
                "radial-gradient(circle at center, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0.80) 55%, rgba(236,253,245,0.50) 100%)",
            }}
          />

          {/* Sacred Ayurvedic Vedic Mandala & Drifting Botanical Leaves Animation */}
          <AyurvedicMandala className="absolute inset-0" />

          {/* Ambient blurred emerald glow orbs */}
          <div className="absolute top-[-100px] left-[-60px] w-[380px] h-[380px] rounded-full bg-emerald-100/50 blur-[100px] animate-prana-breathe pointer-events-none" />
          <div
            className="absolute bottom-[-60px] right-[-40px] w-[320px] h-[320px] rounded-full bg-teal-100/45 blur-[90px] animate-prana-breathe pointer-events-none"
            style={{ animationDelay: "3s" }}
          />

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 pt-14 pb-16 text-center space-y-7 z-10">
            {/* Pill badge with Tulsi Leaf */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-50/95 border border-emerald-200/90 text-emerald-800 t-label shadow-xs backdrop-blur-md">
              <TulsiLeafIcon className="w-4 h-4 text-emerald-600 animate-pulse" />
              <span>Ministry of Ayush &bull; Classical Knowledge &amp; Precision IP Intelligence</span>
            </div>

            {/* Headline */}
            <h1 className="t-hero text-slate-900 max-w-4xl mx-auto">
              Guarding India&apos;s{" "}
              <span className="text-gradient-emerald">Ayurvedic Heritage</span>
              <br className="hidden sm:block" />
              with Precision IP Intelligence
            </h1>

            {/* Sub-headline */}
            <p className="t-body text-slate-600 max-w-2xl mx-auto">
              Bridge 5,000 years of codified Ayurvedic wisdom (AFI, API, TKDL) with Indian IP statutes
              (Patents Act Sec 3(p), BD Act 2002), International Treaties (TRIPS/Nagoya), and Drug
              Licensing &mdash; powered by verified legal RAG.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-wrap items-center justify-center gap-4 pt-1">
              <Link
                href="/chat"
                className="group t-btn gap-2.5 px-7 py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl shadow-lg shadow-emerald-600/20 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-emerald-600/30"
              >
                <Sparkles className="w-4 h-4" />
                <span>Launch AI Legal Assistant</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>

              <Link
                href="/classify"
                className="group t-btn gap-2.5 px-7 py-3.5 bg-white/95 hover:bg-emerald-50 text-emerald-800 border-2 border-emerald-200 hover:border-emerald-400 rounded-xl transition-all duration-300 hover:-translate-y-0.5 shadow-sm backdrop-blur-xs"
              >
                <KalashIcon className="w-4 h-4 text-emerald-600" />
                <span>Classify Your Product</span>
                <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              </Link>
            </div>

            {/* ═══════ CREATIVE AYURVEDIC HERITAGE & LEGAL DEFENSE PILLARS ═══════ */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-6 max-w-5xl mx-auto text-left">
              {/* Pillar 1 - Classical AFI / API Monographs */}
              <div className="p-4.5 rounded-2xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-sm hover:shadow-md hover:border-emerald-300 transition-all duration-300 group">
                <div className="w-10 h-10 rounded-xl bg-emerald-100/80 flex items-center justify-center text-emerald-700 mb-3 group-hover:scale-105 transition-transform">
                  <KhalvaIcon className="w-5 h-5" />
                </div>
                <h4 className="t-card-heading text-slate-900 text-sm">AFI &amp; API Monographs</h4>
                <p className="t-small text-slate-500 mt-1 leading-relaxed">
                  Codified formulations (Kalka, Kwatha, Asava, Bhasma) from authentic pharmacopoeial texts.
                </p>
                <span className="t-label inline-block mt-2.5 text-emerald-700 font-medium">15+ Classical Formulations</span>
              </div>

              {/* Pillar 2 - Defensive TKDL Prior-Art */}
              <div className="p-4.5 rounded-2xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-sm hover:shadow-md hover:border-teal-300 transition-all duration-300 group">
                <div className="w-10 h-10 rounded-xl bg-teal-100/80 flex items-center justify-center text-teal-700 mb-3 group-hover:scale-105 transition-transform">
                  <TalapatraIcon className="w-5 h-5" />
                </div>
                <h4 className="t-card-heading text-slate-900 text-sm">Defensive TKDL Shield</h4>
                <p className="t-small text-slate-500 mt-1 leading-relaxed">
                  Preempt predatory patents and biopiracy across global patent offices (USPTO, EPO, JPO).
                </p>
                <span className="t-label inline-block mt-2.5 text-teal-700 font-medium">Codified Prior-Art</span>
              </div>

              {/* Pillar 3 - Section 3(p) Patent Law */}
              <div className="p-4.5 rounded-2xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-sm hover:shadow-md hover:border-emerald-300 transition-all duration-300 group">
                <div className="w-10 h-10 rounded-xl bg-emerald-100/80 flex items-center justify-center text-emerald-700 mb-3 group-hover:scale-105 transition-transform">
                  <AyurvedaNyayaIcon className="w-5 h-5" />
                </div>
                <h4 className="t-card-heading text-slate-900 text-sm">Section 3(p) TK-Bar</h4>
                <p className="t-small text-slate-500 mt-1 leading-relaxed">
                  Indian Patents Act non-patentability checks &amp; National Biodiversity Authority (NBA) ABS compliance.
                </p>
                <span className="t-label inline-block mt-2.5 text-emerald-700 font-medium">Statutory Verification</span>
              </div>

              {/* Pillar 4 - 6-Tier Product Classification */}
              <div className="p-4.5 rounded-2xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-sm hover:shadow-md hover:border-amber-300 transition-all duration-300 group">
                <div className="w-10 h-10 rounded-xl bg-amber-100/80 flex items-center justify-center text-amber-700 mb-3 group-hover:scale-105 transition-transform">
                  <KalashIcon className="w-5 h-5" />
                </div>
                <h4 className="t-card-heading text-slate-900 text-sm">6-Tier Regulatory Path</h4>
                <p className="t-small text-slate-500 mt-1 leading-relaxed">
                  Classical ASU Drug, Patent &amp; Proprietary, Phytomedicine, AYUSH Aahar &amp; Cosmeceuticals.
                </p>
                <span className="t-label inline-block mt-2.5 text-amber-700 font-medium">D&amp;C Act Rule 158-B</span>
              </div>
            </div>
          </div>
        </section>

        {/* ═══════ THREE POWERFUL MODULES SECTION ═══════ */}
        <section className="relative py-20 bg-white/80 backdrop-blur-md border-b border-emerald-100/60">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 space-y-12">
            <div className="text-center space-y-3">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100/90 text-emerald-800 t-label mx-auto">
                <LotusIcon className="w-4 h-4 text-emerald-700" />
                <span>Ayurvedic Legal Intelligence Suite</span>
              </div>
              <h2 className="t-section text-slate-900">
                Three Precision Engines, One Classical Platform
              </h2>
              <p className="t-body text-slate-500 max-w-xl mx-auto">
                Every engine is grounded in real statutory texts, Gemini AI vector embeddings, and authentic
                pharmacopoeial monographs &mdash; zero mock data, zero hallucinations.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {/* Card 1 - AI Legal Assistant */}
              <Link href="/chat" className="group">
                <div className="h-full p-7 rounded-2xl bg-white/95 backdrop-blur-sm border border-emerald-100 shadow-sm hover:shadow-lg hover:border-emerald-300 transition-all duration-300 hover:-translate-y-1 space-y-4">
                  <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 group-hover:scale-110 transition-transform">
                    <Brain className="w-6 h-6" />
                  </div>
                  <h3 className="t-card-heading text-slate-900">AI Legal Assistant (RAG)</h3>
                  <p className="t-small text-slate-600 leading-relaxed">
                    Ask any Ayurveda IP question in any of the 7 supported Indian languages. Get jurisdiction-specific answers
                    with mandatory inline statutory citations like{" "}
                    <code className="text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded text-xs font-mono">[Source: Patents Act, Sec 3(p)]</code>.
                  </p>
                  <div className="flex flex-wrap gap-2 pt-1">
                    {["Section 3(p)", "BD Act", "TRIPS", "7 Languages"].map((tag) => (
                      <span key={tag} className="t-label px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="flex items-center gap-1.5 t-btn text-emerald-700 pt-2 group-hover:gap-2.5 transition-all">
                    <span>Start Querying</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>

              {/* Card 2 - Product Classifier */}
              <Link href="/classify" className="group">
                <div className="h-full p-7 rounded-2xl bg-white/95 backdrop-blur-sm border border-emerald-100 shadow-sm hover:shadow-lg hover:border-emerald-300 transition-all duration-300 hover:-translate-y-1 space-y-4">
                  <div className="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center text-amber-700 group-hover:scale-110 transition-transform">
                    <Scale className="w-6 h-6" />
                  </div>
                  <h3 className="t-card-heading text-slate-900">6-Category Regulatory Classifier</h3>
                  <p className="t-small text-slate-600 leading-relaxed">
                    Walk through a guided decision tree to classify your Ayurvedic product into Classical ASU Drug,
                    Patent &amp; Proprietary, Phytopharmaceutical, Nutraceutical, Cosmeceutical, or AYUSH Aahar.
                  </p>
                  <div className="flex flex-wrap gap-2 pt-1">
                    {["D&C Act", "FSSAI", "Schedule T", "Rule 158-B"].map((tag) => (
                      <span key={tag} className="t-label px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="flex items-center gap-1.5 t-btn text-emerald-700 pt-2 group-hover:gap-2.5 transition-all">
                    <span>Classify Now</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>

              {/* Card 3 - Prior-Art Search */}
              <Link href="/search" className="group">
                <div className="h-full p-7 rounded-2xl bg-white/95 backdrop-blur-sm border border-emerald-100 shadow-sm hover:shadow-lg hover:border-emerald-300 transition-all duration-300 hover:-translate-y-1 space-y-4">
                  <div className="w-12 h-12 rounded-xl bg-teal-50 flex items-center justify-center text-teal-700 group-hover:scale-110 transition-transform">
                    <Microscope className="w-6 h-6" />
                  </div>
                  <h3 className="t-card-heading text-slate-900">Prior-Art Search (AFI / API)</h3>
                  <p className="t-small text-slate-600 leading-relaxed">
                    Enter your formulation ingredients and uncover classical matches from the
                    Ayurvedic Formulary of India. Real vector similarity against authentic pharmacopoeial monographs.
                  </p>
                  <div className="flex flex-wrap gap-2 pt-1">
                    {["AFI Part I", "TKDL", "Qdrant", "Gemini Embed"].map((tag) => (
                      <span key={tag} className="t-label px-2.5 py-1 rounded-full bg-teal-50 text-teal-700 border border-teal-200">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="flex items-center gap-1.5 t-btn text-emerald-700 pt-2 group-hover:gap-2.5 transition-all">
                    <span>Search Prior Art</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </section>

        {/* ═══════ WHY US / ABOUT SECTION ═══════ */}
        <section className="relative py-24 bg-white/85 backdrop-blur-md overflow-hidden">
          {/* Decorative circles */}
          <div className="absolute -left-32 top-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-emerald-50 rounded-full blur-[80px] pointer-events-none" />

          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              {/* Left column - text */}
              <div className="space-y-8">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 t-label">
                  <Shield className="w-3.5 h-3.5" />
                  <span>Why AYURA (IP-SAKTI Sahayak)?</span>
                </div>

                <h2 className="t-section text-slate-900 leading-tight">
                  The Only Platform That{" "}
                  <span className="text-gradient-emerald">Refuses to Hallucinate</span>{" "}
                  About Your Legal Rights
                </h2>

                <p className="t-body text-slate-600 leading-relaxed">
                  India possesses over 5,000 years of documented traditional medicine &mdash; yet
                  AYUSH innovators still lose patents to bio-piracy, navigate fragmented regulations
                  across 7+ statutory regimes, and receive AI answers with fabricated section numbers.
                  We built AYURA to end that with rigorous source citations.
                </p>

                <div className="space-y-5">
                  {[
                    {
                      icon: <Database className="w-5 h-5" />,
                      title: "100% Authentic Corpus — Zero Mock Data",
                      desc: "Every legal reference comes from statutory texts of the Patents Act 1970, BD Act 2002, D&C Act 1940, AFI Part I, TRIPS, and Nagoya Protocol. We index real sections, not summaries.",
                    },
                    {
                      icon: <BadgeCheck className="w-5 h-5" />,
                      title: "Mandatory Citation Verification",
                      desc: "Every AI answer MUST include inline citations like [Source: Patents Act, Section 3(p)]. If Gemini can't cite a real source, it says \"I don't have enough verified material\" instead of guessing.",
                    },
                    {
                      icon: <Globe className="w-5 h-5" />,
                      title: "Strict Jurisdiction Isolation",
                      desc: "Query Indian law? You'll only get Indian statutory results. Query international? Only TRIPS, PCT, Nagoya, and CBD. Zero cross-contamination between jurisdictions.",
                    },
                    {
                      icon: <Lock className="w-5 h-5" />,
                      title: "Built for Ministry-Grade Trust",
                      desc: "DPDP Act 2023 compliant architecture, audit logging of every query, session persistence, and feedback capture. Designed for government deployment standards.",
                    },
                  ].map((item, i) => (
                    <div key={i} className="flex gap-4 group">
                      <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 shrink-0 group-hover:bg-emerald-200 transition-colors">
                        {item.icon}
                      </div>
                      <div>
                        <h4 className="t-card-heading text-slate-900 text-base">{item.title}</h4>
                        <p className="t-small text-slate-500 mt-1 leading-relaxed">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Right column - visual card stack */}
              <div className="relative space-y-5">
                {/* Card: Real Data Pipeline */}
                <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-md hover:shadow-lg transition-all duration-300 space-y-3 animate-float-slow">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center">
                      <Zap className="w-4 h-4 text-emerald-700" />
                    </div>
                    <span className="t-card-heading text-slate-900 text-sm">Real-Time RAG Pipeline</span>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap t-label">
                    <span className="px-2 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">Query</span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span className="px-2 py-1 rounded-full bg-teal-50 text-teal-700 border border-teal-200">Gemini Embed</span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span className="px-2 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">Qdrant Search</span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span className="px-2 py-1 rounded-full bg-teal-50 text-teal-700 border border-teal-200">Gemini 2.5 Flash</span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span className="px-2 py-1 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">Cited Answer</span>
                  </div>
                </div>

                {/* Card: Corpus Breakdown */}
                <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-md hover:shadow-lg transition-all duration-300 space-y-4" style={{ animationDelay: "1s" }}>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center">
                      <BookOpen className="w-4 h-4 text-amber-700" />
                    </div>
                    <span className="t-card-heading text-slate-900 text-sm">Indexed Legal Corpus</span>
                  </div>
                  <div className="space-y-2">
                    {[
                      { label: "Patents Act, 1970", count: "13 sections", color: "emerald" },
                      { label: "Biological Diversity Act, 2002", count: "6 sections", color: "teal" },
                      { label: "Drugs & Cosmetics Act, 1940", count: "7 provisions", color: "emerald" },
                      { label: "Classical AFI Formulations", count: "15 monographs", color: "amber" },
                      { label: "TRIPS / Nagoya / CBD / PCT", count: "11 articles", color: "teal" },
                    ].map((item, i) => (
                      <div key={i} className="flex items-center justify-between t-small">
                        <span className="text-slate-700 font-medium">{item.label}</span>
                        <span className="t-label px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                          {item.count}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Card: Who Is This For */}
                <div className="p-6 rounded-2xl bg-emerald-50/70 border border-emerald-200 shadow-sm space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-emerald-200 flex items-center justify-center">
                      <Users className="w-4 h-4 text-emerald-800" />
                    </div>
                    <span className="t-card-heading text-emerald-900 text-sm">Built For</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2.5">
                    {[
                      "Ayurvedic Researchers",
                      "Traditional Vaidyas",
                      "AYUSH Startups & MSMEs",
                      "Patent Attorneys",
                      "Ministry Regulators",
                      "Drug Licensing Officers",
                    ].map((role) => (
                      <div key={role} className="flex items-center gap-2 t-small text-emerald-900 font-medium">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                        <span>{role}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ═══════ CTA BANNER ═══════ */}
        <section className="py-16 bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700 text-white">
          <div className="max-w-4xl mx-auto px-4 text-center space-y-6">
            <h2 className="t-section text-white">
              Ready to Protect Your Ayurvedic Innovation?
            </h2>
            <p className="t-body text-emerald-100 max-w-xl mx-auto">
              Start with a free legal query, classify your product into the correct regulatory
              category, or search for prior art in seconds.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-4">
              <Link
                href="/chat"
                className="group t-btn gap-2 px-7 py-3.5 bg-white text-emerald-800 rounded-xl shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl"
              >
                <Sparkles className="w-4 h-4" />
                <span>Ask AI Legal Assistant</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
              <Link
                href="/search"
                className="t-btn gap-2 px-7 py-3.5 bg-emerald-800/40 hover:bg-emerald-800/60 text-white border border-emerald-400/30 rounded-xl transition-all hover:-translate-y-0.5"
              >
                <KhalvaIcon className="w-4 h-4 text-white" />
                <span>Search Prior Art</span>
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
