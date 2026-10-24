import React from 'react';
import { Files, Quote, Tag } from 'lucide-react';

export default function DocumentsSection({ documents }) {
  if (!documents || documents.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Files className="h-5 w-5 text-indigo-400" />
          <h3 className="text-lg font-bold text-white tracking-tight font-['Outfit']">
            Required Documents & Evidence ({documents.length})
          </h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          Strict verification criteria
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {documents.map((doc, idx) => (
          <div
            key={idx}
            className="glass-card rounded-xl p-5 border border-slate-800/90 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div>
              {/* Mandatory Badge & Title */}
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="text-base font-bold text-slate-100 leading-snug">
                  {doc.name}
                </h4>
                <span className={`px-2 py-0.5 rounded text-[10px] font-semibold tracking-wider uppercase shrink-0 ${
                  doc.is_mandatory 
                    ? 'bg-rose-500/15 text-rose-300 border border-rose-500/30' 
                    : 'bg-slate-800 text-slate-400 border border-slate-700'
                }`}>
                  {doc.is_mandatory ? 'Mandatory' : 'Optional / Supporting'}
                </span>
              </div>

              {/* Acceptable document options */}
              {doc.acceptable_types && doc.acceptable_types.length > 0 && (
                <div className="mb-3">
                  <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                    <Tag className="h-3 w-3 text-indigo-400" />
                    Acceptable Proofs:
                  </p>
                  <ul className="space-y-1">
                    {doc.acceptable_types.map((type, tIdx) => (
                      <li key={tIdx} className="text-xs text-slate-300 flex items-start gap-1.5">
                        <span className="h-1.5 w-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                        <span>{type}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Format & specs */}
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs mb-3">
                <span className="text-slate-400 font-semibold block mb-0.5 text-[11px]">
                  Specifications & Preparation:
                </span>
                <span className="text-slate-200">
                  {doc.format_and_specs}
                </span>
              </div>
            </div>

            {/* Source citation */}
            <div className="pt-2 border-t border-slate-800/60 text-xs">
              <div className="flex items-start gap-1.5 text-slate-400 italic">
                <Quote className="h-3 w-3 shrink-0 text-slate-500 mt-0.5" />
                <span className="line-clamp-2">"{doc.source_quote}"</span>
              </div>
              {doc.source_reference && (
                <p className="text-[10px] text-slate-500 font-mono mt-1 text-right">
                  Ref: {doc.source_reference}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
