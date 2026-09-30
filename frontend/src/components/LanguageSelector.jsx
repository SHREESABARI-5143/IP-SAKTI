"use client";

import React, { useState, useRef, useEffect } from "react";
import { Globe, ChevronDown, Check } from "lucide-react";

export const SUPPORTED_LANGUAGES = [
  { code: "en", nativeLabel: "English", englishLabel: "English" },
  { code: "hi", nativeLabel: "हिन्दी", englishLabel: "Hindi" },
  { code: "sa", nativeLabel: "संस्कृतम्", englishLabel: "Sanskrit" },
  { code: "ta", nativeLabel: "தமிழ்", englishLabel: "Tamil" },
  { code: "te", nativeLabel: "తెలుగు", englishLabel: "Telugu" },
  { code: "mr", nativeLabel: "मराठी", englishLabel: "Marathi" },
  { code: "bn", nativeLabel: "বাংলা", englishLabel: "Bengali" },
];

export const LanguageSelector = ({
  language,
  onChange,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const currentOption =
    SUPPORTED_LANGUAGES.find((l) => l.code === language) || SUPPORTED_LANGUAGES[0];

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1 sm:py-1.5 bg-white/95 hover:bg-emerald-50/80 text-slate-700 hover:text-emerald-900 border border-emerald-200/80 rounded-xl text-xs font-semibold shadow-2xs transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-emerald-400 cursor-pointer"
        aria-expanded={isOpen}
      >
        <Globe className="w-3.5 h-3.5 text-emerald-600" />
        <span className="font-semibold text-slate-800">{currentOption.nativeLabel}</span>
        <ChevronDown
          className={`w-3 h-3 text-slate-400 transition-transform duration-200 ${
            isOpen ? "rotate-180 text-emerald-600" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-52 bg-white/95 backdrop-blur-xl border border-emerald-100 rounded-2xl shadow-xl z-50 py-1.5 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
          <div className="px-3.5 py-1.5 text-[10px] font-bold text-slate-400 uppercase tracking-wider border-b border-emerald-50/80 flex items-center justify-between">
            <span>Select Language</span>
            <span className="text-emerald-700 font-mono bg-emerald-50 px-1.5 py-0.5 rounded text-[9px]">7 Supported</span>
          </div>
          <div className="py-1 max-h-64 overflow-y-auto">
            {SUPPORTED_LANGUAGES.map((opt) => (
              <button
                key={opt.code}
                onClick={() => {
                  onChange(opt.code);
                  setIsOpen(false);
                }}
                className={`w-full flex items-center justify-between px-3.5 py-2 text-left text-xs transition-colors cursor-pointer ${
                  opt.code === language
                    ? "bg-emerald-50/90 text-emerald-900 font-bold"
                    : "text-slate-700 hover:bg-emerald-50/50 hover:text-emerald-800 font-medium"
                }`}
              >
                <div className="flex flex-col">
                  <span className="text-xs">{opt.nativeLabel}</span>
                  <span className="text-[10px] text-slate-400 font-normal">{opt.englishLabel}</span>
                </div>
                {opt.code === language ? (
                  <Check className="w-3.5 h-3.5 text-emerald-600" />
                ) : (
                  <span className="text-[10px] font-mono text-slate-300 uppercase">{opt.code}</span>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
