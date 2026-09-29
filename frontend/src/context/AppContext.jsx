"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

const AppContext = createContext(undefined);

export const SUPPORTED_LANGUAGES = [
  { code: "en", nativeLabel: "English", englishLabel: "English", flores: "eng_Latn" },
  { code: "hi", nativeLabel: "हिन्दी", englishLabel: "Hindi", flores: "hin_Deva" },
  { code: "sa", nativeLabel: "संस्कृतम्", englishLabel: "Sanskrit", flores: "san_Deva" },
  { code: "ta", nativeLabel: "தமிழ்", englishLabel: "Tamil", flores: "tam_Taml" },
  { code: "te", nativeLabel: "తెలుగు", englishLabel: "Telugu", flores: "tel_Telu" },
  { code: "mr", nativeLabel: "मराठी", englishLabel: "Marathi", flores: "mar_Deva" },
  { code: "bn", nativeLabel: "বাংলা", englishLabel: "Bengali", flores: "ben_Beng" },
  { code: "gu", nativeLabel: "ગુજરાતી", englishLabel: "Gujarati", flores: "guj_Gujr" },
];

export function AppProvider({ children }) {
  const [language, setLanguageState] = useState("en");
  const [jurisdiction, setJurisdictionState] = useState("india");
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [chatHistory, setChatHistory] = useState([]);
  const [classificationHistory, setClassificationHistory] = useState([]);
  const [priorArtHistory, setPriorArtHistory] = useState([]);
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    try {
      const savedLang = localStorage.getItem("ipsakti_language");
      if (savedLang) setLanguageState(savedLang);

      const savedJurisdiction = localStorage.getItem("ipsakti_jurisdiction");
      if (savedJurisdiction) setJurisdictionState(savedJurisdiction);

      const savedSidebar = localStorage.getItem("ipsakti_sidebar_open");
      if (savedSidebar !== null) setIsSidebarOpen(savedSidebar === "true");

      const savedChat = localStorage.getItem("ipsakti_chat_history");
      if (savedChat) setChatHistory(JSON.parse(savedChat));

      const savedClassify = localStorage.getItem("ipsakti_classify_history");
      if (savedClassify) setClassificationHistory(JSON.parse(savedClassify));

      const savedPA = localStorage.getItem("ipsakti_pa_history");
      if (savedPA) setPriorArtHistory(JSON.parse(savedPA));
    } catch {
      // Ignore localStorage errors
    }
    setIsHydrated(true);
  }, []);

  const setLanguage = (lang) => {
    setLanguageState(lang);
    try {
      localStorage.setItem("ipsakti_language", lang);
    } catch {}
  };

  const setJurisdiction = (jur) => {
    setJurisdictionState(jur);
    try {
      localStorage.setItem("ipsakti_jurisdiction", jur);
    } catch {}
  };

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => {
      const next = !prev;
      try {
        localStorage.setItem("ipsakti_sidebar_open", String(next));
      } catch {}
      return next;
    });
  };

  const addChatHistory = (item) => {
    setChatHistory((prev) => {
      const updated = [
        {
          id: `chat_${Date.now()}`,
          timestamp: new Date().toISOString(),
          ...item,
        },
        ...prev.slice(0, 19), // Keep last 20
      ];
      try {
        localStorage.setItem("ipsakti_chat_history", JSON.stringify(updated));
      } catch {}
      return updated;
    });
  };

  const addClassificationHistory = (item) => {
    setClassificationHistory((prev) => {
      const updated = [
        {
          id: `cls_${Date.now()}`,
          timestamp: new Date().toISOString(),
          ...item,
        },
        ...prev.slice(0, 19),
      ];
      try {
        localStorage.setItem("ipsakti_classify_history", JSON.stringify(updated));
      } catch {}
      return updated;
    });
  };

  const addPriorArtHistory = (item) => {
    setPriorArtHistory((prev) => {
      const updated = [
        {
          id: `pa_${Date.now()}`,
          timestamp: new Date().toISOString(),
          ...item,
        },
        ...prev.slice(0, 19),
      ];
      try {
        localStorage.setItem("ipsakti_pa_history", JSON.stringify(updated));
      } catch {}
      return updated;
    });
  };

  const clearHistory = (type = "all") => {
    if (type === "all" || type === "chat") {
      setChatHistory([]);
      try { localStorage.removeItem("ipsakti_chat_history"); } catch {}
    }
    if (type === "all" || type === "classification") {
      setClassificationHistory([]);
      try { localStorage.removeItem("ipsakti_classify_history"); } catch {}
    }
    if (type === "all" || type === "prior_art") {
      setPriorArtHistory([]);
      try { localStorage.removeItem("ipsakti_pa_history"); } catch {}
    }
  };

  return (
    <AppContext.Provider
      value={{
        language,
        setLanguage,
        jurisdiction,
        setJurisdiction,
        isSidebarOpen,
        setIsSidebarOpen,
        toggleSidebar,
        chatHistory,
        addChatHistory,
        classificationHistory,
        addClassificationHistory,
        priorArtHistory,
        addPriorArtHistory,
        clearHistory,
        isHydrated,
        supportedLanguages: SUPPORTED_LANGUAGES,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
}

