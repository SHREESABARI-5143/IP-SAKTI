"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Shield, Sparkles, FileText, Search, Leaf } from "lucide-react";
import { JurisdictionSwitch } from "./JurisdictionSwitch";
import { LanguageSelector, SupportedLanguage } from "./LanguageSelector";

interface NavbarProps {
  jurisdiction: "india" | "international" | "both";
  onJurisdictionChange: (j: "india" | "international" | "both") => void;
  language: SupportedLanguage;
  onLanguageChange: (lang: SupportedLanguage) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  jurisdiction,
  onJurisdictionChange,
  language,
  onLanguageChange,
}) => {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-emerald-100 bg-white/90 backdrop-blur-md shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 p-0.5 flex items-center justify-center shadow-md shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-white rounded-[10px] flex items-center justify-center">
              <Leaf className="w-4 h-4 text-emerald-600" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-lg tracking-tight text-slate-900 font-manrope">
                AYURA
              </span>
              <span className="t-label px-2 py-0.5 bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-full">
                IP-SAKTI
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium">
              Ministry of Ayush Legal & IP Intelligence
            </p>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-6 text-slate-600">
          <Link
            href="/chat"
            className={`t-nav flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
              pathname === "/chat"
                ? "bg-emerald-50 text-emerald-800 font-semibold border border-emerald-200"
                : "hover:text-emerald-700 hover:bg-emerald-50/50"
            }`}
          >
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>AI Legal Assistant</span>
          </Link>

          <Link
            href="/classify"
            className={`t-nav flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
              pathname === "/classify"
                ? "bg-emerald-50 text-emerald-800 font-semibold border border-emerald-200"
                : "hover:text-emerald-700 hover:bg-emerald-50/50"
            }`}
          >
            <FileText className="w-4 h-4 text-emerald-600" />
            <span>Product Classifier</span>
          </Link>

          <Link
            href="/search"
            className={`t-nav flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors ${
              pathname === "/search"
                ? "bg-emerald-50 text-emerald-800 font-semibold border border-emerald-200"
                : "hover:text-emerald-700 hover:bg-emerald-50/50"
            }`}
          >
            <Search className="w-4 h-4 text-emerald-600" />
            <span>Prior-Art Lookup</span>
          </Link>
        </nav>

        {/* Controls */}
        <div className="flex items-center gap-3">
          <JurisdictionSwitch
            jurisdiction={jurisdiction}
            onChange={onJurisdictionChange}
          />
          <LanguageSelector
            language={language}
            onChange={onLanguageChange}
          />
        </div>
      </div>
    </header>
  );
};
