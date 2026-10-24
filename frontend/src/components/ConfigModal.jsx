import React, { useState } from 'react';
import { 
  X, 
  ShieldCheck, 
  Terminal, 
  CheckCircle2, 
  AlertTriangle, 
  Sparkles, 
  Play,
  Loader2,
  Clock
} from 'lucide-react';

export default function ConfigModal({ isOpen, onClose, systemStatus, onStatusRefresh }) {
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  if (!isOpen) return null;

  const isConfigured = systemStatus?.gemma_configured;

  const handleTestConnection = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      const res = await fetch('/api/test-connection', { method: 'POST' });
      const data = await res.json();
      setTestResult(data);
      if (onStatusRefresh) {
        onStatusRefresh();
      }
    } catch (err) {
      setTestResult({
        success: false,
        message: 'Failed to contact backend test endpoint.',
        error_detail: String(err)
      });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-2xl max-h-[90vh] bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/90">
          <div className="flex items-center gap-2.5">
            <div className="h-8 w-8 rounded-lg bg-indigo-600/20 text-indigo-400 flex items-center justify-center">
              <Sparkles className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-['Outfit']">
                Model Connection &amp; Provider Settings
              </h3>
              <p className="text-xs text-slate-400">
                FixMyForm AI — Solely powered by Google Gemma
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-5 text-xs sm:text-sm">
          
          {/* Status Chip & Test Button */}
          <div className={`p-4 rounded-xl border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 ${
            isConfigured
              ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-300'
              : 'bg-amber-950/20 border-amber-500/30 text-amber-300'
          }`}>
            <div className="flex items-start gap-2.5">
              {isConfigured ? (
                <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0 mt-0.5" />
              ) : (
                <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
              )}
              <div>
                <p className="font-bold text-sm">
                  {isConfigured ? 'API Key Detected in Environment' : 'Demo Mode Active (API Key Empty on Disk)'}
                </p>
                <p className="text-xs mt-0.5 text-slate-300">
                  {isConfigured
                    ? `Current Model: ${systemStatus?.gemma_model} (${systemStatus?.endpoint_host})`
                    : 'Remember to press Ctrl+S to save backend/.env. Click below to verify live inference.'}
                </p>
              </div>
            </div>

            <button
              onClick={handleTestConnection}
              disabled={testing}
              className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs shadow-sm transition-all flex items-center gap-1.5 shrink-0 disabled:opacity-50"
              id="btn-test-connection"
            >
              {testing ? (
                <>
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  <span>Testing Connection...</span>
                </>
              ) : (
                <>
                  <Play className="h-3.5 w-3.5" />
                  <span>Test Model Connection</span>
                </>
              )}
            </button>
          </div>

          {/* Test Result Display */}
          {testResult && (
            <div className={`p-4 rounded-xl border text-xs space-y-1.5 ${
              testResult.success
                ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-200'
                : 'bg-rose-950/40 border-rose-500/50 text-rose-200'
            }`}>
              <div className="flex items-center justify-between font-bold text-sm">
                <span className="flex items-center gap-1.5">
                  {testResult.success ? (
                    <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  ) : (
                    <AlertTriangle className="h-4 w-4 text-rose-400" />
                  )}
                  {testResult.success ? 'Model Connection Verified Live!' : 'Connection Check Failed'}
                </span>
                {testResult.latency_ms > 0 && (
                  <span className="font-mono text-[11px] text-slate-400 flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    {testResult.latency_ms} ms
                  </span>
                )}
              </div>
              <p className="text-xs leading-relaxed">{testResult.message}</p>
              {testResult.error_detail && (
                <div className="p-2 rounded bg-slate-950/80 font-mono text-[11px] text-slate-300 overflow-x-auto">
                  {testResult.error_detail}
                </div>
              )}
              {testResult.available_gemma_models && testResult.available_gemma_models.length > 0 && (
                <div className="pt-1">
                  <p className="text-[11px] font-semibold text-slate-300">Gemma Models Available on Provider:</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {testResult.available_gemma_models.map((m, i) => (
                      <span key={i} className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-[10px] font-mono text-indigo-300">
                        {m}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Strict Architectural Rules */}
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
            <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-indigo-400" />
              Strict Architectural Constraints
            </h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              <li className="flex items-start gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                <span><strong className="text-slate-200">Gemma Only:</strong> Gemma is the exclusive model used for document understanding. Do not silently use another AI model.</span>
              </li>
              <li className="flex items-start gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                <span><strong className="text-slate-200">No DigitalOcean:</strong> DigitalOcean is strictly prohibited as an AI provider.</span>
              </li>
              <li className="flex items-start gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                <span><strong className="text-slate-200">Real Verification:</strong> We do not claim the model works until a real API request succeeds.</span>
              </li>
            </ul>
          </div>

          {/* Setup Guide */}
          <div>
            <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Terminal className="h-4 w-4 text-indigo-400" />
              How to Configure Backboard / Gemma (backend/.env)
            </h4>
            <p className="text-xs text-slate-400 mb-2">
              Add your credentials to <code className="bg-slate-800 text-indigo-300 px-1 py-0.5 rounded font-mono">backend/.env</code> and save (<kbd className="px-1 py-0.5 bg-slate-800 rounded">Ctrl+S</kbd>):
            </p>

            <div className="rounded-xl bg-slate-950 p-3.5 border border-slate-800 font-mono text-xs text-indigo-300 overflow-x-auto leading-relaxed">
              # Backboard API Configuration<br />
              BACKBOARD_API_KEY=your_backboard_api_key<br />
              BACKBOARD_API_ENDPOINT=https://app.backboard.io/api<br />
              BACKBOARD_PROVIDER=google<br />
              GEMMA_MODEL=google/gemma-3-12b-it<br />
              <br />
              # Or Standard OpenAI-Compatible Endpoint (Groq / OpenRouter)<br />
              # GEMMA_API_KEY=your_key_here<br />
              # GEMMA_API_ENDPOINT=https://api.groq.com/openai/v1/chat/completions<br />
              # GEMMA_MODEL=google/gemma-4
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-800 bg-slate-900/90 text-right">
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm"
          >
            Done
          </button>
        </div>

      </div>
    </div>
  );
}
