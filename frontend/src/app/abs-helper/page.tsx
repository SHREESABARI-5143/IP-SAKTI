'use client';

import React, { useState } from 'react';
import { CheckCircle2, AlertTriangle, ShieldCheck, ArrowRight, FileCheck, HelpCircle, MapPin, Building, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { useAppStore } from '@/lib/store';

export default function ABSHelperPage() {
  const { setEscalationModal } = useAppStore();

  const [formData, setFormData] = useState({
    product_name: 'Premium Ashwagandha Wellness Elixir',
    biological_resources: 'Ashwagandha (Withania somnifera), Red Sandalwood, Tulsi',
    sourcing_location: 'India (Madhya Pradesh & Kerala)',
    user_entity_type: 'Indian Individual/Entity',
    activity_type: 'Commercial Utilization',
    associated_traditional_knowledge: true,
    is_normally_traded_commodity: false,
    is_local_vaid_or_hakim: false,
    is_seeking_ipr: true,
    is_export_involved: false
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAssess = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const bioList = formData.biological_resources.split(',').map((s) => s.trim()).filter(Boolean);
      const res = await api.assessABS({
        ...formData,
        biological_resources: bioList
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
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 text-xs font-bold mb-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          Biodiversity Compliance Engine
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Access and Benefit Sharing (ABS) Compliance Helper
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Evaluate statutory compliance under the Biological Diversity Act 2002 & 2023 Amendment, National Biodiversity Authority (NBA) approval mandates, and Nagoya Protocol treaties.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Form */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Assessment Questionnaire</h2>

          <form onSubmit={handleAssess} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">1. Product / Project Name</label>
              <input
                type="text"
                value={formData.product_name}
                onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">2. Biological Resources Utilized</label>
              <textarea
                rows={2}
                value={formData.biological_resources}
                onChange={(e) => setFormData({ ...formData, biological_resources: e.target.value })}
                placeholder="e.g. Ashwagandha root, Guggulu resin, Tulsi leaves"
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">3. Sourcing Geographical Origin</label>
              <input
                type="text"
                value={formData.sourcing_location}
                onChange={(e) => setFormData({ ...formData, sourcing_location: e.target.value })}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">4. Entity Legal Constitution</label>
              <select
                value={formData.user_entity_type}
                onChange={(e) => setFormData({ ...formData, user_entity_type: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-white focus:outline-none"
              >
                <option value="Indian Individual/Entity">Indian Citizen / 100% Indian Entity</option>
                <option value="Foreign Entity / NRI / Entity with Foreign Participation">Foreign Entity / NRI / Indian Entity with Foreign Shareholding (Sec 3(2))</option>
              </select>
            </div>

            <div className="space-y-2 p-3 bg-slate-50 border border-slate-200 rounded-lg">
              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.is_seeking_ipr}
                  onChange={(e) => setFormData({ ...formData, is_seeking_ipr: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>5. Applying for Intellectual Property Rights (Patent)?</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.is_normally_traded_commodity}
                  onChange={(e) => setFormData({ ...formData, is_normally_traded_commodity: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>6. Listed under Section 40 (Normally Traded Commodities)?</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.is_local_vaid_or_hakim}
                  onChange={(e) => setFormData({ ...formData, is_local_vaid_or_hakim: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>7. Registered Traditional Practitioner (Vaid/Hakim exemption)?</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                <input
                  type="checkbox"
                  checked={formData.is_export_involved}
                  onChange={(e) => setFormData({ ...formData, is_export_involved: e.target.checked })}
                  className="rounded text-teal-600"
                />
                <span>8. Exporting raw botanical resource out of India?</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm"
            >
              <span>{loading ? 'Evaluating ABS Obligations...' : 'Run ABS Assessment'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="lg:col-span-7 space-y-4">
          {result ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
              {/* Top Banner */}
              <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider">ABS Compliance Risk Rating</span>
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-extrabold ${
                    result.risk_level === 'High' || result.risk_level === 'Critical'
                      ? 'bg-rose-600 text-white'
                      : 'bg-emerald-700 text-white'
                  }`}>
                    {result.risk_level} Risk Level
                  </span>
                </div>
                <h2 className="text-lg font-bold text-slate-900 mt-2">
                  Competent Regulatory Authority: {result.jurisdiction_authority}
                </h2>
                <p className="text-xs font-semibold text-emerald-900 mt-1">
                  Benefit Sharing Rate: {result.benefit_sharing_obligation}
                </p>
              </div>

              {/* Statutory Forms Required */}
              <div>
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">Mandatory Statutory Filings</h3>
                <div className="space-y-1.5 text-xs text-slate-800">
                  {result.applicable_forms.map((form: string, idx: number) => (
                    <div key={idx} className="p-3 bg-slate-50 border border-slate-200 rounded-lg flex items-start gap-2.5">
                      <FileCheck className="w-4 h-4 text-teal-600 flex-shrink-0 mt-0.5" />
                      <span className="font-semibold">{form}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Step-by-Step Roadmap */}
              <div>
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">Step-by-Step Compliance Roadmap</h3>
                <ol className="space-y-2 text-xs text-slate-800 list-decimal list-inside bg-slate-50 p-4 rounded-xl border border-slate-200">
                  {result.step_by_step_compliance_roadmap.map((step: string, idx: number) => (
                    <li key={idx} className="leading-relaxed font-medium">
                      <span className="text-slate-900">{step}</span>
                    </li>
                  ))}
                </ol>
              </div>

              {/* Documents to verify */}
              <div>
                <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-1.5">Documents to Keep Ready</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                  {result.documents_to_verify.map((doc: string, idx: number) => (
                    <div key={idx} className="p-2.5 bg-amber-50/50 border border-amber-200 rounded-lg text-slate-700">
                      ✓ {doc}
                    </div>
                  ))}
                </div>
              </div>

              {/* Footer CTA */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <p className="text-[11px] text-slate-500 italic max-w-sm">
                  {result.informational_note}
                </p>
                <button
                  onClick={() => setEscalationModal(true, { productCategory: 'ABS Compliance', question: `ABS assessment review for ${formData.product_name}` })}
                  className="px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-lg shadow-sm"
                >
                  Consult ABS Facilitator
                </button>
              </div>
            </div>
          ) : (
            <div className="h-full min-h-[350px] flex flex-col items-center justify-center p-8 bg-white border border-slate-200 rounded-2xl text-center text-slate-400">
              <CheckCircle2 className="w-12 h-12 text-slate-300 mb-3" />
              <h3 className="text-base font-bold text-slate-700">Awaiting Biological Resource Parameters</h3>
              <p className="text-xs text-slate-500 max-w-sm mt-1">
                Provide details regarding botanical sourcing and click 'Run ABS Assessment' to identify National Biodiversity Authority vs State Biodiversity Board filing requirements.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
