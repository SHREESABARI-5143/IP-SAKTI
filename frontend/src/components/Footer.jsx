"use client";

import React from "react";
import { AlertCircle, Leaf, ExternalLink } from "lucide-react";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

export const Footer = () => {
  const { language } = useApp();
  return (
    <footer className="w-full border-t border-emerald-100 bg-white py-6 px-3 sm:px-6 text-xs text-slate-500">
      <div className="w-full flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-[#fcf9f2] p-0.5 border border-emerald-200/80 flex items-center justify-center shadow-2xs overflow-hidden">
            <img src="/ayura_logo.png" alt="AYURA Logo" className="w-full h-full object-contain" />
          </div>
          <span className="font-semibold text-slate-800">
            AYURA (IP-SAKTI)
          </span>
          <span className="text-slate-400">|</span>
          <span>{t(language, "ministrySubtitle")}</span>
        </div>

        <div className="flex items-center gap-4 text-xs text-slate-600">
          <a
            href="https://main.ayush.gov.in/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-emerald-700 flex items-center gap-1"
          >
            Ministry of Ayush <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
          <a
            href="https://www.tkdl.res.in/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-emerald-700 flex items-center gap-1"
          >
            TKDL India <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
          <a
            href="https://ipindia.gov.in/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-emerald-700 flex items-center gap-1"
          >
            IPO India <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
        </div>

        <div className="flex items-center gap-1.5 text-[11px] text-slate-500 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-100">
          <AlertCircle className="w-3 h-3 text-emerald-600 shrink-0" />
          <span>Statutory intelligence tool. Consult qualified patent attorney for filings.</span>
        </div>
      </div>
    </footer>
  );
};
