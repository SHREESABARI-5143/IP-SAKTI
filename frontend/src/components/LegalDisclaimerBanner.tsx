'use client';

import React from 'react';
import { ShieldCheck } from 'lucide-react';
import { useAppStore } from '@/lib/store';
import { translations } from '@/lib/translations';

export const LegalDisclaimerBanner: React.FC = () => {
  const { language } = useAppStore();
  const t = translations[language] || translations.en;

  return (
    <aside aria-label="Statutory Notice" className="bg-gradient-to-r from-amber-500/10 via-amber-400/5 to-amber-500/10 border-b border-amber-200/60 py-1.5 px-4 text-xs">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-3 text-amber-950/90 font-medium">
        <div className="flex items-center gap-2 overflow-hidden">
          <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-amber-200/70 text-amber-900 font-bold text-[10px] tracking-wide uppercase flex-shrink-0">
            <ShieldCheck className="w-3 h-3 text-amber-800" />
            Statutory Notice
          </span>
          <p className="truncate text-[11px] sm:text-xs text-amber-900/90">
            IP-SAKTI Sahayak provides source-grounded research intelligence. It does <strong className="font-semibold text-amber-950">not</strong> constitute binding legal counsel or formal patent prosecution filings.
          </p>
        </div>
        <div className="hidden md:flex items-center gap-2 flex-shrink-0 text-[10px] text-amber-800/80">
          <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Primary Statutory Grounding Active</span>
        </div>
      </div>
    </aside>
  );
};
