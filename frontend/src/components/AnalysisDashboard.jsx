import React, { useState } from 'react';
import { 
  Building2, 
  Sparkles, 
  Code, 
  Printer, 
  RotateCcw, 
  ShieldCheck
} from 'lucide-react';

import DeadlinesSection from './DeadlinesSection';
import DocumentsSection from './DocumentsSection';
import FieldsSection from './FieldsSection';
import InstructionsSection from './InstructionsSection';
import ChecklistSection from './ChecklistSection';

export default function AnalysisDashboard({ 
  data, 
  languageMode, 
  onReset, 
  onViewRawSource,
  onToggleChecklistItem,
  onResetChecklist
}) {
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'deadlines', 'documents', 'fields', 'instructions', 'checklist'

  if (!data) return null;

  const mandatoryDocCount = data.required_documents?.filter(d => d.is_mandatory).length || 0;
  const verifiedCount = data.missing_info_checklist?.filter(c => c.is_checked).length || 0;
  const totalChecklist = data.missing_info_checklist?.length || 0;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 print:py-0 print:space-y-4">
      
      {/* Top Banner Card */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-xl relative overflow-hidden">
        
        {/* Subtle accent glow */}
        <div className="absolute top-0 right-0 w-80 h-80 bg-gradient-to-bl from-indigo-500/10 via-violet-500/5 to-transparent rounded-full blur-2xl pointer-events-none" />

        <div className="relative z-10 space-y-4">
          
          {/* Metadata badges row */}
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="flex flex-wrap items-center gap-2">
              <span className={`px-2.5 py-1 rounded-full font-semibold flex items-center gap-1.5 ${
                data.is_demo 
                  ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30' 
                  : 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
              }`}>
                <ShieldCheck className="h-3.5 w-3.5" />
                <span>{data.is_demo ? 'Verified Demo Sample' : 'Live Document Analysis'}</span>
              </span>

              <span className="px-2.5 py-1 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 font-semibold font-mono flex items-center gap-1">
                <Sparkles className="h-3 w-3" />
                <span>{data.model_used || 'Gemma'}</span>
              </span>

              <span className="text-slate-500 font-mono text-[11px] hidden sm:inline">
                {data.document_name} ({data.pages_processed || 1} pages)
              </span>
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-2 print:hidden">
              <button
                onClick={onViewRawSource}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-medium border border-slate-800 transition-all"
                title="Inspect extracted raw text"
                id="btn-view-source"
              >
                <Code className="h-3.5 w-3.5 text-indigo-400" />
                <span className="hidden sm:inline">Source Text</span>
              </button>

              <button
                onClick={handlePrint}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-medium border border-slate-800 transition-all"
                title="Print or Save PDF report"
                id="btn-print-report"
              >
                <Printer className="h-3.5 w-3.5 text-slate-400" />
                <span className="hidden sm:inline">Print</span>
              </button>

              <button
                onClick={onReset}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-all"
                id="btn-upload-new"
              >
                <RotateCcw className="h-3.5 w-3.5 text-slate-400" />
                <span>New Form</span>
              </button>
            </div>
          </div>

          {/* Form Title & Issuing Authority */}
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight font-['Outfit']">
              {data.form_title}
            </h1>
            <div className="flex items-center gap-1.5 text-xs sm:text-sm text-indigo-300 font-medium mt-1">
              <Building2 className="h-4 w-4 shrink-0 text-indigo-400" />
              <span>{data.issuing_organization}</span>
            </div>
            {data.form_purpose && (
              <p className="text-xs text-slate-400 mt-1 max-w-3xl">
                {data.form_purpose}
              </p>
            )}
          </div>

          {/* Bilingual Summaries Box */}
          <div className="pt-2">
            {languageMode === 'dual' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-indigo-300 mb-1.5">
                    <span className="w-2 h-2 rounded-full bg-indigo-400" />
                    English Form Summary
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    {data.summary_english}
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-cyan-300 mb-1.5">
                    <span className="w-2 h-2 rounded-full bg-cyan-400" />
                    हिंदी / Hinglish सारांश
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans">
                    {data.summary_hinglish}
                  </p>
                </div>
              </div>
            ) : languageMode === 'hinglish' ? (
              <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80">
                <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-cyan-300 mb-1.5">
                  <span className="w-2 h-2 rounded-full bg-cyan-400" />
                  हिंदी / Hinglish सारांश
                </div>
                <p className="text-sm text-slate-300 leading-relaxed">
                  {data.summary_hinglish}
                </p>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80">
                <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-indigo-300 mb-1.5">
                  <span className="w-2 h-2 rounded-full bg-indigo-400" />
                  Plain English Summary
                </div>
                <p className="text-sm text-slate-300 leading-relaxed">
                  {data.summary_english}
                </p>
              </div>
            )}
          </div>

          {/* Metrics summary row */}
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-3 border-t border-slate-800/80">
            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
              <span className="text-xl sm:text-2xl font-extrabold font-mono text-indigo-400">
                {data.deadlines?.length || 0}
              </span>
              <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">
                Stated Deadlines
              </p>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
              <span className="text-xl sm:text-2xl font-extrabold font-mono text-cyan-400">
                {mandatoryDocCount}/{data.required_documents?.length || 0}
              </span>
              <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">
                Mandatory Proofs
              </p>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
              <span className="text-xl sm:text-2xl font-extrabold font-mono text-amber-400">
                {data.required_fields?.length || 0}
              </span>
              <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">
                Required Fields
              </p>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
              <span className="text-xl sm:text-2xl font-extrabold font-mono text-violet-400">
                {data.instructions?.length || 0}
              </span>
              <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">
                Guidance Steps
              </p>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
              <span className="text-xl sm:text-2xl font-extrabold font-mono text-emerald-400">
                {verifiedCount}/{totalChecklist}
              </span>
              <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">
                Checklist Ready
              </p>
            </div>
          </div>

        </div>
      </div>

      {/* Navigation Tabs (optional filter) */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-2 print:hidden">
        <div className="flex items-center gap-1 sm:gap-2 overflow-x-auto py-1">
          <button
            onClick={() => setActiveTab('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'all'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            All Sections
          </button>
          <button
            onClick={() => setActiveTab('deadlines')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'deadlines'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            Deadlines ({data.deadlines?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('documents')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'documents'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            Documents ({data.required_documents?.length || 0})
          </button>
          {data.required_fields?.length > 0 && (
            <button
              onClick={() => setActiveTab('fields')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
                activeTab === 'fields'
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900'
              }`}
            >
              Fields ({data.required_fields?.length})
            </button>
          )}
          <button
            onClick={() => setActiveTab('instructions')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'instructions'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            Instructions ({data.instructions?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('checklist')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
              activeTab === 'checklist'
                ? 'bg-indigo-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            Checklist ({totalChecklist})
          </button>
        </div>
      </div>

      {/* Sections Container */}
      <div className="space-y-10">
        
        {/* Deadlines Section */}
        {(activeTab === 'all' || activeTab === 'deadlines') && (
          <DeadlinesSection deadlines={data.deadlines} />
        )}

        {/* Required Documents Section */}
        {(activeTab === 'all' || activeTab === 'documents') && (
          <DocumentsSection documents={data.required_documents} />
        )}

        {/* Required Form Fields Section */}
        {(activeTab === 'all' || activeTab === 'fields') && data.required_fields?.length > 0 && (
          <FieldsSection fields={data.required_fields} />
        )}

        {/* Instructions Section */}
        {(activeTab === 'all' || activeTab === 'instructions') && (
          <InstructionsSection 
            instructions={data.instructions} 
            languageMode={languageMode} 
          />
        )}

        {/* Missing-Information Checklist Section */}
        {(activeTab === 'all' || activeTab === 'checklist') && (
          <ChecklistSection 
            items={data.missing_info_checklist} 
            languageMode={languageMode}
            onToggleItem={onToggleChecklistItem}
            onResetChecklist={onResetChecklist}
          />
        )}

      </div>

    </div>
  );
}
