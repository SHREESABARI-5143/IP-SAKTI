'use client';

import React, { useState } from 'react';
import { Layers, CheckCircle, AlertTriangle, ShieldCheck, ArrowRight, HelpCircle, FileText } from 'lucide-react';
import { api } from '@/lib/api';
import { useAppStore } from '@/lib/store';

export default function ClassifyPage() {
  const { setEscalationModal } = useAppStore();

  const [formData, setFormData] = useState({
    product_name: 'AyurJoint Mobility Vati',
    product_type_hint: 'Classical Formulation',
    ingredients: 'Ashwagandha, Shallaki (Boswellia serrata), Nirgundi, Guggulu',
    has_classical_text_reference: true,
    classical_text_name: 'Bhaishajya Ratnavali / Ayurvedic Formulary of India (AFI)',
    is_modified_or_extract: false,
    novel_processing_method: false,
    intended_use_or_claims: 'Relieves joint inflammation and supports bone wellness',
    dosage_form: 'Vati / Tablet',
    biological_sources_origin: 'India',
    target_market: 'India'
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleClassify = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const ingList = formData.ingredients.split(',').map((s) => s.trim()).filter(Boolean);
      const res = await api.classifyProduct({
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
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-bold mb-2">
          <Layers className="w-4 h-4 text-teal-600" />
          Regulatory Decision Engine
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Ayurvedic Formulation Classification Engine
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Accurately classify herbal formulations across Drugs & Cosmetics Act 1940 (Rule 158B), FSSAI Ayurveda Aahar 2022, Phytopharmaceuticals, and Cosmetics.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Input Form */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Product Parameters</h2>

          <form onSubmit={handleClassify} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Product Formulation Name</label>
              <input
                type="text"
                value={formData.product_name}
                onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Ingredients (Comma separated)</label>
              <textarea
                rows={2}
                value={formData.ingredients}
                onChange={(e) => setFormData({ ...formData, ingredients: e.target.value })}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-2">
              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.has_classical_text_reference}
                  onChange={(e) => setFormData({ ...formData, has_classical_text_reference: e.target.checked })}
                  className="rounded text-teal-600 focus:ring-teal-500"
                />
                <span>Reference text in First Schedule (Samhita / AFI)?</span>
              </label>

              {formData.has_classical_text_reference && (
                <div>
                  <label className="block font-medium text-slate-600 mb-0.5">Authoritative Text Citation</label>
                  <input
                    type="text"
                    value={formData.classical_text_name}
                    onChange={(e) => setFormData({ ...formData, classical_text_name: e.target.value })}
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-md focus:outline-none"
                  />
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-2">
              <label className="flex items-center gap-2 p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-medium text-slate-700">
                <input
                  type="checkbox"
                  checked={formData.is_modified_or_extract}
                  onChange={(e) => setFormData({ ...formData, is_modified_or_extract: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>Modified / Novel Extract</span>
              </label>

              <label className="flex items-center gap-2 p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-medium text-slate-700">
                <input
                  type="checkbox"
                  checked={formData.novel_processing_method}
                  onChange={(e) => setFormData({ ...formData, novel_processing_method: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>Novel Process</span>
              </label>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Intended Claims & Purpose</label>
              <textarea
                rows={2}
                value={formData.intended_use_or_claims}
                onChange={(e) => setFormData({ ...formData, intended_use_or_claims: e.target.value })}
                placeholder="Describe if intended for disease therapy, food wellness, or external cosmetic use..."
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Dosage Form</label>
              <select
                value={formData.dosage_form}
                onChange={(e) => setFormData({ ...formData, dosage_form: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-white focus:outline-none"
              >
                <option value="Vati / Tablet">Vati / Tablet</option>
                <option value="Asava / Arishta">Asava / Arishta (Fermented)</option>
                <option value="Churna / Powder">Churna / Powder</option>
                <option value="Taila / Ghrita (Medicated Oil/Ghee)">Taila / Ghrita</option>
                <option value="Standardized Botanical Extract Capsule">Standardized Botanical Extract Capsule</option>
                <option value="Ayurveda Aahar Health Drink / Food Bar">Ayurveda Aahar Health Drink / Food Bar</option>
                <option value="Topical Cream / Hair Oil (Cosmetic)">Topical Cream / Hair Oil (Cosmetic)</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm"
            >
              <span>{loading ? 'Evaluating Classification...' : 'Classify Formulation'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-7 space-y-4">
          {result ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
              {/* Top Banner */}
              <div className="p-4 bg-teal-50 border border-teal-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-teal-800 uppercase tracking-wider">Classification Outcome</span>
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-teal-700 text-white">
                    Confidence: {result.confidence} ({Math.round(result.confidence_score * 100)}%)
                  </span>
                </div>
                <h2 className="text-xl font-bold text-slate-900 mt-2">
                  {result.likely_category}
                </h2>
                <p className="text-xs font-semibold text-teal-900 mt-1">
                  Statutory Governance: {result.statutory_governance}
                </p>
              </div>

              {/* Why Explanation */}
              <div>
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-1">Rationale</h3>
                <p className="text-xs text-slate-800 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200">
                  {result.why_explanation}
                </p>
              </div>

              {/* Licensing Requirements */}
              <div>
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">Licensing & Regulatory Pathways</h3>
                <ul className="space-y-1.5 text-xs text-slate-800">
                  {result.licensing_requirements.map((req: string, idx: number) => (
                    <li key={idx} className="flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-teal-600 flex-shrink-0 mt-0.5" />
                      <span>{req}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* IP & ABS Considerations */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                <div className="p-3.5 bg-amber-50/60 border border-amber-200 rounded-xl space-y-1">
                  <h4 className="font-bold text-amber-900 flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-amber-700" />
                    Traditional Knowledge / IP
                  </h4>
                  <p className="text-slate-700 text-[11px] leading-relaxed">{result.traditional_knowledge_concerns}</p>
                </div>

                <div className="p-3.5 bg-blue-50/60 border border-blue-200 rounded-xl space-y-1">
                  <h4 className="font-bold text-blue-900 flex items-center gap-1.5">
                    <FileText className="w-4 h-4 text-blue-700" />
                    ABS / Biodiversity
                  </h4>
                  <p className="text-slate-700 text-[11px] leading-relaxed">{result.abs_considerations}</p>
                </div>
              </div>

              {/* Mandatory Labeling Rules */}
              <div>
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-1.5">Mandatory Labeling Requirements</h3>
                <div className="flex flex-wrap gap-1.5">
                  {result.mandatory_labeling_rules.map((rule: string, idx: number) => (
                    <span key={idx} className="px-2.5 py-1 bg-slate-100 border border-slate-200 rounded-md text-[11px] font-semibold text-slate-800">
                      {rule}
                    </span>
                  ))}
                </div>
              </div>

              {/* Facilitator CTA */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <p className="text-[11px] text-slate-500 italic max-w-sm">
                  {result.important_caveat}
                </p>
                <button
                  onClick={() => setEscalationModal(true, { productCategory: result.likely_category, question: `Classification guidance for ${formData.product_name}` })}
                  className="px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-lg shadow-sm"
                >
                  Consult IP Facilitator
                </button>
              </div>
            </div>
          ) : (
            <div className="h-full min-h-[350px] flex flex-col items-center justify-center p-8 bg-white border border-slate-200 rounded-2xl text-center text-slate-400">
              <Layers className="w-12 h-12 text-slate-300 mb-3" />
              <h3 className="text-base font-bold text-slate-700">Awaiting Product Inputs</h3>
              <p className="text-xs text-slate-500 max-w-sm mt-1">
                Fill in the product formulation details on the left and click 'Classify Formulation' to trigger the statutory decision tree.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
