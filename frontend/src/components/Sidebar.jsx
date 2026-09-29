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
  Leaf
} from "lucide-react";
import { useApp } from "@/context/AppContext";

export const Sidebar = () => {
  const pathname = usePathname();
  const {
    isSidebarOpen,
    toggleSidebar,
    chatHistory = [],
    classificationHistory = [],
    priorArtHistory = [],
    clearHistory
  } = useApp();

  const [activeTab, setActiveTab] = useState("chat"); // 'chat' | 'classification' | 'prior_art'

  const navItems = [
    {
      label: "AI Legal Assistant",
      href: "/chat",
      icon: Sparkles,
      color: "text-emerald-700 bg-emerald-50",
      activeBg: "bg-emerald-100/80 text-emerald-900 font-bold border-emerald-300",
      historyCount: chatHistory.length,
      tabId: "chat"
    },
    {
      label: "Product Classifier",
      href: "/classify",
      icon: Scale,
      color: "text-amber-700 bg-amber-50",
      activeBg: "bg-amber-100/80 text-amber-900 font-bold border-amber-300",
      historyCount: classificationHistory.length,
      tabId: "classification"
    },
    {
      label: "Prior-Art Lookup",
      href: "/search",
      icon: Microscope,
      color: "text-teal-700 bg-teal-50",
      activeBg: "bg-teal-100/80 text-teal-900 font-bold border-teal-300",
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
          className="fixed inset-0 bg-black/20 backdrop-blur-xs z-30 lg:hidden"
        />
      )}

      {/* Main Sidebar Panel */}
      <aside
        className={`fixed lg:sticky top-16 left-0 z-30 h-[calc(100vh-4rem)] bg-white/95 backdrop-blur-md border-r border-emerald-100/80 shadow-sm transition-all duration-300 ease-in-out flex flex-col ${
          isSidebarOpen
            ? "w-72 sm:w-80 translate-x-0"
            : "w-0 lg:w-16 -translate-x-full lg:translate-x-0 overflow-hidden"
        }`}
      >
        {/* Top Control Rail */}
        <div className="p-3 border-b border-emerald-100/60 flex items-center justify-between gap-2">
          {isSidebarOpen ? (
            <>
              <Link
                href="/chat"
                className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white text-xs font-bold shadow-xs transition-all hover:shadow"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>New Session</span>
              </Link>
              <button
                onClick={toggleSidebar}
                className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-emerald-50 transition"
                title="Collapse Sidebar"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
            </>
          ) : (
            <button
              onClick={toggleSidebar}
              className="w-full flex items-center justify-center p-2 rounded-xl text-emerald-700 hover:bg-emerald-50 transition"
              title="Expand Sidebar"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Primary Navigation Modules */}
        <div className="p-2.5 space-y-1.5 border-b border-emerald-100/60">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setActiveTab(item.tabId)}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all text-xs ${
                  isActive
                    ? `${item.activeBg} shadow-xs`
                    : "border-transparent hover:bg-slate-50 text-slate-700 hover:text-slate-900"
                }`}
                title={!isSidebarOpen ? item.label : undefined}
              >
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                    isActive ? "bg-white shadow-2xs" : item.color
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>

                {isSidebarOpen && (
                  <div className="flex-1 flex items-center justify-between min-w-0">
                    <span className="truncate font-medium">{item.label}</span>
                    {item.historyCount > 0 && (
                      <span className="px-1.5 py-0.5 rounded-full text-[10px] font-mono bg-slate-100 text-slate-600">
                        {item.historyCount}
                      </span>
                    )}
                  </div>
                )}
              </Link>
            );
          })}
        </div>

        {/* History Explorer Section (when open) */}
        {isSidebarOpen && (
          <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
            {/* History Tabs */}
            <div className="flex items-center justify-between px-3 pt-3 pb-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <div className="flex items-center gap-1.5">
                <History className="w-3.5 h-3.5 text-emerald-700" />
                <span>History Log</span>
              </div>
              <button
                onClick={() => clearHistory(activeTab)}
                className="text-[10px] text-slate-400 hover:text-red-600 transition flex items-center gap-1 normal-case font-normal"
                title="Clear current tab history"
              >
                <Trash2 className="w-3 h-3" />
                <span>Clear</span>
              </button>
            </div>

            {/* History Tab Buttons */}
            <div className="flex items-center gap-1 px-2.5 pb-2">
              {[
                { id: "chat", label: "Chat", count: chatHistory.length },
                { id: "classification", label: "Classify", count: classificationHistory.length },
                { id: "prior_art", label: "Prior-Art", count: priorArtHistory.length },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 py-1 px-1.5 text-[11px] font-semibold rounded-lg transition text-center ${
                    activeTab === tab.id
                      ? "bg-emerald-100 text-emerald-800 shadow-2xs"
                      : "text-slate-500 hover:bg-slate-100"
                  }`}
                >
                  {tab.label} ({tab.count})
                </button>
              ))}
            </div>

            {/* History Items Scroll Area */}
            <div className="flex-1 overflow-y-auto px-2.5 pb-4 space-y-1.5">
              {/* CHAT TAB HISTORY */}
              {activeTab === "chat" && (
                <>
                  {chatHistory.length === 0 ? (
                    <div className="text-center py-8 text-xs text-slate-400">
                      No recent chat queries.<br />Start asking legal questions!
                    </div>
                  ) : (
                    chatHistory.map((h, i) => (
                      <Link
                        key={h.id || i}
                        href="/chat"
                        className="block p-2.5 rounded-xl bg-slate-50/80 hover:bg-emerald-50/70 border border-slate-200/80 hover:border-emerald-200 transition text-left group"
                      >
                        <div className="text-xs font-semibold text-slate-800 line-clamp-1 group-hover:text-emerald-800">
                          {h.query || "Legal Query"}
                        </div>
                        <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                          <span>{h.jurisdiction?.toUpperCase() || "INDIA"}</span>
                          <span>{h.timestamp ? new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ""}</span>
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
                    <div className="text-center py-8 text-xs text-slate-400">
                      No classification history.<br />Run the 6-tier wizard!
                    </div>
                  ) : (
                    classificationHistory.map((h, i) => (
                      <Link
                        key={h.id || i}
                        href="/classify"
                        className="block p-2.5 rounded-xl bg-slate-50/80 hover:bg-amber-50/70 border border-slate-200/80 hover:border-amber-200 transition text-left group"
                      >
                        <div className="text-xs font-semibold text-slate-800 line-clamp-1 group-hover:text-amber-800">
                          {h.product_name || h.category_name_en || "Product Classification"}
                        </div>
                        <div className="text-[10px] text-amber-700 font-medium mt-0.5">
                          {h.category_name_en}
                        </div>
                        <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                          <span>{h.confidence} Confidence</span>
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
                    <div className="text-center py-8 text-xs text-slate-400">
                      No prior-art searches.<br />Search AFI formulations!
                    </div>
                  ) : (
                    priorArtHistory.map((h, i) => (
                      <Link
                        key={h.id || i}
                        href="/search"
                        className="block p-2.5 rounded-xl bg-slate-50/80 hover:bg-teal-50/70 border border-slate-200/80 hover:border-teal-200 transition text-left group"
                      >
                        <div className="text-xs font-semibold text-slate-800 line-clamp-1 group-hover:text-teal-800">
                          {Array.isArray(h.ingredients) ? h.ingredients.join(", ") : h.query || "Formulation Search"}
                        </div>
                        <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                          <span className="text-teal-700 font-medium">{h.match_count || 0} Matches</span>
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
          <div className="p-3 border-t border-emerald-100/60 bg-emerald-50/40 text-[11px] text-slate-500 flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <Leaf className="w-3.5 h-3.5 text-emerald-600" />
              <span className="font-semibold text-slate-700">AYURA Intelligence</span>
            </div>
            <span className="text-[10px] font-mono text-emerald-800 bg-emerald-100 px-1.5 py-0.5 rounded">
              v1.0
            </span>
          </div>
        )}
      </aside>
    </>
  );
};
