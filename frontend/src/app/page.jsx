"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
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
import { GlobalWorldBackground } from "@/components/GlobalWorldBackground";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

export default function Home() {
  const { jurisdiction, setJurisdiction, language, setLanguage } = useApp();
  const isInternational = jurisdiction === "international";

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/50 relative">
      {/* ═══════ CONTINUOUS SLIGHTLY VISIBLE BACKGROUND ACROSS ENTIRE PAGE ═══════ */}
      <div
        className={`fixed inset-0 bg-cover bg-center pointer-events-none transition-opacity duration-1000 z-0 ${
          isInternational ? "opacity-[0.14]" : "opacity-[0.20]"
        }`}
        style={{
          backgroundImage: isInternational
            ? "radial-gradient(#2563eb 0.8px, transparent 0.8px), radial-gradient(#0284c7 0.8px, #f8fafc 0.8px)"
            : "url('/ayurveda_hero_bg.jpg')",
          backgroundSize: isInternational ? "28px 28px, 28px 28px" : "cover",
          backgroundPosition: isInternational ? "0 0, 14px 14px" : "center",
        }}
      />
      <div
        className={`fixed inset-0 pointer-events-none z-0 transition-colors duration-1000 ${
          isInternational
            ? "bg-gradient-to-b from-white/80 via-blue-50/40 to-white/80"
            : "bg-gradient-to-b from-white/70 via-white/85 to-white/70"
        }`}
      />

      {/* Navbar with 7-Language Selector */}
      <Navbar
        jurisdiction={jurisdiction}
        onJurisdictionChange={setJurisdiction}
        language={language}
        onLanguageChange={setLanguage}
      />

      <main className="flex-1 w-full relative z-10">
        {/* ═══════ HERO SECTION: AYURVEDIC MANDALA (INDIA) OR ROTATING 3D GLOBAL WORLD (INTERNATIONAL) ═══════ */}
        <section
          className={`relative overflow-hidden min-h-[calc(100vh-4rem)] flex items-center justify-center border-b py-3 sm:py-5 px-4 transition-colors duration-500 ${
            isInternational ? "border-blue-100/70" : "border-emerald-100/60"
          }`}
        >
          {/* Subtle Background Texture */}
          {!isInternational && (
            <div
              className="absolute inset-0 bg-cover bg-top pointer-events-none opacity-[0.35] transition-opacity duration-700"
              style={{ backgroundImage: "url('/ayurveda_hero_bg.jpg')" }}
            />
          )}

          {/* Soft center radial wash keeping foreground text ultra-crisp */}
          <div
            className="absolute inset-0 pointer-events-none transition-all duration-700"
            style={{
              background: isInternational
                ? "radial-gradient(circle at center, rgba(255,255,255,0.94) 0%, rgba(240,249,255,0.85) 55%, rgba(224,242,254,0.50) 100%)"
                : "radial-gradient(circle at center, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0.80) 55%, rgba(236,253,245,0.50) 100%)",
            }}
          />

          {/* DYNAMIC BACKGROUND EFFECT:
              • India: Sacred Vedic Mandala & Drifting Botanical Tulsi Leaves
              • International: 3D Rotating Global World Sphere with Orbital Treaty Rings & Pulsing Hubs */}
          {isInternational ? (
            <GlobalWorldBackground className="absolute inset-0" />
          ) : (
            <AyurvedicMandala className="absolute inset-0" />
          )}

          {/* Ambient blurred glow orbs (Emerald for India, Royal Blue / Cyan for International) */}
          <div
            className={`absolute top-[-100px] left-[-60px] w-[380px] h-[380px] rounded-full blur-[100px] animate-prana-breathe pointer-events-none transition-colors duration-700 ${
              isInternational ? "bg-blue-200/50" : "bg-emerald-100/50"
            }`}
          />
          <div
            className={`absolute bottom-[-60px] right-[-40px] w-[320px] h-[320px] rounded-full blur-[90px] animate-prana-breathe pointer-events-none transition-colors duration-700 ${
              isInternational ? "bg-sky-200/45" : "bg-teal-100/45"
            }`}
            style={{ animationDelay: "3s" }}
          />

          <div className="relative max-w-7xl mx-auto px-2 sm:px-4 w-full text-center flex flex-col justify-center items-center space-y-2.5 sm:space-y-3 z-10">
            {/* Sacred Product Emblem - High Visibility Showcase */}
            <div className="flex flex-col items-center justify-center">
              <div className="relative group">
                {/* Ambient glow behind logo */}
                <div
                  className={`absolute -inset-1.5 rounded-2xl blur-lg opacity-70 group-hover:opacity-100 transition duration-500 pointer-events-none ${
                    isInternational
                      ? "bg-gradient-to-r from-blue-500/35 via-indigo-500/30 to-sky-500/35"
                      : "bg-gradient-to-r from-emerald-500/30 via-teal-500/25 to-emerald-500/30"
                  }`}
                />

                <div
                  className={`relative w-16 h-16 sm:w-20 sm:h-20 md:w-22 md:h-22 rounded-2xl p-1.5 shadow-md hover:scale-105 transition-all duration-300 backdrop-blur-md ${
                    isInternational
                      ? "bg-gradient-to-br from-blue-500/40 via-blue-600/30 to-indigo-500/40 shadow-blue-600/20 border border-blue-300/80"
                      : "bg-gradient-to-br from-emerald-500/40 via-emerald-600/30 to-teal-500/40 shadow-emerald-600/20 border border-emerald-300/80"
                  }`}
                >
                  <div className="w-full h-full bg-[#fdfbf7] rounded-xl p-1 flex items-center justify-center overflow-hidden shadow-inner">
                    <img
                      src="/ayura_logo.png"
                      alt="AYURA Official Emblem"
                      className="w-full h-full object-contain filter drop-shadow-xs transition-transform duration-300 group-hover:scale-105"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Pill badge: Tulsi leaf (India) or Global Treaties (International) */}
            <div
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] sm:text-xs font-semibold shadow-2xs backdrop-blur-md transition-colors duration-300 ${
                isInternational
                  ? "bg-blue-50/95 border border-blue-200/90 text-blue-900 shadow-blue-500/10"
                  : "bg-emerald-50/95 border border-emerald-200/90 text-emerald-800"
              }`}
            >
              {isInternational ? (
                <span>Global Treaties • TRIPS Agreement • Nagoya Protocol • CBD • PCT</span>
              ) : (
                <>
                  <TulsiLeafIcon className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
                  <span>{t(language, "heroBadge")}</span>
                </>
              )}
            </div>

            {/* Headline */}
            {isInternational ? (
              <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-[2.5rem] font-extrabold text-slate-900 max-w-4xl mx-auto leading-tight tracking-tight">
                Defending Traditional Knowledge Across{" "}
                <span className="text-gradient-blue">Global Patent Treaties</span>
                <br className="hidden sm:block" /> with Precision IP Intelligence
              </h1>
            ) : (
              <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-[2.5rem] font-extrabold text-slate-900 max-w-4xl mx-auto leading-tight tracking-tight">
                {t(language, "heroTitlePart1")}{" "}
                <span className="text-gradient-emerald">{t(language, "heroTitleHighlight")}</span>
                <br className="hidden sm:block" />
                {t(language, "heroTitlePart2")}
              </h1>
            )}

            {/* Sub-headline */}
            <p className="text-xs sm:text-sm text-slate-600 max-w-2xl mx-auto leading-relaxed">
              {isInternational
                ? "Harmonize 5,000 years of codified Ayurvedic science with Global IP frameworks — TRIPS Art. 27.3(b), Nagoya Protocol ABS, CBD Sovereign Rights, and PCT applications to preempt biopiracy worldwide."
                : t(language, "heroSubtitle")}
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-wrap items-center justify-center gap-3 pt-0.5">
              <Link
                href="/chat"
                className={`group t-btn gap-2 px-5 py-2.5 sm:px-6 sm:py-3 text-white text-xs sm:text-sm rounded-xl shadow-md transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg cursor-pointer ${
                  isInternational
                    ? "bg-gradient-to-r from-blue-600 via-indigo-600 to-sky-600 hover:from-blue-700 hover:to-indigo-700 shadow-blue-600/25 hover:shadow-blue-600/35"
                    : "bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 shadow-emerald-600/20 hover:shadow-emerald-600/30"
                }`}
              >
                <Sparkles className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                <span>{t(language, "ctaLaunchAssistant")}</span>
                <ArrowRight className="w-3.5 h-3.5 sm:w-4 sm:h-4 transition-transform group-hover:translate-x-1" />
              </Link>

              <Link
                href="/classify"
                className={`group t-btn gap-2 px-5 py-2.5 sm:px-6 sm:py-3 border text-xs sm:text-sm rounded-xl transition-all duration-300 hover:-translate-y-0.5 shadow-2xs backdrop-blur-xs cursor-pointer ${
                  isInternational
                    ? "bg-white/95 hover:bg-blue-50 text-blue-900 border-blue-200 hover:border-blue-400"
                    : "bg-white/95 hover:bg-emerald-50 text-emerald-800 border-emerald-200 hover:border-emerald-400"
                }`}
              >
                {isInternational ? (
                  <Scale className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-600" />
                ) : (
                  <KalashIcon className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-600" />
                )}
                <span>{isInternational ? "Global Export Classification" : t(language, "ctaClassifyProduct")}</span>
                <ChevronRight className="w-3.5 h-3.5 sm:w-4 sm:h-4 transition-transform group-hover:translate-x-0.5" />
              </Link>
            </div>

            {/* ═══════ 4 PILLARS: INDIAN LEGAL DEFENSE OR INTERNATIONAL TREATIES ═══════ */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-3 pt-2 sm:pt-3 max-w-5xl mx-auto text-left w-full">
              {isInternational ? (
                <>
                  {/* Pillar 1 - TRIPS Agreement (Art. 27) */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-blue-100/90 shadow-2xs hover:shadow-xs hover:border-blue-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-blue-100/80 flex items-center justify-center text-blue-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <Globe className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">TRIPS Agreement (Art. 27)</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      Patentability exclusions under Art. 27.3(b), traditional knowledge non-obviousness & WTO flexibilities.
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-blue-700">WTO IP Framework</span>
                  </div>

                  {/* Pillar 2 - Nagoya Protocol ABS */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-blue-100/90 shadow-2xs hover:shadow-xs hover:border-indigo-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-indigo-100/80 flex items-center justify-center text-indigo-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <Scale className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">Nagoya Protocol (ABS)</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      Access & Benefit-Sharing, Prior Informed Consent (PIC), and Mutually Agreed Terms (MAT) for filings.
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-indigo-700">Cross-Border ABS</span>
                  </div>

                  {/* Pillar 3 - CBD Sovereign Rights */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-blue-100/90 shadow-2xs hover:shadow-xs hover:border-sky-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-sky-100/80 flex items-center justify-center text-sky-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <Shield className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">CBD Sovereign Rights</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      Convention on Biological Diversity Art. 15 sovereign resource rights & defensive TKDL challenges.
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-sky-700">Biopiracy Preemption</span>
                  </div>

                  {/* Pillar 4 - WIPO & PCT Applications */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-blue-100/90 shadow-2xs hover:shadow-xs hover:border-blue-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-blue-100/80 flex items-center justify-center text-blue-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <BookOpen className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">WIPO & PCT Applications</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      Prior-art opposition filings across USPTO, EPO, JPO, and WIPO Intergovernmental Committee (IGC).
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-blue-700">Global Enforcement</span>
                  </div>
                </>
              ) : (
                <>
                  {/* Pillar 1 - Classical AFI / API Monographs */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-2xs hover:shadow-xs hover:border-emerald-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-emerald-100/80 flex items-center justify-center text-emerald-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <KhalvaIcon className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">{t(language, "pillar1Title")}</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      {t(language, "pillar1Desc")}
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-emerald-700">{t(language, "pillar1Badge")}</span>
                  </div>

                  {/* Pillar 2 - Defensive TKDL Prior-Art */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-2xs hover:shadow-xs hover:border-teal-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-teal-100/80 flex items-center justify-center text-teal-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <TalapatraIcon className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">{t(language, "pillar2Title")}</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      {t(language, "pillar2Desc")}
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-teal-700">{t(language, "pillar2Badge")}</span>
                  </div>

                  {/* Pillar 3 - Section 3(p) Patent Law */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-2xs hover:shadow-xs hover:border-emerald-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-emerald-100/80 flex items-center justify-center text-emerald-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <AyurvedaNyayaIcon className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">{t(language, "pillar3Title")}</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      {t(language, "pillar3Desc")}
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-emerald-700">{t(language, "pillar3Badge")}</span>
                  </div>

                  {/* Pillar 4 - 6-Tier Product Classification */}
                  <div className="p-3 sm:p-3.5 rounded-xl bg-white/90 backdrop-blur-md border border-emerald-100/90 shadow-2xs hover:shadow-xs hover:border-amber-300 transition-all duration-200 group">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-amber-100/80 flex items-center justify-center text-amber-700 mb-1.5 group-hover:scale-105 transition-transform">
                      <KalashIcon className="w-4 h-4" />
                    </div>
                    <h4 className="font-bold text-slate-900 text-xs sm:text-sm">{t(language, "pillar4Title")}</h4>
                    <p className="text-[11px] sm:text-xs text-slate-500 mt-0.5 leading-snug line-clamp-2">
                      {t(language, "pillar4Desc")}
                    </p>
                    <span className="text-[10px] font-semibold inline-block mt-1.5 text-amber-700">{t(language, "pillar4Badge")}</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </section>

        {/* ═══════ THREE POWERFUL MODULES SECTION ═══════ */}
        <section
          className={`relative py-20 bg-white/80 backdrop-blur-md border-b transition-colors duration-500 ${
            isInternational ? "border-blue-100/70" : "border-emerald-100/60"
          }`}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 space-y-12">
            <div className="text-center space-y-3">
              <div
                className={`inline-flex items-center gap-2 px-3 py-1 rounded-full t-label mx-auto transition-colors duration-300 ${
                  isInternational
                    ? "bg-blue-100/90 text-blue-900"
                    : "bg-emerald-100/90 text-emerald-800"
                }`}
              >
                {isInternational ? (
                  <Globe className="w-4 h-4 text-blue-700" />
                ) : (
                  <LotusIcon className="w-4 h-4 text-emerald-700" />
                )}
                <span>{isInternational ? "Global Patent & Treaty Intelligence Suite" : t(language, "suiteBadge")}</span>
              </div>
              <h2 className="t-section text-slate-900">
                {isInternational ? "Three International Engines, One Unified Platform" : t(language, "suiteTitle")}
              </h2>
              <p className="t-body text-slate-500 max-w-xl mx-auto">
                {isInternational
                  ? "Cross-border legal reasoning, global botanical export classification, and worldwide prior-art search across international treaty frameworks."
                  : t(language, "suiteDesc")}
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {/* Card 1 - AI Legal Assistant */}
              <Link href="/chat" className="group">
                <div
                  className={`h-full p-7 rounded-2xl bg-white/95 backdrop-blur-sm border shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1 space-y-4 ${
                    isInternational
                      ? "border-blue-100 hover:border-blue-300"
                      : "border-emerald-100 hover:border-emerald-300"
                  }`}
                >
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform ${
                      isInternational ? "bg-blue-100 text-blue-700" : "bg-emerald-100 text-emerald-700"
                    }`}
                  >
                    <Brain className="w-6 h-6" />
                  </div>
                  <h3 className="t-card-heading text-slate-900">
                    {isInternational ? "Cross-Border Treaty Assistant" : t(language, "module1Title")}
                  </h3>
                  <p className="t-small text-slate-600 leading-relaxed">
                    {isInternational
                      ? "Source-cited legal analysis grounded in TRIPS Art. 27, Nagoya Protocol ABS, CBD Article 15, US 35 U.S.C. 102, and EPO Art. 54."
                      : t(language, "module1Desc")}
                  </p>
                  <div className="flex flex-wrap gap-2 pt-1">
                    {(isInternational
                      ? ["TRIPS Art. 27", "Nagoya ABS", "EPO Art. 54", "WIPO IGC"]
                      : ["Section 3(p)", "BD Act", "TRIPS", "7 Languages"]
                    ).map((tag) => (
                      <span
                        key={tag}
                        className={`t-label px-2.5 py-1 rounded-full border ${
                          isInternational
                            ? "bg-blue-50 text-blue-700 border-blue-200"
                            : "bg-emerald-50 text-emerald-700 border-emerald-200"
                        }`}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div
                    className={`flex items-center gap-1.5 t-btn pt-2 group-hover:gap-2.5 transition-all ${
                      isInternational ? "text-blue-700" : "text-emerald-700"
                    }`}
                  >
                    <span>{t(language, "module1Btn")}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>

              {/* Card 2 - Product Classifier */}
              <Link href="/classify" className="group">
                <div
                  className={`h-full p-7 rounded-2xl bg-white/95 backdrop-blur-sm border shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1 space-y-4 ${
                    isInternational
                      ? "border-blue-100 hover:border-indigo-300"
                      : "border-emerald-100 hover:border-emerald-300"
                  }`}
                >
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform ${
                      isInternational ? "bg-indigo-100 text-indigo-700" : "bg-amber-50 text-amber-700"
                    }`}
                  >
                    <Scale className="w-6 h-6" />
                  </div>
                  <h3 className="t-card-heading text-slate-900">
                    {isInternational ? "Global ASU Export Classifier" : t(language, "module2Title")}
                  </h3>
                  <p className="t-small text-slate-600 leading-relaxed">
                    {isInternational
                      ? "Export classification under US FDA Botanical Drug Guidance, EU Traditional Herbal Medicinal Products Directive (THMPD), and WHO norms."
                      : t(language, "module2Desc")}
                  </p>
                  <div className="flex flex-wrap gap-2 pt-1">
                    {(isInternational
                      ? ["US FDA Botanical", "EU THMPD", "WHO Norms", "TGA Australia"]
                      : ["D&C Act", "FSSAI", "Schedule T", "Rule 158-B"]
                    ).map((tag) => (
                      <span
                        key={tag}
                        className={`t-label px-2.5 py-1 rounded-full border ${
                          isInternational
                            ? "bg-indigo-50 text-indigo-700 border-indigo-200"
                            : "bg-amber-50 text-amber-700 border-amber-200"
                        }`}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div
                    className={`flex items-center gap-1.5 t-btn pt-2 group-hover:gap-2.5 transition-all ${
                      isInternational ? "text-indigo-700" : "text-emerald-700"
                    }`}
                  >
                    <span>{t(language, "module2Btn")}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>

              {/* Card 3 - Prior-Art Search */}
              <Link href="/search" className="group">
                <div
                  className={`h-full p-7 rounded-2xl bg-white/95 backdrop-blur-sm border shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1 space-y-4 ${
                    isInternational
                      ? "border-blue-100 hover:border-sky-300"
                      : "border-emerald-100 hover:border-emerald-300"
                  }`}
                >
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform ${
                      isInternational ? "bg-sky-100 text-sky-700" : "bg-teal-50 text-teal-700"
                    }`}
                  >
                    <Microscope className="w-6 h-6" />
                  </div>
                  <h3 className="t-card-heading text-slate-900">
                    {isInternational ? "Worldwide Prior-Art & TKDL Search" : t(language, "module3Title")}
                  </h3>
                  <p className="t-small text-slate-600 leading-relaxed">
                    {isInternational
                      ? "Cross-reference formulation ingredients against codified AFI monographs mapped to International Patent Classification (IPC A61K) to block foreign patents."
                      : t(language, "module3Desc")}
                  </p>
                  <div className="flex flex-wrap gap-2 pt-1">
                    {(isInternational
                      ? ["IPC A61K", "TKDL WIPO", "Qdrant Vector", "EPO Third-Party"]
                      : ["AFI Part I", "TKDL", "Qdrant", "Gemini Embed"]
                    ).map((tag) => (
                      <span
                        key={tag}
                        className={`t-label px-2.5 py-1 rounded-full border ${
                          isInternational
                            ? "bg-sky-50 text-sky-700 border-sky-200"
                            : "bg-teal-50 text-teal-700 border-teal-200"
                        }`}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div
                    className={`flex items-center gap-1.5 t-btn pt-2 group-hover:gap-2.5 transition-all ${
                      isInternational ? "text-blue-700" : "text-emerald-700"
                    }`}
                  >
                    <span>{t(language, "module3Btn")}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </section>

        {/* ═══════ WHY US / ABOUT SECTION ═══════ */}
        <section className="relative py-24 bg-white/85 backdrop-blur-md overflow-hidden">
          {/* Decorative ambient background circle */}
          <div
            className={`absolute -left-32 top-1/2 -translate-y-1/2 w-[300px] h-[300px] rounded-full blur-[80px] pointer-events-none transition-colors duration-700 ${
              isInternational ? "bg-blue-100/60" : "bg-emerald-50"
            }`}
          />

          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              {/* Left column - text */}
              <div className="space-y-8">
                <div
                  className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border t-label transition-colors duration-300 ${
                    isInternational
                      ? "bg-blue-50 border-blue-200 text-blue-700"
                      : "bg-emerald-50 border-emerald-200 text-emerald-700"
                  }`}
                >
                  <Shield className="w-3.5 h-3.5" />
                  <span>{isInternational ? "Global Defense & Treaty Compliance" : t(language, "whyUsBadge")}</span>
                </div>

                <h2 className="t-section text-slate-900 leading-tight">
                  {isInternational ? (
                    <>
                      Why International Treaties Matter for{" "}
                      <span className="text-gradient-blue">Traditional Medicine</span>
                    </>
                  ) : (
                    <>
                      {t(language, "whyUsTitlePart1")}{" "}
                      <span className="text-gradient-emerald">{t(language, "whyUsTitleHighlight")}</span>{" "}
                      {t(language, "whyUsTitlePart2")}
                    </>
                  )}
                </h2>

                <p className="t-body text-slate-600 leading-relaxed">
                  {isInternational
                    ? "Foreign patent offices routinely grant patents over traditional Ayurvedic remedies due to lack of accessible vernacular prior art. AYURA bridges classical AFI pharmacopoeial monographs with international treaty mechanisms to safeguard heritage globally."
                    : t(language, "whyUsDesc")}
                </p>

                <div className="space-y-5">
                  {[
                    {
                      icon: <Database className="w-5 h-5" />,
                      title: isInternational ? "Multilateral Treaty Grounding" : t(language, "whyItem1Title"),
                      desc: isInternational
                        ? "Synthesizes TRIPS Art. 27, Nagoya ABS, CBD sovereign rights, and USPTO/EPO rules."
                        : t(language, "whyItem1Desc"),
                    },
                    {
                      icon: <BadgeCheck className="w-5 h-5" />,
                      title: isInternational ? "Preemptive Prior-Art Proofs" : t(language, "whyItem2Title"),
                      desc: isInternational
                        ? "Generates verified citation dossiers formatted for third-party observations before foreign examiners."
                        : t(language, "whyItem2Desc"),
                    },
                    {
                      icon: <Globe className="w-5 h-5" />,
                      title: isInternational ? "Sovereign Benefit Sharing" : t(language, "whyItem3Title"),
                      desc: isInternational
                        ? "Tracks cross-border biological material movement to enforce Nagoya ABS fair returns."
                        : t(language, "whyItem3Desc"),
                    },
                    {
                      icon: <Lock className="w-5 h-5" />,
                      title: isInternational ? "Confidential & Sovereign AI" : t(language, "whyItem4Title"),
                      desc: isInternational
                        ? "Private on-device inference without leaking sensitive proprietary ASU formulation details."
                        : t(language, "whyItem4Desc"),
                    },
                  ].map((item, i) => (
                    <div key={i} className="flex gap-4 group">
                      <div
                        className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 transition-colors ${
                          isInternational
                            ? "bg-blue-100 text-blue-700 group-hover:bg-blue-200"
                            : "bg-emerald-100 text-emerald-700 group-hover:bg-emerald-200"
                        }`}
                      >
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
                <div
                  className={`p-6 rounded-2xl bg-white border shadow-md hover:shadow-lg transition-all duration-300 space-y-3 animate-float-slow ${
                    isInternational ? "border-blue-100" : "border-emerald-100"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        isInternational ? "bg-blue-100 text-blue-700" : "bg-emerald-100 text-emerald-700"
                      }`}
                    >
                      <Zap className="w-4 h-4" />
                    </div>
                    <span className="t-card-heading text-slate-900 text-sm">
                      {isInternational ? "Global Treaty Grounding Pipeline" : t(language, "pipelineTitle")}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap t-label">
                    <span
                      className={`px-2 py-1 rounded-full border ${
                        isInternational
                          ? "bg-blue-50 text-blue-700 border-blue-200"
                          : "bg-emerald-50 text-emerald-700 border-emerald-200"
                      }`}
                    >
                      {isInternational ? "Treaty Query" : t(language, "pipelineQuery")}
                    </span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span
                      className={`px-2 py-1 rounded-full border ${
                        isInternational
                          ? "bg-indigo-50 text-indigo-700 border-indigo-200"
                          : "bg-teal-50 text-teal-700 border-teal-200"
                      }`}
                    >
                      {isInternational ? "IPC A61K Embed" : t(language, "pipelineEmbed")}
                    </span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span
                      className={`px-2 py-1 rounded-full border ${
                        isInternational
                          ? "bg-blue-50 text-blue-700 border-blue-200"
                          : "bg-emerald-50 text-emerald-700 border-emerald-200"
                      }`}
                    >
                      {isInternational ? "Multilingual Search" : t(language, "pipelineSearch")}
                    </span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span
                      className={`px-2 py-1 rounded-full border ${
                        isInternational
                          ? "bg-sky-50 text-sky-700 border-sky-200"
                          : "bg-teal-50 text-teal-700 border-teal-200"
                      }`}
                    >
                      {isInternational ? "Treaty Legal RAG" : t(language, "pipelineGen")}
                    </span>
                    <ArrowRight className="w-3 h-3 text-slate-400" />
                    <span
                      className={`px-2 py-1 rounded-full border ${
                        isInternational
                          ? "bg-blue-100 text-blue-800 border-blue-300"
                          : "bg-emerald-100 text-emerald-800 border-emerald-300"
                      }`}
                    >
                      {isInternational ? "Defense Dossier" : t(language, "pipelineAnswer")}
                    </span>
                  </div>
                </div>

                {/* Card: Corpus Breakdown */}
                <div
                  className={`p-6 rounded-2xl bg-white border shadow-md hover:shadow-lg transition-all duration-300 space-y-4 ${
                    isInternational ? "border-blue-100" : "border-emerald-100"
                  }`}
                  style={{ animationDelay: "1s" }}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        isInternational ? "bg-indigo-50 text-indigo-700" : "bg-amber-50 text-amber-700"
                      }`}
                    >
                      <BookOpen className="w-4 h-4" />
                    </div>
                    <span className="t-card-heading text-slate-900 text-sm">
                      {isInternational ? "Indexed Global Treaties & Legal Corpus" : t(language, "indexedCorpusTitle")}
                    </span>
                  </div>
                  <div className="space-y-2">
                    {(isInternational
                      ? [
                          { label: "TRIPS Agreement (WTO)", count: "14 articles", color: "blue" },
                          { label: "Nagoya Protocol on ABS", count: "8 core articles", color: "indigo" },
                          { label: "Convention on Biological Diversity (CBD)", count: "12 provisions", color: "sky" },
                          { label: "Classical AFI Formulations", count: "15 monographs", color: "blue" },
                          { label: "WIPO IGC & IPC Directives", count: "9 guidelines", color: "indigo" },
                        ]
                      : [
                          { label: "Patents Act, 1970", count: "13 sections", color: "emerald" },
                          { label: "Biological Diversity Act, 2002", count: "6 sections", color: "teal" },
                          { label: "Drugs & Cosmetics Act, 1940", count: "7 provisions", color: "emerald" },
                          { label: "Classical AFI Formulations", count: "15 monographs", color: "amber" },
                          { label: "TRIPS / Nagoya / CBD / PCT", count: "11 articles", color: "teal" },
                        ]
                    ).map((item, i) => (
                      <div key={i} className="flex items-center justify-between t-small">
                        <span className="text-slate-700 font-medium">{item.label}</span>
                        <span
                          className={`t-label px-2.5 py-1 rounded-full border ${
                            isInternational
                              ? "bg-blue-50 text-blue-700 border-blue-200"
                              : "bg-emerald-50 text-emerald-700 border-emerald-200"
                          }`}
                        >
                          {item.count}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Card: Who Is This For */}
                <div
                  className={`p-6 rounded-2xl border shadow-sm space-y-3 transition-colors duration-300 ${
                    isInternational
                      ? "bg-blue-50/70 border-blue-200"
                      : "bg-emerald-50/70 border-emerald-200"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        isInternational ? "bg-blue-200 text-blue-800" : "bg-emerald-200 text-emerald-800"
                      }`}
                    >
                      <Users className="w-4 h-4" />
                    </div>
                    <span
                      className={`t-card-heading text-sm ${
                        isInternational ? "text-blue-950" : "text-emerald-900"
                      }`}
                    >
                      {isInternational ? "Built for Global Stakeholders" : t(language, "builtForTitle")}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2.5">
                    {(isInternational
                      ? [
                          "International Patent Attorneys",
                          "Global Ayush Exporters",
                          "Cross-Border Biotech MSMEs",
                          "WIPO & Diplomatic Delegates",
                          "Academic IP Scholars",
                          "Foreign Regulatory Agents",
                        ]
                      : [
                          "Ayurvedic Researchers",
                          "Traditional Vaidyas",
                          "AYUSH Startups & MSMEs",
                          "Patent Attorneys",
                          "Ministry Regulators",
                          "Drug Licensing Officers",
                        ]
                    ).map((role) => (
                      <div
                        key={role}
                        className={`flex items-center gap-2 t-small font-medium ${
                          isInternational ? "text-blue-900" : "text-emerald-900"
                        }`}
                      >
                        <CheckCircle2
                          className={`w-3.5 h-3.5 shrink-0 ${
                            isInternational ? "text-blue-600" : "text-emerald-600"
                          }`}
                        />
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
        <section
          className={`py-16 text-white transition-all duration-700 ${
            isInternational
              ? "bg-gradient-to-r from-blue-700 via-indigo-700 to-sky-700"
              : "bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700"
          }`}
        >
          <div className="max-w-4xl mx-auto px-4 text-center space-y-6">
            <h2 className="t-section text-white">
              {isInternational
                ? "Deploy Global Treaty Intelligence for Your Formulation"
                : t(language, "ctaBannerTitle")}
            </h2>
            <p
              className={`t-body max-w-xl mx-auto ${
                isInternational ? "text-blue-100" : "text-emerald-100"
              }`}
            >
              {isInternational
                ? "Explore cross-border patent eligibility, Nagoya ABS compliance, and defensive TKDL citation dossier generation in seconds."
                : t(language, "ctaBannerSubtitle")}
            </p>
            <div className="flex flex-wrap items-center justify-center gap-4">
              <Link
                href="/chat"
                className={`group t-btn gap-2 px-7 py-3.5 bg-white rounded-xl shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl cursor-pointer ${
                  isInternational ? "text-blue-900" : "text-emerald-800"
                }`}
              >
                <Sparkles className="w-4 h-4" />
                <span>{t(language, "ctaLaunchAssistant")}</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
              <Link
                href="/search"
                className={`t-btn gap-2 px-7 py-3.5 text-white rounded-xl transition-all hover:-translate-y-0.5 cursor-pointer border ${
                  isInternational
                    ? "bg-blue-800/40 hover:bg-blue-800/60 border-blue-400/30"
                    : "bg-emerald-800/40 hover:bg-emerald-800/60 border-emerald-400/30"
                }`}
              >
                {isInternational ? (
                  <Globe className="w-4 h-4 text-white" />
                ) : (
                  <KhalvaIcon className="w-4 h-4 text-white" />
                )}
                <span>{isInternational ? "Search International Prior-Art" : t(language, "ctaSearchPriorArt")}</span>
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
