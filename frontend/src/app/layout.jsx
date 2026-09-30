import { Inter, Manrope } from "next/font/google";
import "./globals.css";
import { AppProvider } from "@/context/AppContext";

/* Inter — body, UI labels, buttons, nav, small text */
const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-inter",
  display: "swap",
});

/* Manrope — hero headings, section headings, sub-headings */
const manrope = Manrope({
  subsets: ["latin"],
  weight: ["600", "700", "800"],
  variable: "--font-manrope",
  display: "swap",
});

export const metadata = {
  title: "AYURA — IP-SAKTI Sahayak | Ministry of Ayush IP & Regulatory AI Intelligence",
  description:
    "Source-cited, jurisdiction-aware AI assistant, classical prior-art search, and statutory product classification engine for the Ayurvedic medicine sector.",
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/ayura_logo.png", type: "image/png" },
    ],
    shortcut: "/favicon.ico",
    apple: "/ayura_logo.png",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${manrope.variable}`}>
      <body className="min-h-screen bg-white text-slate-900 flex flex-col antialiased selection:bg-emerald-100 selection:text-emerald-900 font-inter">
        <AppProvider>
          {children}
        </AppProvider>
      </body>
    </html>
  );
}

