'use client';

import React, { useState } from 'react';
import { 
  FileText, 
  ShieldCheck, 
  AlertTriangle, 
  ArrowRight, 
  Sparkles, 
  Clock, 
  Tag, 
  Layers, 
  CheckCircle,
  HelpCircle
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAppStore } from '@/lib/store';

export default function IPStrategyPage() {
  const { setEscalationModal } = useAppStore();

  const [formData, setFormData] = useState({
    product_name: 'AyurShield Bio-Enhanced Extract',
    product_description: 'Proprietary curcumin and withanolide formulation with improved bioavailability',
    ingredients: 'Curcuma longa (95% curcuminoids), Withania somnifera, Piperine extract',
    is_classical_formulation: false,
    novel_extraction_or_synergy: true,
    has_unique_brand_name: true,
    brand_name: 'AyurShield Ultra',
    has_distinct_packaging_or_bottle: true,
    uses_indigenous_crop_variety: false,
    is_proprietary_process: true,
    target_jurisdiction: 'India'
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleEvaluate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const ingList = formData.ingredients.split(',').map((s) => s.trim()).filter(Boolean);
      const res = await api.assessIPStrategy({
        ...formData,
        ingredients: ingList
      });
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 pb-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 text-blue-800 text-xs font-bold mb-2">
          <FileText className="w-4 h-4 text-blue-600" />
          Multi-Route IP Strategy Matrix
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Intellectual Property Protection Route Matrix
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Evaluate patent eligibility, Section 3(p) TK barriers, trademark classes, GI tags, trade secrets, and plant variety protection.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Form */}
        <div className="lg:col-span-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Product Innovation Data</h2>

          <form onSubmit={handleEvaluate} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Product / Brand Name</label>
              <input
                type="text"
                value={formData.product_name}
                onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Brief Description of Innovation</label>
              <textarea
                rows={2}
                value={formData.product_description}
                onChange={(e) => setFormData({ ...formData, product_description: e.target.value })}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Ingredients Used</label>
              <textarea
                rows={2}
                value={formData.ingredients}
                onChange={(e) => setFormData({ ...formData, ingredients: e.target.value })}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div className="space-y-2 p-3 bg-slate-50 border border-slate-200 rounded-lg">
              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.novel_extraction_or_synergy}
                  onChange={(e) => setFormData({ ...formData, novel_extraction_or_synergy: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>Demonstrable Synergistic Efficacy</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.is_proprietary_process}
                  onChange={(e) => setFormData({ ...formData, is_proprietary_process: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>Novel Process / Extraction Method</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.is_classical_formulation}
                  onChange={(e) => setFormData({ ...formData, is_classical_formulation: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>Exact Classical Ayurvedic Recipe</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm"
            >
              <span>{loading ? 'Evaluating Matrix...' : 'Generate IP Strategy'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="lg:col-span-8 space-y-4">
          {result ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
              {/* Executive Summary */}
              <div className="p-4 bg-slate-900 text-white rounded-xl space-y-1">
                <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider">Executive Strategy</span>
                <p className="text-xs leading-relaxed font-medium">
                  {result.overall_executive_summary}
                </p>
              </div>

              {/* IP Routes Grid */}
              <div className="space-y-3">
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider">Evaluated IP Protection Routes</h3>
                <div className="space-y-2.5">
                  {result.routes.map((route: any, idx: number) => {
                    const isHigh = route.relevance_level.includes('Highly') || route.relevance_level.includes('Potentially');
                    return (
                      <div key={idx} className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-bold text-slate-900">{route.route_name}</h4>
                          <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                            isHigh ? 'bg-teal-100 text-teal-800' : 'bg-slate-200 text-slate-700'
                          }`}>
                            {route.relevance_level}
                          </span>
                        </div>
                        <p className="text-xs text-slate-700 leading-relaxed">{route.analysis_details}</p>
                        <div className="text-[11px] text-slate-500 font-mono">
                          Statutory Basis: {route.statutory_basis}
                        </div>
                        {route.action_items && route.action_items.length > 0 && (
                          <div className="pt-2 border-t border-slate-200 space-y-1 text-xs">
                            <span className="font-semibold text-slate-800">Action Plan:</span>
                            {route.action_items.map((act: string, aIdx: number) => (
                              <p key={aIdx} className="text-slate-600 flex items-start gap-1.5">
                                • {act}
                              </p>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Estimated Timelines & Costs */}
              <div>
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-teal-700" />
                  Statutory Filings & Fee Estimates
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  {result.timeline_and_cost_guidelines.map((item: any, idx: number) => (
                    <div key={idx} className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
                      <p className="font-bold text-slate-800">{item.milestone}</p>
                      <div className="flex justify-between text-[11px] text-slate-600 mt-1">
                        <span>Timeline: {item.timeline}</span>
                        <span className="font-semibold text-teal-800">{item.estimated_official_fee}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Footer */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <p className="text-[11px] text-slate-500 italic max-w-sm">
                  {result.disclaimer}
                </p>
                <button
                  onClick={() => setEscalationModal(true, { productCategory: 'IP Strategy Matrix', question: `IP portfolio assessment for ${formData.product_name}` })}
                  className="px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-lg shadow-sm"
                >
                  Consult Patent Attorney
                </button>
              </div>
            </div>
          ) : (
            <div className="h-full min-h-[350px] flex flex-col items-center justify-center p-8 bg-white border border-slate-200 rounded-2xl text-center text-slate-400">
              <FileText className="w-12 h-12 text-slate-300 mb-3" />
              <h3 className="text-base font-bold text-slate-700">Awaiting Product Strategy Inputs</h3>
              <p className="text-xs text-slate-500 max-w-sm mt-1">
                Enter product details to map out complete multi-route protection across Patents, Trademarks, Trade Secrets, and GI tags.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
