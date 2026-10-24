import React from 'react';
import { Calendar, Clock, AlertTriangle, Quote } from 'lucide-react';

export default function DeadlinesSection({ deadlines }) {
  if (!deadlines || deadlines.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-slate-800 text-center">
        <Clock className="h-8 w-8 text-slate-500 mx-auto mb-2" />
        <h4 className="text-base font-semibold text-slate-300">No Explicit Deadlines Mentioned</h4>
        <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          Gemma 4 strictly avoids hallucinating submission dates. If deadlines are announced in a supplementary gazette or separate notification, they will be captured when uploaded.
        </p>
      </div>
    );
  }

  const getUrgencyBadge = (urgency) => {
    switch (urgency?.toLowerCase()) {
      case 'high':
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-500/15 text-rose-300 border border-rose-500/30 flex items-center gap-1">
            <AlertTriangle className="h-3 w-3 text-rose-400" />
            High Urgency
          </span>
        );
      case 'medium':
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/15 text-amber-300 border border-amber-500/30">
            Medium Priority
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
            Standard Timeline
          </span>
        );
    }
  };

  const getCategoryColor = (category) => {
    switch (category?.toLowerCase()) {
      case 'submission':
        return 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20';
      case 'fee_payment':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'correction':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      default:
        return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Calendar className="h-5 w-5 text-indigo-400" />
          <h3 className="text-lg font-bold text-white tracking-tight font-['Outfit']">
            Explicit Deadlines & Cutoffs ({deadlines.length})
          </h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          Extracted directly from source
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {deadlines.map((item, idx) => (
          <div
            key={idx}
            className="glass-card rounded-xl p-4 border border-slate-800/90 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div>
              {/* Top row: category & urgency */}
              <div className="flex items-center justify-between gap-2 mb-2.5">
                <span className={`text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full border ${getCategoryColor(item.category)}`}>
                  {item.category?.replace('_', ' ')}
                </span>
                {getUrgencyBadge(item.urgency)}
              </div>

              {/* Title & Date */}
              <h4 className="text-sm font-semibold text-slate-100 mb-1 leading-snug">
                {item.title}
              </h4>
              <p className="text-sm font-bold text-indigo-300 font-mono bg-slate-900/80 px-2.5 py-1.5 rounded-lg border border-slate-800 mb-3">
                {item.date_or_time}
              </p>
            </div>

            {/* Source quote */}
            <div className="pt-2 border-t border-slate-800/60 text-xs">
              <div className="flex items-start gap-1.5 text-slate-400 italic">
                <Quote className="h-3 w-3 shrink-0 text-slate-500 mt-0.5" />
                <span className="line-clamp-3">"{item.source_quote}"</span>
              </div>
              {item.source_reference && (
                <p className="text-[10px] text-slate-500 font-mono mt-1 text-right">
                  Ref: {item.source_reference}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
