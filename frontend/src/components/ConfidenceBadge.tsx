'use client';

import React, { useState } from 'react';
import { ShieldCheck, AlertTriangle, HelpCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { Confidence } from '@/lib/store';

interface Props {
  confidence?: Confidence;
}

export const ConfidenceBadge: React.FC<Props> = ({ confidence }) => {
  const [expanded, setExpanded] = useState(false);

  if (!confidence) return null;

  const isHigh = confidence.level === 'High';
  const isMed = confidence.level === 'Medium';
  const isLow = confidence.level === 'Low';
  const isAbstain = confidence.level === 'Abstain';

  const badgeBg = isHigh
    ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
    : isMed
    ? 'bg-amber-50 text-amber-800 border-amber-200'
    : isLow
    ? 'bg-orange-50 text-orange-800 border-orange-200'
    : 'bg-rose-50 text-rose-800 border-rose-200';

  return (
    <div className="inline-block my-2">
      <div
        onClick={() => setExpanded(!expanded)}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-md border text-xs font-medium cursor-pointer transition-all ${badgeBg}`}
      >
        <ShieldCheck className="w-4 h-4" />
        <span>Confidence: <strong>{confidence.level}</strong> ({Math.round(confidence.score * 100)}%)</span>
        {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </div>

      {expanded && (
        <div className="mt-2 p-3 bg-white border border-slate-200 rounded-lg shadow-md text-xs text-slate-700 max-w-md space-y-2">
          <p className="font-semibold text-slate-900">{confidence.explanation}</p>
          <div className="space-y-1.5 pt-1 border-t border-slate-100">
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Source Authority Hierarchy:</span>
              <span className="font-semibold text-slate-800">{Math.round(confidence.source_authority_score * 100)}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Semantic Relevance:</span>
              <span className="font-semibold text-slate-800">{Math.round(confidence.retrieval_relevance_score * 100)}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Jurisdictional Precision:</span>
              <span className="font-semibold text-slate-800">{Math.round(confidence.jurisdiction_match_score * 100)}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Citation Grounding:</span>
              <span className="font-semibold text-slate-800">{Math.round(confidence.citation_grounding_score * 100)}%</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
