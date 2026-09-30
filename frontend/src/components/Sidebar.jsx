"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Sparkles,
  Scale,
  Microscope,
  History,
  ChevronLeft,
  ChevronRight,
  Plus,
  Trash2,
  Leaf,
  Clock,
  ExternalLink,
  MessageSquare
} from "lucide-react";
import { useApp } from "@/context/AppContext";
import { t } from "@/lib/i18n";

export const Sidebar = () => {
  const pathname = usePathname();
  const {
    isSidebarOpen,
    toggleSidebar,
    chatHistory = [],
    classificationHistory = [],
    priorArtHistory = [],
    clearHistory,
    language,
  } = useApp();

  const [activeTab, setActiveTab] = useState("chat"); // 'chat' | 'classification' | 'prior_art'

  const navItems = [
    {
      label: t(language, "aiAssistant"),
      href: "/chat",
      icon: Sparkles,
      color: "text-emerald-700 bg-emerald-50",
      activeBg: "bg-emerald-50 text-emerald-900 font-bold border-emerald-300 shadow-2xs",
      accentBorder: "border-l-4 border-l-emerald-600",
      historyCount: chatHistory.length,
      tabId: "chat"
    },
    {
      label: t(language, "classifier"),
      href: "/classify",
      icon: Scale,
      color: "text-amber-700 bg-amber-50",
      activeBg: "bg-amber-50 text-amber-900 font-bold border-amber-300 shadow-2xs",
      accentBorder: "border-l-4 border-l-amber-600",
      historyCount: classificationHistory.length,
      tabId: "classification"
    },
    {
      label: t(language, "priorArt"),
      href: "/search",
      icon: Microscope,
      color: "text-teal-700 bg-teal-50",
      activeBg: "bg-teal-50 text-teal-900 font-bold border-teal-300 shadow-2xs",
      accentBorder: "border-l-4 border-l-teal-600",
      historyCount: priorArtHistory.length,
      tabId: "prior_art"
    }
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isSidebarOpen && (
        <div
          onClick={toggleSidebar}
          className="fixed inset-0 bg-slate-900/30 backdrop-blur-xs z-30 lg:hidden transition-opacity"
        />
      )}

      {/* Main Sidebar Panel */}
      <aside
        className={`fixed lg:sticky top-16 left-0 z-30 h-[calc(100vh-4rem)] bg-white/95 backdrop-blur-xl border-r border-emerald-100/90 shadow-sm transition-all duration-300 ease-in-out flex flex-col ${
          isSidebarOpen
            ? "w-72 sm:w-80 translate-x-0"
            : "w-0 lg:w-16 -translate-x-full lg:translate-x-0 overflow-hidden"
        }`}
      >
        {/* Top Control Rail */}
        <div className="p-2.5 sm:p-3 border-b border-emerald-100/70 flex items-center justify-between gap-2">
          {isSidebarOpen ? (
            <>
              <Link
                href="/chat"
                className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-gradient-to-r from-emerald-600 via-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white text-xs font-bold shadow-sm shadow-emerald-600/25 transition-all duration-200 hover:shadow-md hover:scale-[1.01]"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>{t(language, "newSession")}</span>
              </Link>
              <button
                onClick={toggleSidebar}
                className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-emerald-50 transition cursor-pointer"
                title="Collapse Sidebar"
                aria-label="Collapse Sidebar"
              >
                <ChevronLeft className="w-4 h-4 text-emerald-700" />
              </button>
            </>
          ) : (
            <div className="w-full flex flex-col items-center gap-2">
              <button
                onClick={toggleSidebar}
                className="w-10 h-10 flex items-center justify-center rounded-xl text-emerald-700 hover:bg-emerald-50 border border-emerald-200/60 shadow-2xs transition cursor-pointer group"
                title="Expand Sidebar"
                aria-label="Expand Sidebar"
              >
                <ChevronRight className="w-5 h-5 transition-transform group-hover:translate-x-0.5" />
              </button>
              <Link
                href="/chat"
                className="w-10 h-10 flex items-center justify-center rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition"
                title="New Session"
              >
                <Plus className="w-4 h-4" />
              </Link>
            </div>
          )}
        </div>

        {/* Primary Navigation Modules */}
        <div className="p-2 sm:p-2.5 space-y-1.5 border-b border-emerald-100/70">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setActiveTab(item.tabId)}
                className={`relative flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all text-xs group ${
                  isActive
                    ? `${item.activeBg} ${item.accentBorder}`
                    : "border-transparent hover:bg-emerald-50/50 text-slate-700 hover:text-slate-900"
                }`}
                title={!isSidebarOpen ? item.label : undefined}
              >
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 transition-transform group-hover:scale-105 ${
                    isActive ? "bg-white shadow-2xs text-emerald-700" : item.color
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>

                {isSidebarOpen ? (
                  <div className="flex-1 flex items-center justify-between min-w-0">
                    <span className="truncate font-semibold tracking-tight">{item.label}</span>
                    {item.historyCount > 0 && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-slate-100/90 text-slate-600 group-hover:bg-white group-hover:text-emerald-800 transition">
                        {item.historyCount}
                      </span>
                    )}
                  </div>
                ) : (
                  /* Dot indicator in collapsed rail */
                  isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-5 bg-emerald-600 rounded-r" />
                  )
                )}
              </Link>
            );
          })}
        </div>

        {/* History Explorer Section (when open) */}
        {isSidebarOpen && (
          <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
            {/* History Header */}
            <div className="flex items-center justify-between px-3.5 pt-3 pb-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <div className="flex items-center gap-1.5 text-slate-700">
                <History className="w-3.5 h-3.5 text-emerald-700" />
                <span>{t(language, "sessionRecords")}</span>
              </div>
              <button
                onClick={() => clearHistory(activeTab)}
                className="text-[10px] text-slate-400 hover:text-red-600 transition flex items-center gap-1 normal-case font-medium hover:bg-red-50 px-2 py-0.5 rounded cursor-pointer"
                title="Clear current tab history"
              >
                <Trash2 className="w-3 h-3" />
                <span>{t(language, "clear")}</span>
              </button>
            </div>

            {/* History Tab Segment Control */}
            <div className="flex items-center gap-1 px-3 pb-2.5">
              {[
                { id: "chat", label: t(language, "chatTab"), count: chatHistory.length },
                { id: "classification", label: t(language, "classifyTab"), count: classificationHistory.length },
                { id: "prior_art", label: t(language, "priorArtTab"), count: priorArtHistory.length },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 py-1.5 px-1.5 text-[11px] font-semibold rounded-lg transition-all text-center cursor-pointer ${
                    activeTab === tab.id
                      ? "bg-emerald-100 text-emerald-900 font-bold shadow-2xs"
                      : "text-slate-500 hover:bg-slate-100 hover:text-slate-800"
                  }`}
                >
                  {tab.label} <span className="opacity-75 text-[10px]">({tab.count})</span>
                </button>
              ))}
            </div>

            {/* History Items Scroll Area */}
            <div className="flex-1 overflow-y-auto px-3 pb-4 space-y-2">
              {/* CHAT TAB HISTORY */}
              {activeTab === "chat" && (
                <>
                  {chatHistory.length === 0 ? (
                    <div className="text-center py-10 px-4 text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
                      <MessageSquare className="w-6 h-6 mx-auto mb-2 text-slate-300" />
                      No recent chat queries.<br />Ask any Ayurveda IP question!
                    </div>
                  ) : (
                    chatHistory.map((h, i) => (
                      <Link
                        key={h.id || i}
                        href="/chat"
                        className="block p-2.5 rounded-xl bg-slate-50/90 hover:bg-emerald-50/80 border border-slate-200/70 hover:border-emerald-300 transition-all text-left group shadow-2xs"
                      >
                        <div className="text-xs font-semibold text-slate-800 line-clamp-1 group-hover:text-emerald-800">
                          {h.query || "Legal Query"}
                        </div>
                        <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1.5 pt-1 border-t border-slate-200/50">
                          <span className="font-mono text-emerald-700 bg-emerald-100/60 px-1.5 py-0.2 rounded font-semibold uppercase">
                            {h.jurisdiction || "INDIA"}
                          </span>
                          <span className="flex items-center gap-1">
                            <Clock className="w-2.5 h-2.5" />
                            {h.timestamp ? new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "Just now"}
                          </span>
                        </div>
                      </Link>
                    ))
                  )}
                </>
              )}

              {/* CLASSIFICATION TAB HISTORY */}
              {activeTab === "classification" && (
                <>
                  {classificationHistory.length === 0 ? (
                    <div className="text-center py-10 px-4 text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
                      <Scale className="w-6 h-6 mx-auto mb-2 text-slate-300" />
                      No classification history.<br />Run the 6-tier wizard!
                    </div>
                  ) : (
                    classificationHistory.map((h, i) => (
                      <Link
                        key={h.id || i}
                        href="/classify"
                        className="block p-2.5 rounded-xl bg-slate-50/90 hover:bg-amber-50/80 border border-slate-200/70 hover:border-amber-300 transition-all text-left group shadow-2xs"
                      >
                        <div className="text-xs font-semibold text-slate-800 line-clamp-1 group-hover:text-amber-800">
                          {h.product_name || h.category_name_en || "Product Classification"}
                        </div>
                        <div className="text-[10px] text-amber-800 font-medium mt-0.5 line-clamp-1">
                          {h.category_name_en}
                        </div>
                        <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1.5 pt-1 border-t border-slate-200/50">
                          <span className="font-semibold text-amber-700">{h.confidence} Confidence</span>
                          <span>{h.timestamp ? new Date(h.timestamp).toLocaleDateString() : ""}</span>
                        </div>
                      </Link>
                    ))
                  )}
                </>
              )}

              {/* PRIOR ART TAB HISTORY */}
              {activeTab === "prior_art" && (
                <>
                  {priorArtHistory.length === 0 ? (
                    <div className="text-center py-10 px-4 text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
                      <Microscope className="w-6 h-6 mx-auto mb-2 text-slate-300" />
                      No prior-art searches.<br />Search AFI monographs!
                    </div>
                  ) : (
                    priorArtHistory.map((h, i) => (
                      <Link
                        key={h.id || i}
                        href="/search"
                        className="block p-2.5 rounded-xl bg-slate-50/90 hover:bg-teal-50/80 border border-slate-200/70 hover:border-teal-300 transition-all text-left group shadow-2xs"
                      >
                        <div className="text-xs font-semibold text-slate-800 line-clamp-1 group-hover:text-teal-800">
                          {Array.isArray(h.ingredients) ? h.ingredients.join(", ") : h.query || "Formulation Search"}
                        </div>
                        <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1.5 pt-1 border-t border-slate-200/50">
                          <span className="text-teal-700 font-semibold bg-teal-50 px-1.5 py-0.2 rounded">
                            {h.match_count || 0} Matches
                          </span>
                          <span>{h.timestamp ? new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ""}</span>
                        </div>
                      </Link>
                    ))
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* Bottom Branding / Status */}
        {isSidebarOpen && (
          <div className="p-3 border-t border-emerald-100/70 bg-gradient-to-r from-emerald-50/50 to-teal-50/30 text-[11px] text-slate-500 flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <img src="/ayura_logo.png" alt="AYURA" className="w-4 h-4 object-contain rounded-xs" />
              <span className="font-semibold text-slate-700">AYURA IP-SAKTI</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span className="text-[10px] font-mono text-emerald-800 bg-white border border-emerald-200/80 px-1.5 py-0.5 rounded shadow-2xs font-semibold">
                v1.0 Ready
              </span>
            </div>
          </div>
        )}
      </aside>
    </>
  );
};
