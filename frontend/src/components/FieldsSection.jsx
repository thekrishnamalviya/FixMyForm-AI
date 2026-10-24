import React from 'react';
import { FormInput } from 'lucide-react';

export default function FieldsSection({ fields }) {
  if (!fields || fields.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FormInput className="h-5 w-5 text-indigo-400" />
          <h3 className="text-lg font-bold text-white tracking-tight font-['Outfit']">
            Required Form Fields ({fields.length})
          </h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          Applicant Input Requirements
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {fields.map((field, idx) => (
          <div
            key={idx}
            className="glass-card rounded-xl p-4 border border-slate-800/90 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="text-sm font-bold text-slate-100">
                  {field.field_name}
                </h4>
                <span className={`px-2 py-0.5 rounded text-[10px] font-semibold tracking-wider uppercase shrink-0 ${
                  field.is_mandatory
                    ? 'bg-rose-500/15 text-rose-300 border border-rose-500/30'
                    : 'bg-slate-800 text-slate-400 border border-slate-700'
                }`}>
                  {field.is_mandatory ? 'Mandatory' : 'Optional'}
                </span>
              </div>

              <span className="inline-block px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-[10px] font-mono text-cyan-300 mb-2">
                Type: {field.field_type}
              </span>

              <p className="text-xs text-slate-300 leading-relaxed mb-3">
                {field.description}
              </p>

              {field.validation_rules && (
                <div className="p-2 rounded bg-slate-900/80 border border-slate-800/80 text-[11px] text-slate-400 mb-2">
                  <span className="font-semibold text-slate-300 mr-1">Rule:</span>
                  {field.validation_rules}
                </div>
              )}
            </div>

            {field.source_reference && (
              <p className="text-[10px] text-slate-500 font-mono text-right pt-2 border-t border-slate-800/50">
                Ref: {field.source_reference}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
