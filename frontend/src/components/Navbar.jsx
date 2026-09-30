"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Leaf,
  PanelLeft,
  PanelLeftClose,
  Sparkles,
  Scale,
  Microscope,
  Home,
  Database
} from "lucide-react";
import { JurisdictionSwitch } from "./JurisdictionSwitch";
import { LanguageSelector } from "./LanguageSelector";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

export const Navbar = ({
  jurisdiction: propJurisdiction,
  onJurisdictionChange: propOnJurisdictionChange,
  language: propLanguage,
  onLanguageChange: propOnLanguageChange,
} = {}) => {
  const pathname = usePathname();
  const appContext = useApp();

  const jurisdiction = propJurisdiction || appContext.jurisdiction;
  const onJurisdictionChange = propOnJurisdictionChange || appContext.setJurisdiction;
  const language = propLanguage || appContext.language;
  const onLanguageChange = propOnLanguageChange || appContext.setLanguage;
  const { isSidebarOpen, toggleSidebar } = appContext;
  const isInternational = jurisdiction === "international";

  const navLinks = [
    { label: t(language, "home"), href: "/", icon: Home },
    { label: t(language, "aiAssistant"), href: "/chat", icon: Sparkles },
    { label: t(language, "classifier"), href: "/classify", icon: Scale },
    { label: t(language, "priorArt"), href: "/search", icon: Microscope },
  ];

  return (
    <header
      className={`sticky top-0 z-40 w-full border-b backdrop-blur-xl shadow-xs transition-colors duration-500 ${
        isInternational
          ? "border-blue-100/90 bg-white/92 shadow-blue-500/5"
          : "border-emerald-100/80 bg-white/90 shadow-emerald-500/5"
      }`}
    >
      {/* Subtle glowing accent line at the bottom */}
      <div
        className={`absolute bottom-0 left-0 right-0 h-[1.5px] bg-gradient-to-r pointer-events-none transition-all duration-500 ${
          isInternational
            ? "from-transparent via-blue-500/50 to-transparent"
            : "from-transparent via-emerald-500/40 to-transparent"
        }`}
      />

      <div className="w-full px-3 sm:px-4 lg:px-6 h-16 flex items-center justify-between gap-2 sm:gap-4">
        {/* Left Side: Sidebar Toggle + Brand Logo */}
        <div className="flex items-center gap-2.5 sm:gap-3 shrink-0">
          <button
            onClick={toggleSidebar}
            className={`p-2 rounded-xl border transition-all duration-200 shadow-2xs group cursor-pointer ${
              isInternational
                ? "text-slate-600 hover:text-blue-900 hover:bg-blue-50/80 border-slate-200/80 hover:border-blue-300"
                : "text-slate-600 hover:text-emerald-800 hover:bg-emerald-50/80 border-slate-200/80 hover:border-emerald-300"
            }`}
            title={isSidebarOpen ? "Collapse Navigation & History Sidebar" : "Expand Navigation & History Sidebar"}
            aria-label="Toggle Sidebar"
          >
            {isSidebarOpen ? (
              <PanelLeftClose
                className={`w-4.5 h-4.5 transition-transform group-hover:scale-105 ${
                  isInternational ? "text-blue-700" : "text-emerald-700"
                }`}
              />
            ) : (
              <PanelLeft
                className={`w-4.5 h-4.5 transition-transform group-hover:scale-105 ${
                  isInternational ? "text-blue-700" : "text-emerald-700"
                }`}
              />
            )}
          </button>

          <Link href="/" className="flex items-center gap-2.5 sm:gap-3 group">
            <div
              className={`w-11 h-11 sm:w-12 sm:h-12 rounded-xl p-[2px] flex items-center justify-center shadow-md transition-all duration-300 group-hover:scale-105 shrink-0 ${
                isInternational
                  ? "bg-gradient-to-br from-blue-600 via-indigo-600 to-sky-500 shadow-blue-600/25 group-hover:shadow-blue-600/35"
                  : "bg-gradient-to-br from-emerald-500 via-emerald-600 to-teal-600 shadow-emerald-600/20 group-hover:shadow-emerald-600/30"
              }`}
            >
              <div className="w-full h-full bg-[#fdfaf3] rounded-[10px] p-0.5 flex items-center justify-center overflow-hidden">
                <img
                  src="/ayura_logo.png"
                  alt="AYURA Product Logo"
                  className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300"
                />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900 font-manrope">
                  AYURA
                </span>
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wide transition-colors duration-300 border ${
                    isInternational
                      ? "bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-900 border-blue-200/90"
                      : "bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-800 border-emerald-200/80"
                  }`}
                >
                  {isInternational ? "GLOBAL-TREATIES" : "IP-SAKTI"}
                </span>
              </div>
              <p className="text-[10px] sm:text-[11px] text-slate-500 font-medium hidden sm:block leading-none mt-0.5">
                {isInternational
                  ? "WIPO & International Treaties Intelligence"
                  : t(language, "ministrySubtitle")}
              </p>
            </div>
          </Link>
        </div>

        {/* Center: Desktop Navigation Hub Pills */}
        <nav className="hidden lg:flex items-center gap-1 bg-slate-100/70 border border-slate-200/70 p-1 rounded-2xl shadow-2xs">
          {navLinks.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`relative flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? isInternational
                      ? "bg-white text-blue-900 shadow-sm border border-blue-200/70 font-bold"
                      : "bg-white text-emerald-800 shadow-sm border border-emerald-200/60 font-bold"
                    : "text-slate-600 hover:text-slate-900 hover:bg-white/60"
                }`}
              >
                <Icon
                  className={`w-3.5 h-3.5 transition-colors ${
                    isActive
                      ? isInternational
                        ? "text-blue-600"
                        : "text-emerald-600"
                      : "text-slate-400"
                  }`}
                />
                <span>{item.label}</span>
                {isActive && (
                  <span
                    className={`w-1.5 h-1.5 rounded-full animate-pulse ml-0.5 ${
                      isInternational ? "bg-blue-500" : "bg-emerald-500"
                    }`}
                  />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Right Side: Live Status Badge + Controls */}
        <div className="flex items-center gap-2 sm:gap-2.5">
          {/* Live Statutory Graph Badge (Wide screens) */}
          <div
            className={`hidden xl:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium shadow-2xs transition-colors duration-300 border ${
              isInternational
                ? "bg-blue-50/80 border-blue-200/70 text-blue-900"
                : "bg-emerald-50/70 border-emerald-200/60 text-emerald-800"
            }`}
          >
            <span className="relative flex h-2 w-2">
              <span
                className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                  isInternational ? "bg-blue-400" : "bg-emerald-400"
                }`}
              />
              <span
                className={`relative inline-flex rounded-full h-2 w-2 ${
                  isInternational ? "bg-blue-500" : "bg-emerald-500"
                }`}
              />
            </span>
            <Database
              className={`w-3 h-3 ${isInternational ? "text-blue-600" : "text-emerald-600"}`}
            />
            <span>{isInternational ? "TRIPS • Nagoya • CBD" : "4.8k+ Citations"}</span>
          </div>

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


