import React from "react";
import { TulsiLeafIcon } from "./AyurvedicIcons";

export const AyurvedicMandala = ({ className = "" }) => {
  return (
    <div className={`pointer-events-none overflow-hidden ${className}`}>
      {/* ── Central Vedic Sacred Geometry Mandala ── */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[520px] h-[520px] sm:w-[620px] sm:h-[620px] md:w-[680px] md:h-[680px] opacity-[0.36] sm:opacity-[0.40] animate-mandala-slow">
        <svg viewBox="0 0 400 400" className="w-full h-full" fill="none">
          <defs>
            {/* Luminous Vedic Emerald-to-Gold Gradient */}
            <linearGradient id="mandalaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#059669" stopOpacity="0.95" />
              <stop offset="35%" stopColor="#10b981" stopOpacity="0.9" />
              <stop offset="70%" stopColor="#f59e0b" stopOpacity="0.95" />
              <stop offset="100%" stopColor="#ea580c" stopOpacity="0.85" />
            </linearGradient>

            {/* Sacred Saffron & Gold Radial Gradient */}
            <radialGradient id="mandalaCoreGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#fbbf24" stopOpacity="0.8" />
              <stop offset="60%" stopColor="#059669" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#047857" stopOpacity="0" />
            </radialGradient>

            {/* Delicate Petal Watercolor Fill */}
            <linearGradient id="petalFillGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.14" />
              <stop offset="50%" stopColor="#10b981" stopOpacity="0.10" />
              <stop offset="100%" stopColor="#059669" stopOpacity="0.18" />
            </linearGradient>

            {/* Subtle Mandala Glow Filter */}
            <filter id="mandalaGlow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="0" stdDeviation="2.5" floodColor="#10b981" floodOpacity="0.25" />
            </filter>
          </defs>

          {/* Glowing central halo */}
          <circle cx="200" cy="200" r="140" fill="url(#mandalaCoreGrad)" />

          {/* Outer circle rings with rich color */}
          <circle cx="200" cy="200" r="192" stroke="url(#mandalaGrad)" strokeWidth="1.2" strokeDasharray="5 5" />
          <circle cx="200" cy="200" r="178" stroke="url(#mandalaGrad)" strokeWidth="1.8" filter="url(#mandalaGlow)" />
          <circle cx="200" cy="200" r="154" stroke="url(#mandalaGrad)" strokeWidth="1.2" strokeDasharray="3 4" />

          {/* 12-petaled sacred lotus array with rich color and soft fill */}
          {[...Array(12)].map((_, i) => {
            const rot = i * 30;
            return (
              <g key={i} transform={`rotate(${rot} 200 200)`}>
                {/* Outer petal with soft warm fill */}
                <path
                  d="M200 25 C185 80 185 130 200 160 C215 130 215 80 200 25 Z"
                  stroke="url(#mandalaGrad)"
                  strokeWidth="1.6"
                  fill="url(#petalFillGrad)"
                />
                {/* Inner petal point */}
                <path
                  d="M200 60 C192 100 192 130 200 150 C208 130 208 100 200 60 Z"
                  stroke="url(#mandalaGrad)"
                  strokeWidth="1.1"
                />
                {/* Golden Bindu Petal Accent */}
                <circle cx="200" cy="25" r="3.5" fill="#f59e0b" fillOpacity="0.85" />
              </g>
            );
          })}

          {/* Interlocking Tridosha Triangles in vivid gradient */}
          <polygon points="200,60 321,270 79,270" stroke="url(#mandalaGrad)" strokeWidth="1.6" />
          <polygon points="200,340 79,130 321,130" stroke="url(#mandalaGrad)" strokeWidth="1.6" />

          {/* Concentric inner circles & sacred bindu */}
          <circle cx="200" cy="200" r="88" stroke="url(#mandalaGrad)" strokeWidth="1.4" />
          <circle cx="200" cy="200" r="54" stroke="url(#mandalaGrad)" strokeWidth="1.6" strokeDasharray="4 4" />
          <circle cx="200" cy="200" r="24" stroke="url(#mandalaGrad)" strokeWidth="2" />
          <circle cx="200" cy="200" r="8" fill="#f59e0b" fillOpacity="0.85" />
          <circle cx="200" cy="200" r="3.5" fill="#047857" />
        </svg>
      </div>

      {/* ── Floating Sacred Botanical Ayurvedic Leaves with Enhanced Color ── */}
      {/* Leaf 1: Top Left - Vibrant Emerald */}
      <div className="absolute top-[18%] left-[8%] animate-leaf-drift-1 opacity-75 text-emerald-500 drop-shadow-[0_2px_8px_rgba(16,185,129,0.3)]">
        <TulsiLeafIcon className="w-8 h-8" />
      </div>

      {/* Leaf 2: Top Right - Sacred Amber Gold */}
      <div className="absolute top-[14%] right-[10%] animate-leaf-drift-2 opacity-70 text-amber-500 drop-shadow-[0_2px_8px_rgba(245,158,11,0.3)]" style={{ animationDelay: "2s" }}>
        <TulsiLeafIcon className="w-10 h-10 rotate-45" />
      </div>

      {/* Leaf 3: Mid Bottom Left - Rich Teal */}
      <div className="absolute bottom-[22%] left-[12%] animate-leaf-drift-2 opacity-65 text-teal-600 drop-shadow-[0_2px_8px_rgba(13,148,136,0.3)]" style={{ animationDelay: "4s" }}>
        <TulsiLeafIcon className="w-7 h-7 -rotate-30" />
      </div>

      {/* Leaf 4: Bottom Right - Vibrant Green */}
      <div className="absolute bottom-[28%] right-[14%] animate-leaf-drift-1 opacity-75 text-emerald-600 drop-shadow-[0_2px_8px_rgba(5,150,105,0.3)]" style={{ animationDelay: "1s" }}>
        <TulsiLeafIcon className="w-9 h-9 rotate-12" />
      </div>
    </div>
  );
};
