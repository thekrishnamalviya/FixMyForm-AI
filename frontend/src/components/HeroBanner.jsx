import React from 'react';
import { Sparkles, ShieldCheck, Languages, CheckSquare, Calendar } from 'lucide-react';

export default function HeroBanner() {
  return (
    <div className="relative pt-10 pb-6 text-center max-w-4xl mx-auto px-4">
      
      {/* Badge */}
      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-4 backdrop-blur-sm">
        <Sparkles className="h-3.5 w-3.5 text-indigo-400" />
        <span>Gemma 4 Document Intelligence Architecture</span>
      </div>

      {/* Main Headline */}
      <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight font-['Outfit']">
        Turn Confusing Forms into{' '}
        <span className="bg-gradient-to-r from-indigo-400 via-violet-400 to-cyan-400 bg-clip-text text-transparent">
          Crystal-Clear Action Steps
        </span>
      </h1>

      {/* Subhead */}
      <p className="mt-4 text-sm sm:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
        Upload any government, admission, scholarship, employment, or visa form. 
        Detect explicitly stated deadlines, get bilingual explanations in simple English &amp; Hinglish, 
        and check every requirement before you submit.
      </p>

      {/* Feature Pills */}
      <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-3 mt-6 text-xs text-slate-300">
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
          <Calendar className="h-3.5 w-3.5 text-rose-400" />
          <span>Explicit Source Deadlines</span>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
          <Languages className="h-3.5 w-3.5 text-indigo-400" />
          <span>Simple English + Hinglish</span>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
          <CheckSquare className="h-3.5 w-3.5 text-emerald-400" />
          <span>Missing-Info Checklist</span>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
          <ShieldCheck className="h-3.5 w-3.5 text-cyan-400" />
          <span>Zero Hallucinations</span>
        </div>
      </div>

    </div>
  );
}
