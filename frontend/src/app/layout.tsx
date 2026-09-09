import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { LegalDisclaimerBanner } from '@/components/LegalDisclaimerBanner';
import { SourceDrawer } from '@/components/SourceDrawer';
import { EscalationModal } from '@/components/EscalationModal';

export const metadata: Metadata = {
  title: 'IP-SAKTI Sahayak — Multilingual Ayurvedic IP & Regulatory Intelligence Platform',
  description: 'Citation-grounded AI with evidence validation and safe abstention for Indian & International Patents, Traditional Knowledge (TKDL), ABS (BDA 2023), AYUSH Formulations, and Export Compliance.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link 
          href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" 
          rel="stylesheet" 
        />
      </head>
      <body className="min-h-screen flex flex-col bg-slate-50/70 text-slate-900 selection:bg-teal-600 selection:text-white antialiased font-sans">
        <LegalDisclaimerBanner />
        <Navbar />
        <main className="flex-1 flex flex-col">
          {children}
        </main>
        <Footer />
        <SourceDrawer />
        <EscalationModal />
      </body>
    </html>
  );
}
