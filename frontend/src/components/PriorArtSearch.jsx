"use client";

import React, { useState } from "react";
import { searchPriorArt } from "@/lib/api";
import { Search, AlertTriangle, Microscope } from "lucide-react";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

export const PriorArtSearch = ({ language }) => {
  const { addPriorArtHistory } = useApp();
  const [ingredientInput, setIngredientInput] = useState("Haridra, Pippali, Ghrita");
  const [freeTextInput, setFreeTextInput] = useState("Turmeric based formulation for skin allergy");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const ings = ingredientInput.split(",").map((s) => s.trim()).filter(Boolean);
      const res = await searchPriorArt(ings, freeTextInput);
      setResponse(res);
      if (addPriorArtHistory) {
        addPriorArtHistory({
          ingredients: ings,
          query: freeTextInput,
          match_count: res.matches?.length || 0,
        });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">

      {/* Page Header */}
      <div className="p-6 sm:p-7 rounded-2xl bg-white/95 backdrop-blur-xs border border-emerald-100/90 shadow-sm space-y-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-50 border border-teal-200/80 flex items-center justify-center shadow-2xs">
            <Microscope className="w-5 h-5 text-teal-700" />
          </div>
          <div>
            <h2 className="t-subheading text-slate-900">
              {t(language, "searchHeaderTitle")}
            </h2>
            <p className="t-small text-slate-500">{t(language, "searchHeaderSubtitle")}</p>
          </div>
        </div>
        <p className="t-body text-slate-600 max-w-2xl leading-relaxed">
          {t(language, "searchHeaderDesc")}
        </p>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSearch} className="bg-white border border-emerald-100 shadow-md p-6 rounded-2xl space-y-4">
        <div>
          <label className="block t-label text-slate-700 uppercase tracking-wider mb-2">
            {t(language, "ingredientsLabel")}
          </label>
          <input
            type="text"
            value={ingredientInput}
            onChange={(e) => setIngredientInput(e.target.value)}
            placeholder={t(language, "ingredientsPlaceholder")}
            className="w-full bg-white border border-emerald-200 focus:border-emerald-500 rounded-xl px-4 py-3 t-body text-slate-800 placeholder-slate-400 focus:outline-none focus:shadow-md transition"
          />
        </div>

        <div>
          <label className="block t-label text-slate-700 uppercase tracking-wider mb-2">
            {t(language, "freeTextLabel")}
          </label>
          <input
            type="text"
            value={freeTextInput}
            onChange={(e) => setFreeTextInput(e.target.value)}
            placeholder={t(language, "freeTextPlaceholder")}
            className="w-full bg-white border border-emerald-200 focus:border-emerald-500 rounded-xl px-4 py-3 t-body text-slate-800 placeholder-slate-400 focus:outline-none focus:shadow-md transition"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full t-btn gap-2 py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl shadow-lg shadow-emerald-600/20 transition disabled:opacity-50 hover:-translate-y-0.5 active:translate-y-0 cursor-pointer"
        >
          {loading ? (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <>
              <Search className="w-4 h-4" />
              <span>{t(language, "searchBtn")}</span>
            </>
          )}
        </button>
      </form>

      {/* Results */}
      {response && (
        <div className="space-y-4 animate-in fade-in duration-300">
          {/* Verdict banner */}
          <div className="p-5 rounded-xl border border-amber-200 bg-amber-50 shadow-sm space-y-2">
            <div className="flex items-center gap-2 text-amber-700 font-bold text-sm">
              <AlertTriangle className="w-5 h-5" />
              <span>{t(language, "priorArtVerdict")}</span>
            </div>
            <p className="text-xs text-slate-700">{response.summary_verdict}</p>
            <div className="text-xs text-slate-700 bg-white p-3 rounded-lg border border-amber-200">
              <strong className="text-amber-700">{t(language, "recommendationLabel")}</strong> {response.recommendation}
            </div>
          </div>

          {/* Matched formulations */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              {t(language, "matchedFormulations")} ({response.matches?.length || 0})
            </h3>

            {response.matches?.map((match) => (
              <div
                key={match.id}
                className="bg-white p-5 rounded-xl border border-emerald-100 hover:border-emerald-300 shadow-sm hover:shadow-md transition space-y-3"
              >
                <div className="flex items-center justify-between border-b border-emerald-50 pb-2">
                  <div>
                    <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      <span>{match.name}</span>
                      <span className="text-xs text-amber-600 font-normal">({match.sanskrit_name})</span>
                    </h4>
                    <span className="text-[11px] text-slate-400">
                      Text: {match.source_text} | Ref: {match.afi_reference}
                    </span>
                  </div>
                  <span className="px-2.5 py-1 bg-teal-50 text-teal-700 border border-teal-200 rounded-full text-xs font-bold">
                    {t(language, "similarity")} {Math.round(match.match_score * 100)}%
                  </span>
                </div>

                <div className="grid sm:grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="font-semibold text-slate-500 block mb-1">{t(language, "ingredientsInText")}</span>
                    <div className="flex flex-wrap gap-1">
                      {match.ingredients?.map((ing, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded border border-emerald-200 text-[11px] font-medium"
                        >
                          {ing}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <span className="font-semibold text-slate-500 block mb-1">{t(language, "traditionalIndication")}</span>
                    <p className="text-slate-600 bg-slate-50 p-2 rounded border border-slate-200 leading-relaxed">
                      {match.indication}
                    </p>
                  </div>
                </div>

                <div className="text-xs text-amber-700 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
                  <strong className="text-amber-700">{t(language, "section3pStatus")}</strong> {match.patentability_status}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
