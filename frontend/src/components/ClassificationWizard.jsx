"use client";

import React, { useState, useEffect } from "react";
import {
  startClassification,
  submitClassificationAnswer,
  getPathwayRecommendation,
} from "@/lib/api";
import {
  CheckCircle2,
  ArrowRight,
  RotateCcw,
  ShieldCheck,
  Layers,
  FileCheck,
  Scale,
} from "lucide-react";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

export const ClassificationWizard = ({ language }) => {
  const { addClassificationHistory } = useApp();
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [result, setResult] = useState(null);
  const [pathwayData, setPathwayData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [stepCount, setStepCount] = useState(1);
  const [sessionId] = useState(() => `sess_${Date.now()}`);

  const loadStartQuestion = async () => {
    setLoading(true);
    setResult(null);
    setPathwayData(null);
    setStepCount(1);
    try {
      const q = await startClassification();
      setCurrentQuestion(q);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStartQuestion();
  }, []);

  const handleOptionSelect = async (optionId) => {
    if (!currentQuestion) return;
    setLoading(true);
    try {
      const res = await submitClassificationAnswer(sessionId, currentQuestion.question_id, optionId);
      if (res && "category" in res) {
        setResult(res);
        setCurrentQuestion(null);
        if (addClassificationHistory) {
          addClassificationHistory({
            category: res.category,
            category_name_en: res.category_name_en,
            category_name_hi: res.category_name_hi,
            confidence: res.confidence,
          });
        }
        const pw = await getPathwayRecommendation(res.category);
        setPathwayData(pw);
      } else {
        setCurrentQuestion(res);
        setStepCount((prev) => prev + 1);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">

      {/* Header */}
      <div className="bg-white/95 backdrop-blur-xs border border-emerald-100/90 shadow-sm p-6 sm:p-7 rounded-2xl space-y-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200/80 flex items-center justify-center shadow-2xs">
            <Scale className="w-5 h-5 text-amber-600" />
          </div>
          <div>
            <h2 className="t-subheading text-slate-900">
              {t(language, "classifyHeaderTitle")}
            </h2>
            <p className="t-small text-slate-500">{t(language, "classifyHeaderSubtitle")}</p>
          </div>
        </div>
        <p className="t-body text-slate-600 max-w-2xl leading-relaxed">
          {t(language, "classifyHeaderDesc")}
        </p>
      </div>

      {/* Loading state */}
      {loading ? (
        <div className="bg-white border border-emerald-100 shadow-md p-12 rounded-2xl text-center space-y-4">
          <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-semibold text-slate-500">
            {t(language, "classifyEvaluating")}
          </p>
        </div>

      ) : result ? (
        /* ── Result Card ── */
        <div className="space-y-6 animate-in fade-in duration-300">
          <div className="bg-white p-6 sm:p-8 rounded-2xl border-2 border-emerald-300 shadow-xl relative overflow-hidden">
            {/* Decorative gradient blob */}
            <div className="absolute -top-12 -right-12 w-40 h-40 bg-emerald-100 rounded-full blur-3xl pointer-events-none" />

            <div className="flex items-center justify-between border-b border-emerald-100 pb-4 mb-6">
              <div>
                <span className="t-label tracking-wider text-emerald-600 uppercase">
                  {t(language, "classifyResultTitle")}
                </span>
                <h3 className="t-subheading text-slate-900 mt-1">
                  {language === "hi" ? result.category_name_hi : result.category_name_en}
                </h3>
              </div>
              <span className="px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full t-label flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                {t(language, "confidenceLabel")} {result.confidence}
              </span>
            </div>

            <div className="space-y-4">
              {/* Legal rationale */}
              <div>
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
                  {t(language, "legalRationale")}
                </h4>
                <p className="text-xs text-slate-700 bg-emerald-50/60 p-3.5 rounded-xl border border-emerald-100 leading-relaxed">
                  {result.reasoning}
                </p>
              </div>

              <div className="grid sm:grid-cols-2 gap-4 pt-2">
                {/* Statutory basis */}
                <div className="bg-amber-50 p-4 rounded-xl border border-amber-200 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-amber-700">
                    <ShieldCheck className="w-4 h-4" />
                    <span>{t(language, "statutoryBasis")}</span>
                  </div>
                  <ul className="text-xs text-slate-700 space-y-1">
                    {result.cited_rules?.map((rule, idx) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="text-amber-600">•</span>
                        <span>{rule}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* IP protection */}
                <div className="bg-emerald-50 p-4 rounded-xl border border-emerald-200 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-emerald-700">
                    <Layers className="w-4 h-4" />
                    <span>{t(language, "availableIpProtection")}</span>
                  </div>
                  <ul className="text-xs text-slate-700 space-y-1">
                    {result.applicable_ip_instruments?.map((ip, idx) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="text-emerald-600">•</span>
                        <span>{ip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Licensing & next steps */}
              <div className="bg-white p-4 rounded-xl border border-slate-200 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-teal-700">
                  <FileCheck className="w-4 h-4" />
                  <span>{t(language, "mandatoryLicensing")}</span>
                </div>
                <div className="grid sm:grid-cols-2 gap-2 text-xs text-slate-700 pt-1">
                  <div>
                    <span className="font-semibold text-slate-500 block mb-1">{t(language, "licencesNeeded")}</span>
                    {result.regulatory_implications?.map((imp, idx) => (
                      <div key={idx} className="mb-1 text-emerald-700 font-medium">✓ {imp}</div>
                    ))}
                  </div>
                  <div>
                    <span className="font-semibold text-slate-500 block mb-1">{t(language, "actionItems")}</span>
                    {result.next_steps?.map((st, idx) => (
                      <div key={idx} className="mb-1 text-teal-700 font-medium">➔ {st}</div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Restart */}
            <div className="pt-6 flex justify-end">
              <button
                onClick={loadStartQuestion}
                className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-xs font-semibold rounded-xl transition text-slate-700 border border-slate-200 cursor-pointer"
              >
                <RotateCcw className="w-4 h-4" />
                <span>{t(language, "classifyAnother")}</span>
              </button>
            </div>
          </div>
        </div>

      ) : (
        /* ── Wizard Question ── */
        currentQuestion && (
          <div className="bg-white border border-emerald-100 shadow-md p-6 sm:p-8 rounded-2xl space-y-6 animate-in fade-in duration-200">
            {/* Step counter */}
            <div className="flex items-center justify-between text-xs font-semibold text-slate-500 border-b border-emerald-50 pb-3">
              <span className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                {t(language, "stepCountLabel", { step: stepCount })}
              </span>
              <span className="text-amber-600 font-bold">{t(language, "ayushRegulatoryEngine")}</span>
            </div>

            {/* Question text */}
            <div className="space-y-2">
              <h3 className="t-card-heading text-slate-900 leading-snug">
                {language === "hi" ? currentQuestion.title_hi : currentQuestion.title_en}
              </h3>
              {(currentQuestion.description_en || currentQuestion.description_hi) && (
                <p className="t-small text-slate-600 leading-relaxed bg-emerald-50/60 p-3 rounded-lg border border-emerald-100">
                  {language === "hi" ? currentQuestion.description_hi : currentQuestion.description_en}
                </p>
              )}
            </div>

            {/* Option cards */}
            <div className="space-y-3 pt-2">
              {currentQuestion.options?.map((opt) => (
                <button
                  key={opt.id}
                  onClick={() => handleOptionSelect(opt.id)}
                  className="w-full text-left p-4 rounded-xl bg-white border border-emerald-100 hover:border-emerald-400 hover:bg-emerald-50/40 hover:shadow-md flex items-center justify-between group transition-all duration-200"
                >
                  <span className="t-small font-medium text-slate-700 group-hover:text-emerald-800">
                    {language === "hi" ? opt.label_hi : opt.label_en}
                  </span>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-transform" />
                </button>
              ))}
            </div>
          </div>
        )
      )}
    </div>
  );
};
