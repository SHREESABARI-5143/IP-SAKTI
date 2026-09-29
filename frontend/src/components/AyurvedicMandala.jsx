import React from "react";
import { TulsiLeafIcon } from "./AyurvedicIcons";

export const AyurvedicMandala = ({ className = "" }) => {
  return (
    <div className={`pointer-events-none overflow-hidden ${className}`}>
      {/* ── Central Vedic Sacred Geometry Mandala ── */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[580px] h-[580px] sm:w-[720px] sm:h-[720px] opacity-[0.16] animate-mandala-slow">
        <svg viewBox="0 0 400 400" className="w-full h-full text-emerald-800" fill="none">
          <defs>
            <linearGradient id="mandalaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#059669" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#10b981" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#d97706" stopOpacity="0.7" />
            </linearGradient>
          </defs>

          {/* Outer circle */}
          <circle cx="200" cy="200" r="190" stroke="url(#mandalaGrad)" strokeWidth="1" strokeDasharray="4 4" />
          <circle cx="200" cy="200" r="175" stroke="url(#mandalaGrad)" strokeWidth="1.2" />
          <circle cx="200" cy="200" r="150" stroke="url(#mandalaGrad)" strokeWidth="0.8" strokeDasharray="2 3" />

          {/* 12-petaled sacred lotus array */}
          {[...Array(12)].map((_, i) => {
            const rot = i * 30;
            return (
              <g key={i} transform={`rotate(${rot} 200 200)`}>
                {/* Outer petal */}
                <path
                  d="M200 25 C185 80 185 130 200 160 C215 130 215 80 200 25 Z"
                  stroke="url(#mandalaGrad)"
                  strokeWidth="1.2"
                />
                {/* Inner petal point */}
                <path
                  d="M200 60 C192 100 192 130 200 150 C208 130 208 100 200 60 Z"
                  stroke="url(#mandalaGrad)"
                  strokeWidth="0.8"
                />
                <circle cx="200" cy="25" r="3" fill="#059669" fillOpacity="0.4" />
              </g>
            );
          })}

          {/* Interlocking Tridosha Triangles */}
          <polygon points="200,60 321,270 79,270" stroke="url(#mandalaGrad)" strokeWidth="1.2" />
          <polygon points="200,340 79,130 321,130" stroke="url(#mandalaGrad)" strokeWidth="1.2" />

          {/* Concentric inner circles */}
          <circle cx="200" cy="200" r="85" stroke="url(#mandalaGrad)" strokeWidth="1" />
          <circle cx="200" cy="200" r="50" stroke="url(#mandalaGrad)" strokeWidth="1.2" strokeDasharray="3 3" />
          <circle cx="200" cy="200" r="22" stroke="url(#mandalaGrad)" strokeWidth="1.5" />
          <circle cx="200" cy="200" r="6" fill="#059669" fillOpacity="0.6" />
        </svg>
      </div>

      {/* ── Floating Sacred Botanical Ayurvedic Leaves ── */}
      {/* Leaf 1: Top Left */}
      <div className="absolute top-[18%] left-[8%] animate-leaf-drift-1 opacity-60 text-emerald-600">
        <TulsiLeafIcon className="w-8 h-8 drop-shadow-xs" />
      </div>

      {/* Leaf 2: Top Right */}
      <div className="absolute top-[14%] right-[10%] animate-leaf-drift-2 opacity-50 text-teal-600" style={{ animationDelay: "2s" }}>
        <TulsiLeafIcon className="w-10 h-10 rotate-45 drop-shadow-xs" />
      </div>

      {/* Leaf 3: Mid Bottom Left */}
      <div className="absolute bottom-[22%] left-[12%] animate-leaf-drift-2 opacity-45 text-emerald-700" style={{ animationDelay: "4s" }}>
        <TulsiLeafIcon className="w-7 h-7 -rotate-30 drop-shadow-xs" />
      </div>

      {/* Leaf 4: Bottom Right */}
      <div className="absolute bottom-[28%] right-[14%] animate-leaf-drift-1 opacity-55 text-emerald-600" style={{ animationDelay: "1s" }}>
        <TulsiLeafIcon className="w-9 h-9 rotate-12 drop-shadow-xs" />
      </div>
    </div>
  );
};
