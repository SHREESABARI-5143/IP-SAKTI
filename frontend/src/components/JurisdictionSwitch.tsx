"use client";

import React from "react";
import { Globe } from "lucide-react";

interface JurisdictionSwitchProps {
  jurisdiction: "india" | "international" | "both";
  onChange: (j: "india" | "international" | "both") => void;
}

export const JurisdictionSwitch: React.FC<JurisdictionSwitchProps> = ({
  jurisdiction,
  onChange,
}) => {
  return (
    <div className="flex items-center bg-emerald-50/70 border border-emerald-200/80 rounded-full p-1 shadow-sm">
      <button
        onClick={() => onChange("india")}
        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-200 ${
          jurisdiction === "india"
            ? "bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/20"
            : "text-slate-600 hover:text-emerald-800 hover:bg-emerald-100/50"
        }`}
      >
        <span className="text-sm">🇮🇳</span>
        <span>India</span>
      </button>

      <button
        onClick={() => onChange("international")}
        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-200 ${
          jurisdiction === "international"
            ? "bg-gradient-to-r from-teal-700 to-emerald-800 text-white shadow-md shadow-teal-700/20"
            : "text-slate-600 hover:text-emerald-800 hover:bg-emerald-100/50"
        }`}
      >
        <Globe className="w-3.5 h-3.5" />
        <span>International</span>
      </button>
    </div>
  );
};
