/**
 * OfflineTranslator.jsx
 * Dual-pane real-time translation UI with offline indicators & language selection.
 */
"use client";

import React, { useState } from "react";
import {
  Languages,
  Cpu,
  Zap,
  Copy,
  Check,
  Trash2,
  DownloadCloud,
  AlertCircle,
  Loader2,
} from "lucide-react";
import { useTranslator, INDIAN_LANGUAGES } from "../hooks/useTranslator";

export default function OfflineTranslator() {
  const {
    inputText,
    outputText,
    targetLang,
    status,
    progressInfo,
    device,
    latency,
    errorMessage,
    handleInputChange,
    handleLanguageChange,
    handleClear,
    isReady,
    isTranslating,
    isLoading,
  } = useTranslator();

  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    if (!outputText) return;
    navigator.clipboard.writeText(outputText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const currentLangObj =
    INDIAN_LANGUAGES.find((l) => l.code === targetLang) || INDIAN_LANGUAGES[0];

  return (
    <div className="w-full max-w-5xl mx-auto p-4 sm:p-6 space-y-5">
      {/* Header & Status Indicator Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-white border border-emerald-100 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center gap-3.5">
          <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl border border-emerald-100">
            <Languages className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-800 flex items-center gap-2">
              Offline Neural Translator
              <span className="text-[11px] font-semibold px-2.5 py-0.5 bg-emerald-100 text-emerald-800 rounded-full border border-emerald-200">
                100% Local (NLLB-200)
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Zero external cloud calls • Runs in background Web Worker • WebGPU/WASM
            </p>
          </div>
        </div>

        {/* Device & Engine Badge */}
        <div className="flex items-center gap-2 text-xs">
          {isLoading ? (
            <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-50 text-amber-700 border border-amber-200 rounded-xl">
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              <span>Loading Engine...</span>
            </div>
          ) : isReady ? (
            <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-xl">
              {device === "webgpu" ? (
                <Zap className="w-3.5 h-3.5 text-amber-500" />
              ) : (
                <Cpu className="w-3.5 h-3.5 text-emerald-600" />
              )}
              <span className="font-semibold uppercase">{device} Accelerated</span>
              {latency !== null && (
                <span className="text-[10px] text-slate-400">({latency}ms)</span>
              )}
            </div>
          ) : null}
        </div>
      </div>

      {/* Progress / Error Alerts */}
      {isLoading && (
        <div className="bg-slate-900 text-white rounded-2xl p-4 shadow-md space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="flex items-center gap-2 font-medium">
              <DownloadCloud className="w-4 h-4 text-emerald-400 animate-bounce" />
              {progressInfo.file || "Downloading quantized model weights to browser cache..."}
            </span>
            <span className="font-mono text-emerald-400 font-bold">{progressInfo.percent}%</span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-emerald-500 h-2 transition-all duration-300 ease-out"
              style={{ width: `${progressInfo.percent}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-400">
            Downloaded once and permanently cached offline via Cache API.
          </p>
        </div>
      )}

      {status === "error" && (
        <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 p-3.5 rounded-xl text-xs">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Dual Pane Translation Area */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Source: English (Left Pane) */}
        <div className="flex flex-col bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden focus-within:border-emerald-500 transition-colors">
          <div className="flex items-center justify-between px-4 py-2.5 border-b border-slate-100 bg-slate-50/60">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              English (Source)
            </span>
            {inputText && (
              <button
                onClick={handleClear}
                className="text-slate-400 hover:text-red-500 transition-colors p-1"
                title="Clear input"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
          <textarea
            value={inputText}
            onChange={(e) => handleInputChange(e.target.value)}
            placeholder="Type English legal or patent text here to translate in real-time..."
            className="w-full h-64 p-4 text-slate-800 placeholder-slate-400 resize-none focus:outline-none text-sm leading-relaxed"
          />
          <div className="flex items-center justify-between px-4 py-2 border-t border-slate-100 text-[11px] text-slate-400">
            <span>{inputText.length} characters</span>
            <span>300ms Debounced</span>
          </div>
        </div>

        {/* Target: Indian Language (Right Pane) */}
        <div className="flex flex-col bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="flex items-center justify-between px-4 py-2 border-b border-slate-100 bg-slate-50/60">
            {/* Target Language Dropdown */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-500 uppercase">Target:</span>
              <select
                value={targetLang}
                onChange={(e) => handleLanguageChange(e.target.value)}
                className="text-xs font-bold bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-emerald-800 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              >
                {INDIAN_LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.native} ({lang.name})
                  </option>
                ))}
              </select>
            </div>

            {/* Copy Button */}
            <button
              onClick={copyToClipboard}
              disabled={!outputText}
              className={`flex items-center gap-1 text-xs px-2.5 py-1 rounded-lg transition-colors ${
                copied
                  ? "bg-emerald-100 text-emerald-800"
                  : "hover:bg-slate-100 text-slate-600 disabled:opacity-40"
              }`}
              title="Copy translated text"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-600" />
                  <span className="text-[11px] font-medium">Copied</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span className="text-[11px]">Copy</span>
                </>
              )}
            </button>
          </div>

          <div className="relative flex-1">
            <textarea
              value={outputText}
              readOnly
              placeholder={
                isLoading
                  ? "Initializing local model..."
                  : `Real-time translation in ${currentLangObj.name} (${currentLangObj.native}) will appear here...`
              }
              className="w-full h-64 p-4 text-slate-800 placeholder-slate-400 bg-slate-50/30 resize-none focus:outline-none text-sm leading-relaxed"
            />
            {isTranslating && (
              <div className="absolute bottom-3 right-3 flex items-center gap-1.5 px-2 py-1 bg-white/95 border border-slate-200 rounded-md text-[10px] text-slate-600 shadow-xs">
                <Loader2 className="w-3 h-3 animate-spin text-emerald-600" />
                <span>Translating...</span>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between px-4 py-2 border-t border-slate-100 text-[11px] text-slate-400">
            <span>FLORES Code: {currentLangObj.flores}</span>
            {latency !== null && !isTranslating && (
              <span className="text-emerald-600 font-medium">Rendered in {latency}ms</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
