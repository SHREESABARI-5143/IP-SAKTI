"use client";

import React from "react";
import { Globe } from "lucide-react";

export const JurisdictionSwitch = ({
  jurisdiction,
  onChange,
}) => {
  const isInternational = jurisdiction === "international";

  return (
    <div
      className={`flex items-center bg-slate-100/90 p-0.5 sm:p-1 rounded-full border transition-all duration-300 shadow-2xs backdrop-blur-xs ${
        isInternational
          ? "border-blue-200/90 bg-blue-50/40 shadow-blue-500/10"
          : "border-emerald-200/70 bg-slate-100/80 shadow-emerald-500/10"
      }`}
    >
      <button
        type="button"
        onClick={() => onChange("india")}
        className={`flex items-center gap-1.5 px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full text-[11px] sm:text-xs font-semibold transition-all duration-300 cursor-pointer ${
          !isInternational
            ? "bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-sm shadow-emerald-600/30 scale-[1.02]"
            : "text-slate-600 hover:text-blue-900 hover:bg-white/70"
        }`}
        title="Switch to Indian Statutory Law (Patents Act, BD Act, D&C Act, TKDL)"
      >
        <span className="text-xs sm:text-sm">🇮🇳</span>
        <span>India</span>
      </button>

      <button
        type="button"
        onClick={() => onChange("international")}
        className={`flex items-center gap-1.5 px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full text-[11px] sm:text-xs font-semibold transition-all duration-300 cursor-pointer ${
          isInternational
            ? "bg-gradient-to-r from-blue-600 via-indigo-600 to-sky-600 text-white shadow-sm shadow-blue-600/30 scale-[1.02]"
            : "text-slate-600 hover:text-emerald-900 hover:bg-white/70"
        }`}
        title="Switch to International Treaties (TRIPS, Nagoya Protocol, CBD, PCT)"
      >
        <Globe className={`w-3.5 h-3.5 text-current ${isInternational ? "animate-spin" : ""}`} style={isInternational ? { animationDuration: "14s" } : {}} />
        <span>International</span>
      </button>
    </div>
  );
};
