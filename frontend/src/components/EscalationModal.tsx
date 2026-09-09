'use client';

import React, { useState } from 'react';
import { X, Send, UserCheck, ShieldAlert, CheckCircle } from 'lucide-react';
import { useAppStore } from '@/lib/store';
import { api } from '@/lib/api';

export const EscalationModal: React.FC = () => {
  const { isEscalationModalOpen, setEscalationModal, escalationContext, jurisdiction } = useAppStore();

  const [subject, setSubject] = useState(escalationContext?.question?.slice(0, 60) || 'Ayurvedic IP Advisory Request');
  const [email, setEmail] = useState('innovator@ayush-startup.in');
  const [phone, setPhone] = useState('+91 98765 43210');
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  if (!isEscalationModalOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await api.createEscalation({
        subject,
        question: escalationContext?.question || subject,
        jurisdiction,
        product_category: escalationContext?.productCategory || 'Ayurvedic Formulation',
        ai_analysis_summary: escalationContext?.aiAnalysis || 'Initial AI screening completed with primary statutory citations.',
        user_notes: notes,
        contact_email: email,
        contact_phone: phone
      });
      setSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden">
        <div className="p-4 bg-teal-800 text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-teal-300" />
            <h3 className="font-semibold text-sm">Escalate to Certified IP Facilitator</h3>
          </div>
          <button
            onClick={() => {
              setEscalationModal(false);
              setSubmitted(false);
            }}
            className="text-teal-200 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {submitted ? (
          <div className="p-8 text-center space-y-4">
            <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
              <CheckCircle className="w-7 h-7" />
            </div>
            <h3 className="text-lg font-bold text-slate-900">Escalation Request Submitted!</h3>
            <p className="text-sm text-slate-600">
              Your inquiry and AI statutory analysis have been packaged and assigned to an authorized IP Facilitator. You will receive an advisory response at <strong>{email}</strong> within 24-48 hours.
            </p>
            <button
              onClick={() => {
                setEscalationModal(false);
                setSubmitted(false);
              }}
              className="px-5 py-2 bg-teal-700 hover:bg-teal-800 text-white text-sm font-semibold rounded-lg"
            >
              Done
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            <p className="text-xs text-slate-600 leading-relaxed">
              When complex freedom-to-operate (FTO), patent drafting, or State Biodiversity Board filings are required, submit your query to a qualified AYUSH IP facilitator.
            </p>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Subject / Query Title</label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                required
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Contact Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Additional Formulation / Case Notes</label>
              <textarea
                rows={3}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Mention specific concerns regarding traditional knowledge prior art, SBB notice, or commercial targets..."
                className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
              />
            </div>

            <div className="p-3 bg-amber-50 rounded-lg border border-amber-200 text-xs text-amber-800 flex items-start gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" />
              <span>Prior AI analysis and retrieved statutory provisions will be automatically attached to this escalation package.</span>
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setEscalationModal(false)}
                className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 shadow-sm transition-all"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{isSubmitting ? 'Submitting...' : 'Submit Escalation Package'}</span>
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
