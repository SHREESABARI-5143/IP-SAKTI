'use client';

import React from 'react';
import { Shield, BookOpen, Scale, Award, HeartHandshake } from 'lucide-react';
import Link from 'next/link';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-950 text-slate-300 text-xs border-t border-slate-800/80 mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Col 1: Brand & Purpose */}
          <div className="space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-teal-800 to-emerald-600 flex items-center justify-center text-white shadow-md">
                <Shield className="w-4 h-4 text-amber-300" />
              </div>
              <div>
                <span className="font-extrabold text-white text-sm tracking-tight">IP-SAKTI</span>
                <span className="ml-1 text-[10px] text-teal-400 font-bold uppercase tracking-wider">Sahayak</span>
              </div>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed">
              Source-grounded legal & regulatory intelligence platform for Ayurveda, Siddha, Unani, and traditional knowledge-based bio-innovations.
            </p>
          </div>

          {/* Col 2: Statutory Coverage */}
          <div>
            <h4 className="font-bold text-white mb-3 flex items-center gap-1.5 text-xs uppercase tracking-wider text-teal-400">
              <Scale className="w-4 h-4 text-teal-400" />
              Indian Statutory Acts
            </h4>
            <ul className="space-y-1.5 text-slate-400 text-xs">
              <li>• The Patents Act 1970 (Sec 3(p), 3(d), 10(4))</li>
              <li>• Biological Diversity Act 2002 & 2023</li>
              <li>• Drugs & Cosmetics Act 1940 (Rule 158B)</li>
              <li>• FSSAI Ayurveda Aahar Regulations 2022</li>
              <li>• Trade Marks & GI Act 1999</li>
            </ul>
          </div>

          {/* Col 3: International Coverage */}
          <div>
            <h4 className="font-bold text-white mb-3 flex items-center gap-1.5 text-xs uppercase tracking-wider text-teal-400">
              <Award className="w-4 h-4 text-teal-400" />
              International Treaties
            </h4>
            <ul className="space-y-1.5 text-slate-400 text-xs">
              <li>• WIPO GRATK Treaty (2024)</li>
              <li>• Nagoya Protocol on ABS (CBD)</li>
              <li>• US FDA DSHEA (21 CFR Part 111)</li>
              <li>• EU THMPD Directive (2004/24/EC)</li>
              <li>• UK MHRA & Japan FOSHU Regulations</li>
            </ul>
          </div>

          {/* Col 4: Trust & Facilitation */}
          <div>
            <h4 className="font-bold text-white mb-3 flex items-center gap-1.5 text-xs uppercase tracking-wider text-teal-400">
              <HeartHandshake className="w-4 h-4 text-teal-400" />
              Facilitation Network
            </h4>
            <p className="text-slate-400 text-xs leading-relaxed mb-3">
              Need assistance with patent drafting, NBA Form 3 filing, or licensing?
            </p>
            <Link
              href="/admin"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-teal-300 font-semibold text-xs hover:border-teal-500 transition-colors"
            >
              <span>Facilitator Escalation Portal →</span>
            </Link>
          </div>
        </div>

        {/* Bottom copyright */}
        <div className="border-t border-slate-800/80 mt-8 pt-6 flex flex-col sm:flex-row items-center justify-between text-slate-500 text-xs gap-3">
          <p>© 2026 IP-SAKTI Sahayak Platform • Smart India Hackathon 2026</p>
          <p className="text-slate-500">
            Citation-Grounded AI with Evidence Validation & Safe Abstention
          </p>
        </div>
      </div>
    </footer>
  );
};
