import React from 'react';
import { 
  FileText, 
  Settings as SettingsIcon, 
  ShieldAlert, 
  CheckCircle2 
} from 'lucide-react';

export default function Navbar({ 
  systemStatus, 
  languageMode, 
  setLanguageMode, 
  onOpenConfig
}) {
  const isDemo = systemStatus?.demo_mode_active ?? true;

  return (
    <header className="sticky top-0 z-40 w-full backdrop-blur-xl bg-slate-950/80 border-b border-slate-800/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-400 p-[1px] shadow-lg shadow-indigo-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[11px] flex items-center justify-center">
              <FileText className="h-5 w-5 text-indigo-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg sm:text-xl tracking-tight text-white font-['Outfit']">
                FixMyForm <span className="bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">AI</span>
              </span>
              <span className="text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                Gemma 4
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Intelligent Document & Form Compliance Engine
            </p>
          </div>
        </div>

        {/* Center / Right controls */}
        <div className="flex items-center gap-2 sm:gap-4">
          
          {/* Status Badge */}
          {isDemo ? (
            <button
              onClick={onOpenConfig}
              className="group flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-medium hover:bg-amber-500/20 transition-all shadow-sm"
              title="Gemma API is not configured. Running in Demo Mode with verified sample forms."
            >
              <ShieldAlert className="h-3.5 w-3.5 text-amber-400 animate-pulse" />
              <span>Demo Mode</span>
              <span className="hidden md:inline text-amber-400/80 font-normal">· Pre-analyzed Samples</span>
            </button>
          ) : (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-medium">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
              <span>Gemma 4 Live</span>
            </div>
          )}

          {/* Language Toggle */}
          <div className="flex items-center bg-slate-900/90 border border-slate-800 rounded-lg p-0.5 text-xs">
            <button
              onClick={() => setLanguageMode('dual')}
              className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                languageMode === 'dual'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Side-by-side English & Hinglish"
            >
              Dual
            </button>
            <button
              onClick={() => setLanguageMode('en')}
              className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                languageMode === 'en'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Plain English only"
            >
              English
            </button>
            <button
              onClick={() => setLanguageMode('hinglish')}
              className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                languageMode === 'hinglish'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Hinglish / Hindi conversational explanations"
            >
              हिंदी (Hinglish)
            </button>
          </div>

          {/* Settings / Config Button */}
          <button
            onClick={onOpenConfig}
            className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 hover:bg-slate-800 transition-all"
            title="Gemma 4 Configuration & Setup"
            id="btn-settings"
          >
            <SettingsIcon className="h-4 w-4" />
          </button>

        </div>
      </div>
    </header>
  );
}
