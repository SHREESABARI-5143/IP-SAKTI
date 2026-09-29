import React from "react";

// 1. Khalva Yantra (Ayurvedic Mortar & Pestle for herbal preparation)
export const KhalvaIcon = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className={className}>
    {/* Pestle */}
    <path d="M14.5 3.5l-4 8.5" />
    <path d="M13 2.5a1.8 1.8 0 0 1 2.5 2.5l-1 2.2-2.5-1.2 1-3.5z" />
    {/* Mortar bowl */}
    <path d="M3.5 12c0 5 3.5 8 8.5 8s8.5-3 8.5-8H3.5z" />
    {/* Mortar base */}
    <path d="M7.5 20v1.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V20" />
    {/* Mortar rim */}
    <line x1="2.5" y1="12" x2="21.5" y2="12" />
  </svg>
);

// 2. Talapatra / Palm Leaf Manuscript (Codified Classical Texts / Grantha)
export const TalapatraIcon = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className={className}>
    {/* Top manuscript slat */}
    <rect x="3" y="4" width="18" height="4.5" rx="1.5" />
    <circle cx="7" cy="6.25" r="0.75" fill="currentColor" />
    <circle cx="17" cy="6.25" r="0.75" fill="currentColor" />
    {/* Middle manuscript slat */}
    <rect x="3" y="10" width="18" height="4.5" rx="1.5" />
    <circle cx="7" cy="12.25" r="0.75" fill="currentColor" />
    <circle cx="17" cy="12.25" r="0.75" fill="currentColor" />
    {/* Binding cord connecting slats */}
    <line x1="7" y1="2.5" x2="7" y2="21.5" strokeDasharray="1.5 1.5" />
    <line x1="17" y1="2.5" x2="17" y2="21.5" strokeDasharray="1.5 1.5" />
    {/* Bottom manuscript slat */}
    <rect x="3" y="16" width="18" height="4.5" rx="1.5" />
    <circle cx="7" cy="18.25" r="0.75" fill="currentColor" />
    <circle cx="17" cy="18.25" r="0.75" fill="currentColor" />
  </svg>
);

// 3. Tulsi / Sacred Herbal Botanical (Holy Basil Leaf Node)
export const TulsiLeafIcon = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className={className}>
    {/* Main central stem */}
    <path d="M12 22C12 14 12 7 12 2" />
    {/* Top left leaf */}
    <path d="M12 7C9.5 5 6 6 6 8.5c0 2 3.5 3 6 3" />
    {/* Top right leaf */}
    <path d="M12 6C14.5 4 18 5 18 7.5c0 2-3.5 3-6 3" />
    {/* Mid left leaf */}
    <path d="M12 12C8.5 10 4 11.5 4 14.5c0 2.5 4.5 3.5 8 3" />
    {/* Mid right leaf */}
    <path d="M12 11C15.5 9 20 10.5 20 13.5c0 2.5-4.5 3.5-8 3" />
    {/* Seed spike at top */}
    <circle cx="12" cy="2.5" r="1" fill="currentColor" />
  </svg>
);

// 4. Padma / Sacred Lotus (Purity & Ayurvedic Heritage)
export const LotusIcon = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className={className}>
    {/* Central petal */}
    <path d="M12 4c-2 4-2 8 0 12 2-4 2-8 0-12z" />
    {/* Left petal */}
    <path d="M12 16C8 14 4 10 5 7c3 0 6 4 7 9z" />
    {/* Right petal */}
    <path d="M12 16c4-2 8-6 7-9-3 0-6 4-7 9z" />
    {/* Bottom water/leaf base */}
    <path d="M3 19c3 2 6 2 9 0 3 2 6 2 9 0" />
    <path d="M7 21c2.5 1.5 7.5 1.5 10 0" />
  </svg>
);

// 5. Kalash / Amrit Kumbha (Sacred Ayurvedic Formulation Vessel)
export const KalashIcon = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className={className}>
    {/* Coconut / Mango leaves on top */}
    <path d="M12 2l-2 4 4 0-2-4z" />
    <path d="M9 5c-2-1-4 0-4 2 2 1 4 0 4-2z" />
    <path d="M15 5c2-1 4 0 4 2-2 1-4 0-4-2z" />
    {/* Pot rim */}
    <ellipse cx="12" cy="7.5" rx="4.5" ry="1.2" />
    {/* Pot belly */}
    <path d="M7.8 8.5C5 11 5 16 8 18.5h8c3-2.5 3-7.5.2-10" />
    {/* Base */}
    <path d="M9 18.5v1.5a.5.5 0 0 0 .5.5h5a.5.5 0 0 0 .5-.5v-1.5" />
    {/* Sacred Swastika / Thread dot */}
    <circle cx="12" cy="13.5" r="1.2" fill="currentColor" />
  </svg>
);

// 6. Nyaya Scales + Dravyaguna (Legal Protection + Ayurvedic Wisdom)
export const AyurvedaNyayaIcon = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className={className}>
    {/* Pillar & Base */}
    <line x1="12" y1="3" x2="12" y2="20" />
    <path d="M8 20h8" />
    {/* Balance Beam */}
    <path d="M4 6.5h16" />
    <circle cx="12" cy="6.5" r="1.5" />
    {/* Left Pan (Herbal Plant) */}
    <path d="M4 6.5L2 13h4L4 6.5z" />
    <path d="M4 11.5c-1-2 1-3 0-4" />
    {/* Right Pan (Statutory Law Scroll) */}
    <path d="M20 6.5L18 13h4l-2-6.5z" />
    <line x1="19" y1="10" x2="21" y2="10" />
  </svg>
);
