import React from 'react';
import { ListOrdered, AlertTriangle, Languages } from 'lucide-react';

export default function InstructionsSection({ instructions, languageMode }) {
  if (!instructions || instructions.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ListOrdered className="h-5 w-5 text-indigo-400" />
          <h3 className="text-lg font-bold text-white tracking-tight font-['Outfit']">
            Step-by-Step Form Instructions ({instructions.length})
          </h3>
        </div>
        <span className="text-xs text-slate-400 flex items-center gap-1">
          <Languages className="h-3.5 w-3.5 text-indigo-400" />
          <span>Bilingual: Simple English & Hinglish</span>
        </span>
      </div>

      <div className="space-y-4">
        {instructions.map((step) => (
          <div
            key={step.step_number}
            className="glass-card rounded-xl p-5 border border-slate-800/90 hover:border-slate-700 transition-all"
          >
            {/* Step header */}
            <div className="flex items-start gap-3 mb-3">
              <div className="h-7 w-7 rounded-lg bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                {step.step_number}
              </div>
              <div className="flex-1">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                  <h4 className="text-base font-bold text-slate-100">
                    {step.title}
                  </h4>
                  {step.source_reference && (
                    <span className="text-[10px] text-slate-400 font-mono self-start sm:self-auto">
                      Ref: {step.source_reference}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Bilingual explanations */}
            {languageMode === 'dual' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                {/* English */}
                <div className="p-3.5 rounded-lg bg-slate-900/90 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-indigo-300 font-semibold text-xs mb-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                    Simple English
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {step.english_explanation}
                  </p>
                </div>

                {/* Hinglish */}
                <div className="p-3.5 rounded-lg bg-slate-900/90 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-cyan-300 font-semibold text-xs mb-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                    हिंदी / Hinglish
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed font-sans">
                    {step.hinglish_explanation}
                  </p>
                </div>
              </div>
            ) : languageMode === 'hinglish' ? (
              <div className="p-3.5 rounded-lg bg-slate-900/90 border border-slate-800/80 mb-3">
                <div className="flex items-center gap-1.5 text-cyan-300 font-semibold text-xs mb-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                  हिंदी / Hinglish
                </div>
                <p className="text-sm text-slate-200 leading-relaxed">
                  {step.hinglish_explanation}
                </p>
              </div>
            ) : (
              <div className="p-3.5 rounded-lg bg-slate-900/90 border border-slate-800/80 mb-3">
                <div className="flex items-center gap-1.5 text-indigo-300 font-semibold text-xs mb-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                  Simple English
                </div>
                <p className="text-sm text-slate-200 leading-relaxed">
                  {step.english_explanation}
                </p>
              </div>
            )}

            {/* Critical warning callout */}
            {step.critical_warning && (
              <div className="flex items-start gap-2 p-3 rounded-lg bg-amber-500/10 border border-amber-500/25 text-amber-200 text-xs">
                <AlertTriangle className="h-4 w-4 shrink-0 text-amber-400 mt-0.5" />
                <div>
                  <span className="font-semibold text-amber-300 mr-1">
                    Crucial Warning:
                  </span>
                  <span>{step.critical_warning}</span>
                </div>
              </div>
            )}

          </div>
        ))}
      </div>
    </div>
  );
}
