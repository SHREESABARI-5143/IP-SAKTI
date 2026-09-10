import type { Metadata, Viewport } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { LegalDisclaimerBanner } from '@/components/LegalDisclaimerBanner';
import { SourceDrawer } from '@/components/SourceDrawer';
import { EscalationModal } from '@/components/EscalationModal';

export const metadata: Metadata = {
  title: 'IP-SAKTI Sahayak — Multilingual Ayurvedic IP & Regulatory Intelligence Platform',
  description: 'Citation-grounded AI with evidence validation and safe abstention for Indian & International Patents, Traditional Knowledge (TKDL), ABS (BDA 2023), AYUSH Formulations, and Export Compliance.',
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/favicon.ico',
  },
};

export const viewport: Viewport = {
  themeColor: '#059669',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full scroll-smooth">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&family=Noto+Sans+Tamil:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="IP-SAKTI" />
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
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                  navigator.serviceWorker.register('/sw.js').catch(function(err) {
                    console.log('SW registration skipped:', err);
                  });
                });
              }
            `,
          }}
        />
      </body>
    </html>
  );
}
