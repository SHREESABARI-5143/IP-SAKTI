"use client";

import React from "react";
import { AlertCircle, Leaf, ExternalLink } from "lucide-react";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

export const Footer = () => {
  const { language, jurisdiction } = useApp();
  const isInternational = jurisdiction === "international";

  return (
    <footer className="w-full border-t border-slate-200 bg-slate-900 text-slate-100 py-6 px-4 sm:px-8 text-xs shadow-inner transition-colors duration-300">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Brand & Subtitle */}
        <div className="flex flex-wrap items-center justify-center md:justify-start gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-white p-0.5 border border-emerald-400 flex items-center justify-center shadow-xs overflow-hidden shrink-0">
            <img src="/ayura_logo.png" alt="AYURA Logo" className="w-full h-full object-contain" />
          </div>
          <span className="font-bold text-white tracking-tight text-sm">
            AYURA (IP-SAKTI)
          </span>
          <span className="text-slate-400 font-normal hidden sm:inline">•</span>
          <span className="text-slate-300 font-medium text-xs">
            {t(language, "ministrySubtitle")}
          </span>
        </div>

        {/* Statutory Links */}
        <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-6 text-xs font-semibold text-slate-200">
          <a
            href="https://main.ayush.gov.in/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-emerald-400 transition-colors flex items-center gap-1.5 py-1 px-2 rounded-md hover:bg-slate-800/80"
          >
            <span>Ministry of Ayush</span>
            <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
          </a>
          <a
            href="https://www.tkdl.res.in/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-emerald-400 transition-colors flex items-center gap-1.5 py-1 px-2 rounded-md hover:bg-slate-800/80"
          >
            <span>TKDL India</span>
            <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
          </a>
          <a
            href="https://ipindia.gov.in/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-emerald-400 transition-colors flex items-center gap-1.5 py-1 px-2 rounded-md hover:bg-slate-800/80"
          >
            <span>IPO India</span>
            <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
          </a>
          {isInternational && (
            <a
              href="https://www.wipo.int/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-400 transition-colors flex items-center gap-1.5 py-1 px-2 rounded-md hover:bg-slate-800/80"
            >
              <span>WIPO</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
            </a>
          )}
        </div>

        {/* Statutory Disclaimer Pill */}
        <div className="flex items-center gap-2 text-[11px] font-medium text-emerald-300 bg-emerald-950/80 px-3.5 py-1.5 rounded-full border border-emerald-700/60 shadow-xs">
          <AlertCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
          <span className="text-slate-200">Statutory intelligence tool. Consult qualified patent attorney for filings.</span>
        </div>
      </div>
    </footer>
  );
};
