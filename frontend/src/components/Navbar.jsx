"use client";

import React from "react";
import Link from "next/link";
import { Leaf, PanelLeft, PanelLeftClose } from "lucide-react";
import { JurisdictionSwitch } from "./JurisdictionSwitch";
import { LanguageSelector } from "./LanguageSelector";
import { useApp } from "@/context/AppContext";

export const Navbar = ({
  jurisdiction: propJurisdiction,
  onJurisdictionChange: propOnJurisdictionChange,
  language: propLanguage,
  onLanguageChange: propOnLanguageChange,
} = {}) => {
  const appContext = useApp();

  const jurisdiction = propJurisdiction || appContext.jurisdiction;
  const onJurisdictionChange = propOnJurisdictionChange || appContext.setJurisdiction;
  const language = propLanguage || appContext.language;
  const onLanguageChange = propOnLanguageChange || appContext.setLanguage;
  const { isSidebarOpen, toggleSidebar } = appContext;

  return (
    <header className="sticky top-0 z-40 w-full border-b border-emerald-100 bg-white/95 backdrop-blur-md shadow-2xs">
      <div className="w-full max-w-7xl 2xl:max-w-[1600px] mx-auto px-3 sm:px-6 h-16 flex items-center justify-between gap-3">
        {/* Left Side: Sidebar Toggle + Brand Logo */}
        <div className="flex items-center gap-2.5 sm:gap-3">
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-xl text-slate-600 hover:text-emerald-800 hover:bg-emerald-50 border border-slate-200/80 hover:border-emerald-300 transition shadow-2xs"
            title={isSidebarOpen ? "Collapse Navigation & History Sidebar" : "Expand Navigation & History Sidebar"}
          >
            {isSidebarOpen ? (
              <PanelLeftClose className="w-5 h-5 text-emerald-700" />
            ) : (
              <PanelLeft className="w-5 h-5 text-emerald-700" />
            )}
          </button>

          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 p-0.5 flex items-center justify-center shadow-md shadow-emerald-500/20 group-hover:scale-105 transition-transform">
              <div className="w-full h-full bg-white rounded-[10px] flex items-center justify-center">
                <Leaf className="w-4 h-4 text-emerald-600" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-lg tracking-tight text-slate-900 font-manrope">
                  AYURA
                </span>
                <span className="t-label px-2 py-0.5 bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-full text-[10px]">
                  IP-SAKTI
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">
                Ministry of Ayush Legal &amp; IP Intelligence
              </p>
            </div>
          </Link>
        </div>

        {/* Right Side: Jurisdiction & Language Controls */}
        <div className="flex items-center gap-2 sm:gap-3">
          <JurisdictionSwitch
            jurisdiction={jurisdiction}
            onChange={onJurisdictionChange}
          />
          <LanguageSelector
            language={language}
            onChange={onLanguageChange}
          />
        </div>
      </div>
    </header>
  );
};


