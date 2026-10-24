import React from 'react';
import { ShieldAlert, KeyRound } from 'lucide-react';

export default function DemoModeBanner({ 
  onOpenConfig, 
  onSelectSample, 
  activeSampleId 
}) {
  const samplePills = [
    { id: 'passport', label: '🛂 Indian Passport (Form 1)', desc: 'Tatkaal, Annexure E, Address rules' },
    { id: 'scholarship', label: '🎓 NSP Scholarship 2026', desc: '30-Nov cutoff, NPCI bank mapping' },
    { id: 'tax_12bb', label: '💼 Form 12BB Tax & HRA', desc: 'Landlord PAN, 80C & 80D proofs' },
  ];

  return (
    <div className="w-full bg-gradient-to-r from-amber-950/40 via-amber-900/30 to-slate-900 border-b border-amber-500/30 px-4 py-3">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-xs sm:text-sm">
        
        {/* Notice text */}
        <div className="flex items-start sm:items-center gap-2.5">
          <div className="p-1 rounded-md bg-amber-500/20 text-amber-400 shrink-0 mt-0.5 sm:mt-0">
            <ShieldAlert className="h-4 w-4" />
          </div>
          <div>
            <span className="font-semibold text-amber-300 mr-2">
              Demo Mode Active:
            </span>
            <span className="text-slate-300">
              Gemma API key is not configured. Exploring authentic pre-analyzed forms.
            </span>
            <span className="text-amber-400/90 font-medium ml-1.5 hidden lg:inline">
              (We do not fake AI responses — live document uploads require a configured Gemma 4 endpoint).
            </span>
          </div>
        </div>

        {/* Action pills & config link */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <div className="flex items-center gap-1.5 overflow-x-auto py-1">
            {samplePills.map((pill) => (
              <button
                key={pill.id}
                onClick={() => onSelectSample(pill.id)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition-all whitespace-nowrap ${
                  activeSampleId === pill.id
                    ? 'bg-amber-400 text-slate-950 shadow-sm font-semibold'
                    : 'bg-slate-900/80 text-amber-200/90 hover:bg-amber-500/20 border border-amber-500/30'
                }`}
                title={pill.desc}
              >
                {pill.label}
              </button>
            ))}
          </div>

          <button
            onClick={onOpenConfig}
            className="flex items-center gap-1 px-3 py-1 rounded-md bg-indigo-600/90 hover:bg-indigo-600 text-white font-medium text-xs transition-all shadow-sm shrink-0"
          >
            <KeyRound className="h-3 w-3" />
            <span>Connect Gemma 4</span>
          </button>
        </div>

      </div>
    </div>
  );
}
