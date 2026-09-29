"use client";

import React from "react";
import { AlertCircle, Leaf, ExternalLink } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="w-full border-t border-emerald-100 bg-white py-8 px-4 text-xs text-slate-500">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-emerald-100 flex items-center justify-center text-emerald-700">
            <Leaf className="w-3.5 h-3.5" />
          </div>
          <span className="font-semibold text-slate-800">
            AYURA (IP-SAKTI Sahayak)
          </span>
          <span className="text-slate-400">|</span>
          <span>Ministry of Ayush Regulatory & IP Intelligence</span>
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
