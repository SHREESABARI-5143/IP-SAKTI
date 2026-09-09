'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Shield, 
  Sparkles, 
  FileText, 
  CheckCircle2, 
  Layers, 
  Package, 
  Lock, 
  Database, 
  Sliders,
  Globe2,
  ChevronDown,
  Menu,
  X,
  Languages
} from 'lucide-react';
import { useAppStore } from '@/lib/store';
import { translations } from '@/lib/translations';

export const Navbar: React.FC = () => {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { 
    jurisdiction, 
    setJurisdiction, 
    selectedCountry, 
    setSelectedCountry, 
    language, 
    setLanguage 
  } = useAppStore();

  const t = translations[language] || translations.en;

  const navLinks = [
    { href: '/', label: 'Research Copilot', shortLabel: 'Copilot', icon: Sparkles },
    { href: '/classify', label: 'Formulation Classifier', shortLabel: 'Classifier', icon: Layers },
    { href: '/abs-helper', label: 'ABS Compliance', shortLabel: 'ABS', icon: CheckCircle2 },
    { href: '/ip-strategy', label: 'IP Strategy Matrix', shortLabel: 'IP Matrix', icon: FileText },
    { href: '/products', label: 'Product Workspace', shortLabel: 'Products', icon: Package },
    { href: '/documents', label: 'Private Vault', shortLabel: 'Vault', icon: Lock },
    { href: '/sources', label: 'Statutory Sources', shortLabel: 'Registry', icon: Database },
    { href: '/admin', label: 'Admin Console', shortLabel: 'Admin', icon: Sliders },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl border-b border-slate-200/80 shadow-xs">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-2 sm:gap-4">
          
          {/* Brand Logo */}
          <Link href="/" className="flex items-center gap-2.5 flex-shrink-0 group py-1">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-900 via-teal-800 to-emerald-600 flex items-center justify-center text-white shadow-md shadow-teal-900/15 group-hover:scale-105 transition-transform">
              <Shield className="w-5 h-5 text-amber-300" />
            </div>
            <div className="flex flex-col whitespace-nowrap">
              <div className="flex items-center gap-1.5 leading-none">
                <span className="font-extrabold text-slate-900 text-base sm:text-lg tracking-tight">IP-SAKTI</span>
                <span className="px-1.5 py-0.5 bg-gradient-to-r from-teal-50 to-emerald-50 text-teal-800 border border-teal-200/80 text-[10px] font-bold rounded-md uppercase tracking-wider">
                  Sahayak
                </span>
              </div>
              <span className="text-[10px] text-slate-500 font-semibold tracking-tight mt-0.5">
                Ayurvedic IP & Regulatory AI
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden xl:flex items-center gap-1 bg-slate-100/70 p-1 rounded-xl border border-slate-200/60">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-white text-teal-900 shadow-xs border border-slate-200/80 font-bold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 flex-shrink-0 ${isActive ? 'text-teal-700' : 'text-slate-400'}`} />
                  <span>{link.shortLabel}</span>
                </Link>
              );
            })}
          </nav>

          {/* Medium Screen Compact Navigation (dropdown or scrollable) */}
          <nav className="hidden md:flex xl:hidden items-center gap-1 overflow-x-auto py-1 scrollbar-none max-w-[420px]">
            {navLinks.slice(0, 5).map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-1 px-2 py-1 rounded-md text-xs font-semibold whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-teal-50 text-teal-900 border border-teal-200 font-bold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                  title={link.label}
                >
                  <Icon className={`w-3.5 h-3.5 flex-shrink-0 ${isActive ? 'text-teal-700' : 'text-slate-400'}`} />
                  <span>{link.shortLabel}</span>
                </Link>
              );
            })}
            <Link
              href="/sources"
              className="text-xs text-slate-500 hover:text-teal-800 font-semibold px-1.5 py-1 whitespace-nowrap"
            >
              More...
            </Link>
          </nav>

          {/* Right Controls: Jurisdiction Switcher + Language Selector */}
          <div className="flex items-center gap-2 flex-shrink-0">
            
            {/* Jurisdiction Toggle Switch */}
            <div className="flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200/80 shadow-2xs">
              <button
                onClick={() => setJurisdiction('India')}
                className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-bold rounded-lg transition-all ${
                  jurisdiction === 'India'
                    ? 'bg-gradient-to-r from-teal-800 to-teal-700 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <span>🇮🇳</span>
                <span className="hidden sm:inline">India</span>
              </button>
              <button
                onClick={() => setJurisdiction('International')}
                className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-bold rounded-lg transition-all ${
                  jurisdiction === 'International'
                    ? 'bg-gradient-to-r from-teal-800 to-teal-700 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <span>🌐</span>
                <span className="hidden sm:inline">International</span>
              </button>
            </div>

            {/* Country Selector for International Mode */}
            {jurisdiction === 'International' && (
              <div className="relative">
                <select
                  value={selectedCountry}
                  onChange={(e) => setSelectedCountry(e.target.value)}
                  className="appearance-none bg-white border border-slate-200 text-slate-800 text-xs font-bold rounded-lg pl-2.5 pr-7 py-1.5 shadow-2xs hover:border-teal-400 focus:outline-none focus:ring-1 focus:ring-teal-600 cursor-pointer"
                >
                  <option value="USA">🇺🇸 USA (DSHEA)</option>
                  <option value="EU">🇪🇺 EU (THMPD)</option>
                  <option value="UK">🇬🇧 UK (MHRA)</option>
                  <option value="Japan">🇯🇵 Japan (FOSHU)</option>
                  <option value="Australia">🇦🇺 Australia (TGA)</option>
                  <option value="UAE">🇦🇪 UAE (MOHAP)</option>
                </select>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
            )}

            {/* Language Segmented Control */}
            <div className="flex items-center bg-slate-100/90 p-0.5 rounded-lg border border-slate-200/80">
              <button
                onClick={() => setLanguage('en')}
                title="English"
                className={`px-2 py-1 text-xs font-bold rounded-md transition-all ${
                  language === 'en' ? 'bg-white text-teal-900 shadow-2xs' : 'text-slate-500 hover:text-slate-800'
                }`}
              >
                EN
              </button>
              <button
                onClick={() => setLanguage('hi')}
                title="हिन्दी"
                className={`px-2 py-1 text-xs font-bold rounded-md transition-all ${
                  language === 'hi' ? 'bg-white text-teal-900 shadow-2xs' : 'text-slate-500 hover:text-slate-800'
                }`}
              >
                हिन्दी
              </button>
              <button
                onClick={() => setLanguage('ta')}
                title="தமிழ்"
                className={`px-2 py-1 text-xs font-bold rounded-md transition-all ${
                  language === 'ta' ? 'bg-white text-teal-900 shadow-2xs' : 'text-slate-500 hover:text-slate-800'
                }`}
              >
                தமிழ்
              </button>
            </div>

            {/* Mobile Menu Hamburger */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 md:hidden"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white/98 px-4 py-3 space-y-1 shadow-lg">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold ${
                  isActive
                    ? 'bg-teal-50 text-teal-800 font-bold border border-teal-200'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-teal-700' : 'text-slate-400'}`} />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
};
