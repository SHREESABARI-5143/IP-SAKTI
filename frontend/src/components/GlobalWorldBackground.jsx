"use client";

import React from "react";
import { Globe, Scale, Shield, FileText } from "lucide-react";

export const GlobalWorldBackground = ({ className = "" }) => {
  return (
    <div className={`pointer-events-none overflow-hidden select-none ${className}`}>
      {/* ── Ambient Pulsing Oceanic & Cyan Nebula Glow Orbs ── */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[540px] h-[540px] sm:w-[640px] sm:h-[640px] rounded-full bg-blue-400/15 blur-[120px] animate-globe-aura pointer-events-none" />
      <div
        className="absolute top-[42%] left-[48%] -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] rounded-full bg-cyan-400/15 blur-[90px] animate-globe-aura pointer-events-none"
        style={{ animationDelay: "4s" }}
      />

      {/* ── Central Pure 3D Spherical Earth Globe (No Orbits, No Floating Text) ── */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] sm:w-[580px] sm:h-[580px] md:w-[640px] md:h-[640px] opacity-[0.88] sm:opacity-[0.92]">
        <svg viewBox="0 0 700 700" className="w-full h-full" fill="none">
          <defs>
            {/* Globe Sphere Shading: Atmospheric rim light from top-left */}
            <radialGradient id="globeSphereGrad" cx="38%" cy="32%" r="65%">
              <stop offset="0%" stopColor="#e0f2fe" stopOpacity="0.45" />
              <stop offset="25%" stopColor="#bae6fd" stopOpacity="0.25" />
              <stop offset="65%" stopColor="#0284c7" stopOpacity="0.12" />
              <stop offset="90%" stopColor="#0369a1" stopOpacity="0.08" />
              <stop offset="100%" stopColor="#0c4a6e" stopOpacity="0.18" />
            </radialGradient>

            {/* Glowing International Cyan-to-Blue Linear Gradient */}
            <linearGradient id="globeBlueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.95" />
              <stop offset="40%" stopColor="#2563eb" stopOpacity="0.9" />
              <stop offset="75%" stopColor="#4f46e5" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.9" />
            </linearGradient>

            {/* Continental Landmass Silhouette Gradient */}
            <linearGradient id="continentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0284c7" stopOpacity="0.32" />
              <stop offset="50%" stopColor="#2563eb" stopOpacity="0.38" />
              <stop offset="100%" stopColor="#38bdf8" stopOpacity="0.30" />
            </linearGradient>

            {/* Glowing Beacon / Rim Filter */}
            <filter id="globeGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor="#38bdf8" floodOpacity="0.6" />
            </filter>

            {/* Globe Sphere Clipping Mask (Radius 185, Center 350, 350) */}
            <clipPath id="globeSphereClip">
              <circle cx="350" cy="350" r="185" />
            </clipPath>
          </defs>

          {/* ── Ambient Planetary Atmospheric Halos ── */}
          <circle cx="350" cy="350" r="198" stroke="url(#globeBlueGrad)" strokeWidth="1.2" strokeOpacity="0.25" strokeDasharray="3 4" />
          <circle cx="350" cy="350" r="190" stroke="#38bdf8" strokeWidth="2" strokeOpacity="0.45" filter="url(#globeGlow)" />

          {/* ── Main Spherical Earth Globe Body ── */}
          <g clipPath="url(#globeSphereClip)">
            {/* Globe Ocean Depth Base */}
            <circle cx="350" cy="350" r="185" fill="url(#globeSphereGrad)" />

            {/* Latitudinal Parallels (Equator, Tropics, Arctic/Antarctic) */}
            {/* Arctic Circle 60°N */}
            <ellipse cx="350" cy="230" rx="135" ry="18" stroke="#38bdf8" strokeWidth="1.1" strokeOpacity="0.35" strokeDasharray="3 3" />
            {/* Tropic of Cancer 23.5°N */}
            <ellipse cx="350" cy="285" rx="172" ry="24" stroke="#60a5fa" strokeWidth="1.2" strokeOpacity="0.45" />
            {/* Equator 0° */}
            <ellipse cx="350" cy="350" rx="185" ry="30" stroke="#2563eb" strokeWidth="1.8" strokeOpacity="0.65" />
            {/* Tropic of Capricorn 23.5°S */}
            <ellipse cx="350" cy="415" rx="172" ry="24" stroke="#60a5fa" strokeWidth="1.2" strokeOpacity="0.45" />
            {/* Antarctic Circle 60°S */}
            <ellipse cx="350" cy="470" rx="135" ry="18" stroke="#38bdf8" strokeWidth="1.1" strokeOpacity="0.35" strokeDasharray="3 3" />

            {/* Longitudinal Meridians */}
            <ellipse cx="350" cy="350" rx="130" ry="185" stroke="#93c5fd" strokeWidth="1" strokeOpacity="0.3" strokeDasharray="4 4" />
            <ellipse cx="350" cy="350" rx="70" ry="185" stroke="#60a5fa" strokeWidth="1.1" strokeOpacity="0.38" />
            <ellipse cx="350" cy="350" rx="20" ry="185" stroke="#3b82f6" strokeWidth="1.2" strokeOpacity="0.45" />
            <line x1="350" y1="165" x2="350" y2="535" stroke="#2563eb" strokeWidth="1.5" strokeOpacity="0.5" />

            {/* ── Seamless Rotating Continents Vector Track ── */}
            <g className="animate-globe-pan" style={{ willChange: "transform" }}>
              {/* Set 1: World Continents */}
              <g transform="translate(0, 0)">
                {/* Europe & Africa */}
                <path
                  d="M320 230 c10 -15 35 -10 40 5 c-5 12 15 22 25 15 c10 10 5 25 -5 32 c-8 15 -18 10 -22 25 c-5 20 8 35 5 50 c-5 18 -15 28 -25 35 c-12 8 -20 -10 -22 -22 c-5 -25 12 -45 5 -65 c-8 -15 2 -32 5 -45 c2 -18 -8 -22 -6 -50 z"
                  fill="url(#continentGrad)"
                  stroke="#38bdf8"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
                {/* Asia & Indian Subcontinent */}
                <path
                  d="M380 220 c25 -15 65 -12 85 5 c18 15 32 35 25 55 c-10 18 -32 20 -40 35 c-8 12 -5 28 -18 35 c-12 6 -15 -8 -22 -15 c-10 12 -18 20 -28 25 c-8 4 -12 -10 -15 -18 c-8 -22 15 -35 12 -52 c-5 -18 -18 -25 -12 -45 c5 -12 8 -18 13 -25 z"
                  fill="url(#continentGrad)"
                  stroke="#60a5fa"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
                {/* India Promontory Accent */}
                <path
                  d="M408 290 c8 12 14 26 10 38 c-4 12 -12 18 -16 22 c-4 -10 -8 -22 -6 -35 c2 -12 8 -18 12 -25 z"
                  fill="#38bdf8"
                  fillOpacity="0.4"
                  stroke="#0284c7"
                  strokeWidth="1"
                />
                {/* Australia */}
                <path
                  d="M470 385 c18 -8 38 2 40 18 c2 16 -12 25 -25 28 c-15 4 -22 -8 -22 -22 c0 -12 2 -20 7 -24 z"
                  fill="url(#continentGrad)"
                  stroke="#38bdf8"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
                {/* Americas */}
                <path
                  d="M170 210 c15 -5 32 10 25 25 c-5 12 -15 18 -12 30 c4 15 18 20 15 35 c-4 18 -22 22 -20 38 c2 18 12 32 10 48 c-4 18 -18 25 -22 38 c-5 15 -14 10 -18 0 c-6 -22 10 -45 8 -65 c-2 -18 -15 -25 -12 -42 c4 -18 20 -22 22 -40 c2 -15 -5 -25 4 -27 z"
                  fill="url(#continentGrad)"
                  stroke="#38bdf8"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
              </g>

              {/* Set 2: Seamless Duplicate shifted by 400px for continuous rotation */}
              <g transform="translate(400, 0)">
                {/* Europe & Africa */}
                <path
                  d="M320 230 c10 -15 35 -10 40 5 c-5 12 15 22 25 15 c10 10 5 25 -5 32 c-8 15 -18 10 -22 25 c-5 20 8 35 5 50 c-5 18 -15 28 -25 35 c-12 8 -20 -10 -22 -22 c-5 -25 12 -45 5 -65 c-8 -15 2 -32 5 -45 c2 -18 -8 -22 -6 -50 z"
                  fill="url(#continentGrad)"
                  stroke="#38bdf8"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
                {/* Asia & Indian Subcontinent */}
                <path
                  d="M380 220 c25 -15 65 -12 85 5 c18 15 32 35 25 55 c-10 18 -32 20 -40 35 c-8 12 -5 28 -18 35 c-12 6 -15 -8 -22 -15 c-10 12 -18 20 -28 25 c-8 4 -12 -10 -15 -18 c-8 -22 15 -35 12 -52 c-5 -18 -18 -25 -12 -45 c5 -12 8 -18 13 -25 z"
                  fill="url(#continentGrad)"
                  stroke="#60a5fa"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
                {/* India Promontory Accent */}
                <path
                  d="M408 290 c8 12 14 26 10 38 c-4 12 -12 18 -16 22 c-4 -10 -8 -22 -6 -35 c2 -12 8 -18 12 -25 z"
                  fill="#38bdf8"
                  fillOpacity="0.4"
                  stroke="#0284c7"
                  strokeWidth="1"
                />
                {/* Australia */}
                <path
                  d="M470 385 c18 -8 38 2 40 18 c2 16 -12 25 -25 28 c-15 4 -22 -8 -22 -22 c0 -12 2 -20 7 -24 z"
                  fill="url(#continentGrad)"
                  stroke="#38bdf8"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
                {/* Americas */}
                <path
                  d="M170 210 c15 -5 32 10 25 25 c-5 12 -15 18 -12 30 c4 15 18 20 15 35 c-4 18 -22 22 -20 38 c2 18 12 32 10 48 c-4 18 -18 25 -22 38 c-5 15 -14 10 -18 0 c-6 -22 10 -45 8 -65 c-2 -18 -15 -25 -12 -42 c4 -18 20 -22 22 -40 c2 -15 -5 -25 4 -27 z"
                  fill="url(#continentGrad)"
                  stroke="#38bdf8"
                  strokeWidth="0.8"
                  strokeOpacity="0.5"
                />
              </g>
            </g>

            {/* Internal Sphere Rim Gradient Overlay for pure spherical glass depth */}
            <circle
              cx="350"
              cy="350"
              r="185"
              stroke="#38bdf8"
              strokeWidth="3.5"
              strokeOpacity="0.4"
              fill="none"
              filter="url(#globeGlow)"
            />
          </g>
        </svg>
      </div>

      {/* ── Floating International Legal & Treaty Icons (Matching India Botanical Leaves Style) ── */}
      {/* Icon 1: Top Left - Global Treaties (Sky Blue) */}
      <div className="absolute top-[18%] left-[8%] animate-leaf-drift-1 opacity-75 text-sky-500 drop-shadow-[0_2px_8px_rgba(14,165,233,0.35)]">
        <Globe className="w-8 h-8" />
      </div>

      {/* Icon 2: Top Right - Legal Balance & Nagoya ABS (Royal Indigo) */}
      <div
        className="absolute top-[14%] right-[10%] animate-leaf-drift-2 opacity-70 text-indigo-500 drop-shadow-[0_2px_8px_rgba(99,102,241,0.35)]"
        style={{ animationDelay: "2s" }}
      >
        <Scale className="w-9 h-9 rotate-12" />
      </div>

      {/* Icon 3: Mid Bottom Left - Defensive Patent Shield (Vibrant Blue) */}
      <div
        className="absolute bottom-[22%] left-[12%] animate-leaf-drift-2 opacity-65 text-blue-600 drop-shadow-[0_2px_8px_rgba(37,99,235,0.35)]"
        style={{ animationDelay: "4s" }}
      >
        <Shield className="w-8 h-8 -rotate-12" />
      </div>

      {/* Icon 4: Bottom Right - Codified Patent Gazette & Treaties (Electric Cyan) */}
      <div
        className="absolute bottom-[28%] right-[14%] animate-leaf-drift-1 opacity-75 text-cyan-500 drop-shadow-[0_2px_8px_rgba(6,182,212,0.35)]"
        style={{ animationDelay: "1s" }}
      >
        <FileText className="w-8 h-8 rotate-12" />
      </div>
    </div>
  );
};
