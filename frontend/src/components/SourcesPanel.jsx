"use client";

import React from "react";
import { X, BookOpen, ShieldCheck } from "lucide-react";

export const SourcesPanel = ({
  isOpen,
  onClose,
  sources = [],
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/30 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-md bg-white border-l border-emerald-100 h-full flex flex-col shadow-2xl animate-in slide-in-from-right duration-300">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-emerald-100 bg-emerald-50/60">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-700" />
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              Legal Corpus Citations ({sources.length})
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-emerald-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white">
          {sources.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-sm">
              No specific legal sources retrieved for this turn.
            </div>
          ) : (
            sources.map((src, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl space-y-2 bg-white border border-emerald-100 hover:border-emerald-300 shadow-sm hover:shadow-md transition"
              >
                <div className="flex items-center justify-between">
                  <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <ShieldCheck className="w-3 h-3" />
                    {src.jurisdiction?.toUpperCase()} JURISDICTION
                  </span>
                  <span className="text-[11px] text-slate-400 font-mono font-semibold">
                    Match: {Math.round((src.relevance_score || 0) * 100)}%
                  </span>
                </div>

                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">{src.doc_title}</h4>
                    <div className="text-xs font-semibold text-emerald-700">{src.section_title}</div>
                  </div>
                  {src.url && (
                    <a
                      href={src.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-2.5 py-1 text-[11px] font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 rounded-lg transition shrink-0"
                    >
                      Official Gazette / Act ↗
                    </a>
                  )}
                </div>

                {src.effective_date && (
                  <div className="text-[11px] text-slate-500 font-medium">
                    📅 Effective: <span className="text-slate-700">{src.effective_date}</span>
                  </div>
                )}

                <blockquote className="text-xs text-slate-600 bg-emerald-50/60 p-3 rounded-lg border-l-2 border-emerald-400 italic leading-relaxed">
                  &quot;{src.excerpt}&quot;
                </blockquote>

                <div className="pt-1 text-[11px] text-slate-400 flex items-center justify-between">
                  <div>Citation Key: <span className="font-mono text-emerald-700">{src.citation_key}</span></div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-emerald-100 text-[11px] text-slate-500 bg-emerald-50/40">
          Source references extracted directly from the Ministry of Ayush & IP India statutory index.
        </div>
      </div>
    </div>
  );
};
