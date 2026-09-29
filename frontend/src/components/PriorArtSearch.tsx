"use client";

import React, { useState } from "react";
import { searchPriorArt, PriorArtResponse } from "@/lib/api";
import { Search, BookOpen, AlertTriangle, Microscope } from "lucide-react";
import { SupportedLanguage } from "./LanguageSelector";

interface PriorArtSearchProps {
  language: SupportedLanguage;
}

export const PriorArtSearch: React.FC<PriorArtSearchProps> = ({ language }) => {
  const [ingredientInput, setIngredientInput] = useState<string>("Haridra, Pippali, Ghrita");
  const [freeTextInput, setFreeTextInput] = useState<string>("Turmeric based formulation for skin allergy");
  const [response, setResponse] = useState<PriorArtResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const ings = ingredientInput.split(",").map((s) => s.trim()).filter(Boolean);
      const res = await searchPriorArt(ings, freeTextInput);
      setResponse(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6 space-y-6">

      {/* Page Header */}
      <div className="p-6 rounded-2xl bg-white border border-emerald-100 shadow-md space-y-2">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-teal-50 flex items-center justify-center">
            <Microscope className="w-5 h-5 text-teal-700" />
          </div>
          <div>
            <h2 className="t-subheading text-slate-900">
              {language === "hi"
                ? "एएफआई / एपीआई पूर्व कला (Prior-Art) खोज"
                : "Formulation Prior-Art & TKDL Search"}
            </h2>
            <p className="t-small text-slate-500">Real vector search against AFI Part I pharmacopoeial monographs</p>
          </div>
        </div>
        <p className="t-body text-slate-600 max-w-2xl leading-relaxed">
          {language === "hi"
            ? "आयुर्वेदिक फॉर्मूलरी ऑफ़ इंडिया (AFI) और फार्माकोपिया डेटाबेस में अपने योग/घटकों की जांच करें कि क्या यह पूर्व कला के रूप में मौजूद है।"
            : "Check your formulation ingredients and preparation methods against codified classical texts (AFI & API) to identify prior-art barriers before filing patent applications."}
        </p>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSearch} className="bg-white border border-emerald-100 shadow-md p-6 rounded-2xl space-y-4">
        <div>
          <label className="block t-label text-slate-700 uppercase tracking-wider mb-2">
            {language === "hi" ? "घटक सूची (कॉमा से अलग करें)" : "Formulation Ingredients (Comma separated)"}
          </label>
          <input
            type="text"
            value={ingredientInput}
            onChange={(e) => setIngredientInput(e.target.value)}
            placeholder="e.g. Haridra, Pippali, Ghrita, Amalaki"
            className="w-full bg-white border border-emerald-200 focus:border-emerald-500 rounded-xl px-4 py-3 t-body text-slate-800 placeholder-slate-400 focus:outline-none focus:shadow-md transition"
          />
        </div>

        <div>
          <label className="block t-label text-slate-700 uppercase tracking-wider mb-2">
            {language === "hi" ? "विवरण या चिकित्सीय संकेत" : "Free-text Description or Indication"}
          </label>
          <input
            type="text"
            value={freeTextInput}
            onChange={(e) => setFreeTextInput(e.target.value)}
            placeholder="e.g. Fermented liquid for digestion and cough"
            className="w-full bg-white border border-emerald-200 focus:border-emerald-500 rounded-xl px-4 py-3 t-body text-slate-800 placeholder-slate-400 focus:outline-none focus:shadow-md transition"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full t-btn gap-2 py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl shadow-lg shadow-emerald-600/20 transition disabled:opacity-50 hover:-translate-y-0.5 active:translate-y-0"
        >
          {loading ? (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <>
              <Search className="w-4 h-4" />
              <span>{language === "hi" ? "पूर्व कला खोजें" : "Search Codified Prior-Art"}</span>
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
              <span>Prior-Art Assessment Verdict</span>
            </div>
            <p className="text-xs text-slate-700">{response.summary_verdict}</p>
            <div className="text-xs text-slate-700 bg-white p-3 rounded-lg border border-amber-200">
              <strong className="text-amber-700">Recommendation:</strong> {response.recommendation}
            </div>
          </div>

          {/* Matched formulations */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Matched Classical Formulations ({response.matches.length})
            </h3>

            {response.matches.map((match) => (
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
                    Similarity: {Math.round(match.match_score * 100)}%
                  </span>
                </div>

                <div className="grid sm:grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="font-semibold text-slate-500 block mb-1">Ingredients in Text:</span>
                    <div className="flex flex-wrap gap-1">
                      {match.ingredients.map((ing, idx) => (
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
                    <span className="font-semibold text-slate-500 block mb-1">Traditional Indication:</span>
                    <p className="text-slate-600 bg-slate-50 p-2 rounded border border-slate-200 leading-relaxed">
                      {match.indication}
                    </p>
                  </div>
                </div>

                <div className="text-xs text-amber-700 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
                  <strong className="text-amber-700">Section 3(p) Patent Status:</strong> {match.patentability_status}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
