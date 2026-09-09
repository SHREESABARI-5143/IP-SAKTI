'use client';

import React, { useState, useEffect } from 'react';
import { Database, ExternalLink, ShieldCheck, CheckCircle2, Clock, Scale, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';

export default function SourcesPage() {
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('All');

  const fetchSources = async () => {
    setLoading(true);
    try {
      const data = await api.getSources(
        selectedJurisdiction !== 'All' ? { jurisdiction: selectedJurisdiction } : undefined
      );
      setSources(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSources();
  }, [selectedJurisdiction]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-bold mb-2">
            <Database className="w-4 h-4 text-teal-600" />
            Verified Statutory Registry
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Authoritative Legal & Regulatory Source Explorer
          </h1>
          <p className="text-sm text-slate-600 mt-1">
            Browse all primary legislation, government notifications, official pharmacopoeias, and international treaties indexed in IP-SAKTI Sahayak.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
          {['All', 'India', 'International', 'USA', 'EU'].map((j) => (
            <button
              key={j}
              onClick={() => setSelectedJurisdiction(j)}
              className={`px-3 py-1.5 font-bold rounded-lg transition-all ${
                selectedJurisdiction === j
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {j}
            </button>
          ))}
        </div>
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="p-12 text-center text-xs text-slate-500">Loading statutory sources...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sources.map((src) => (
            <div
              key={src.id}
              className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded-md text-[10px] font-bold bg-teal-50 text-teal-800 border border-teal-200 uppercase">
                    {src.jurisdiction} • {src.domain}
                  </span>
                  <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-700">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Rank #{src.authority_rank} Primary</span>
                  </div>
                </div>

                <h3 className="text-base font-bold text-slate-900 mt-2.5 leading-snug">
                  {src.name}
                </h3>

                <div className="mt-3 space-y-1.5 text-xs text-slate-600">
                  <p className="flex items-center gap-1.5">
                    <Scale className="w-3.5 h-3.5 text-teal-600 flex-shrink-0" />
                    <span>Authority: <strong>{src.authority}</strong></span>
                  </p>
                  <p className="flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-teal-600 flex-shrink-0" />
                    <span>Type: <strong>{src.source_type}</strong></span>
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                <div className="flex items-center gap-1 text-[11px] text-slate-500">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  <span>Verified Active</span>
                </div>

                {src.source_url && (
                  <a
                    href={src.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs font-bold text-teal-700 hover:text-teal-800"
                  >
                    <span>Official Gazette</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
