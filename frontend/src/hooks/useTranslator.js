"use client";

import { useState, useEffect, useRef, useCallback } from "react";

export const INDIAN_LANGUAGES = [
  { code: "hi", name: "Hindi", native: "हिन्दी", flores: "hin_Deva" },
  { code: "ta", name: "Tamil", native: "தமிழ்", flores: "tam_Taml" },
  { code: "te", name: "Telugu", native: "తెలుగు", flores: "tel_Telu" },
  { code: "bn", name: "Bengali", native: "বাংলা", flores: "ben_Beng" },
  { code: "mar", name: "Marathi", native: "मराठी", flores: "mar_Deva" },
  { code: "gu", name: "Gujarati", native: "ગુજરાતી", flores: "guj_Gujr" },
];

export function useTranslator() {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [targetLang, setTargetLang] = useState("hi");
  const [status, setStatus] = useState("idle"); // idle, loading, ready, translating, complete, error
  const [progressInfo, setProgressInfo] = useState({ percent: 0, file: "" });
  const [device, setDevice] = useState("wasm");
  const [latency, setLatency] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const workerRef = useRef(null);
  const debounceTimerRef = useRef(null);
  const requestIdRef = useRef(0);

  // Initialize Worker
  useEffect(() => {
    try {
      workerRef.current = new Worker(
        new URL("../workers/translator.worker.js", import.meta.url),
        { type: "module" }
      );

      workerRef.current.onmessage = (e) => {
        const { status: workerStatus, progress, device: dev, output, latencyMs, error } = e.data;

        if (workerStatus === "loading") {
          setStatus("loading");
        } else if (workerStatus === "progress") {
          if (progress) {
            const pct = Math.round((progress.progress || 0) * 100);
            setProgressInfo({
              percent: pct,
              file: progress.file || "Loading translation model...",
            });
          }
        } else if (workerStatus === "ready") {
          setStatus("ready");
          if (dev) setDevice(dev);
        } else if (workerStatus === "translating") {
          setStatus("translating");
        } else if (workerStatus === "complete") {
          setStatus("complete");
          setOutputText(output || "");
          if (latencyMs !== undefined) setLatency(latencyMs);
          if (dev) setDevice(dev);
        } else if (workerStatus === "error") {
          setStatus("error");
          setErrorMessage(error || "Translation engine error");
        }
      };

      // Request initialization
      workerRef.current.postMessage({
        type: "INIT",
        payload: { isDesktop: false },
      });
    } catch (err) {
      console.error("Worker initialization error:", err);
      setStatus("error");
      setErrorMessage("Could not initialize local translation worker in this browser.");
    }

    return () => {
      if (workerRef.current) {
        workerRef.current.terminate();
      }
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  const triggerTranslation = useCallback(
    (text, lang) => {
      if (!workerRef.current) return;
      if (!text || text.trim() === "") {
        setOutputText("");
        return;
      }

      requestIdRef.current += 1;
      const currentId = requestIdRef.current;

      workerRef.current.postMessage({
        type: "TRANSLATE",
        payload: {
          id: currentId,
          text: text.trim(),
          targetLang: lang,
        },
      });
    },
    []
  );

  const handleInputChange = (text) => {
    setInputText(text);

    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = setTimeout(() => {
      triggerTranslation(text, targetLang);
    }, 300);
  };

  const handleLanguageChange = (lang) => {
    setTargetLang(lang);
    if (inputText) {
      triggerTranslation(inputText, lang);
    }
  };

  const handleClear = () => {
    setInputText("");
    setOutputText("");
    setLatency(null);
  };

  return {
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
    isReady: status === "ready" || status === "complete" || status === "translating",
    isTranslating: status === "translating",
    isLoading: status === "loading",
  };
}
