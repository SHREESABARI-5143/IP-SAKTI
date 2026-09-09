'use client';

import React from 'react';
import { X, ExternalLink, BookOpen, Scale, Calendar, CheckCircle2 } from 'lucide-react';
import { useAppStore } from '@/lib/store';

export const SourceDrawer: React.FC = () => {
  const { activeSourceDrawer, setActiveSourceDrawer } = useAppStore();

  if (!activeSourceDrawer) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-lg bg-white shadow-2xl border-l border-slate-200 flex flex-col transform transition-transform duration-300">
      {/* Header */}
      <div className="p-4 bg-slate-900 text-white flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-teal-400" />
          <h3 className="font-semibold text-sm">Authoritative Source Inspector</h3>
        </div>
        <button
          onClick={() => setActiveSourceDrawer(null)}
          className="p-1 text-slate-400 hover:text-white rounded-md hover:bg-slate-800"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Body */}
      <div className="p-6 overflow-y-auto space-y-5 flex-1">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-teal-50 text-teal-800 border border-teal-200 mb-2">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Verified Primary Source
          </div>
          <h2 className="text-lg font-bold text-slate-900 leading-tight">
            {activeSourceDrawer.source_title}
          </h2>
          <p className="text-sm font-medium text-slate-600 mt-1 flex items-center gap-1">
            <Scale className="w-4 h-4 text-teal-600" />
            Authority: {activeSourceDrawer.authority}
          </p>
        </div>

        {activeSourceDrawer.provision_ref && (
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Statutory Provision:</span>
            <p className="text-sm font-semibold text-slate-900 mt-0.5">{activeSourceDrawer.provision_ref}</p>
          </div>
        )}

        <div>
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Official Excerpt:</h4>
          <blockquote className="p-4 bg-amber-50/60 border-l-4 border-amber-500 text-slate-800 text-sm italic rounded-r-lg leading-relaxed">
            "{activeSourceDrawer.quote_text}"
          </blockquote>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-2">
          <div className="p-3 border border-slate-100 bg-slate-50 rounded-lg">
            <span className="text-xs text-slate-500">Version:</span>
            <p className="text-xs font-semibold text-slate-800">{activeSourceDrawer.version || 'Active Gazette'}</p>
          </div>
          <div className="p-3 border border-slate-100 bg-slate-50 rounded-lg">
            <span className="text-xs text-slate-500">Effective Date:</span>
            <p className="text-xs font-semibold text-slate-800">{activeSourceDrawer.effective_date || 'Enacted'}</p>
          </div>
        </div>

        {activeSourceDrawer.source_url && (
          <div className="pt-4 border-t border-slate-200">
            <a
              href={activeSourceDrawer.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-teal-700 hover:bg-teal-800 text-white text-sm font-semibold rounded-lg shadow-sm transition-all"
            >
              <span>View Official Government Registry</span>
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        )}
      </div>
    </div>
  );
};
