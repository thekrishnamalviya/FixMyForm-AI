import React, { useState } from 'react';
import { CheckSquare, Square, CheckCircle2, Filter, RotateCcw } from 'lucide-react';

export default function ChecklistSection({ 
  items, 
  languageMode, 
  onToggleItem,
  onResetChecklist 
}) {
  const [selectedCategory, setSelectedCategory] = useState('all');

  if (!items || items.length === 0) {
    return null;
  }

  const completedCount = items.filter((i) => i.is_checked).length;
  const progressPercent = Math.round((completedCount / items.length) * 100);

  const categories = ['all', ...new Set(items.map((i) => i.category || 'general'))];

  const filteredItems = selectedCategory === 'all'
    ? items
    : items.filter((i) => (i.category || 'general') === selectedCategory);

  return (
    <div className="space-y-4">
      
      {/* Header & Progress Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <CheckSquare className="h-5 w-5 text-indigo-400" />
            <h3 className="text-lg font-bold text-white tracking-tight font-['Outfit']">
              Pre-Submission Verification Checklist ({items.length})
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Verify every mandatory field and document before submitting to avoid delays
          </p>
        </div>

        {/* Action reset / mark all */}
        <div className="flex items-center gap-3 self-start sm:self-auto">
          <span className="text-xs font-semibold font-mono text-indigo-300">
            {completedCount}/{items.length} Ready ({progressPercent}%)
          </span>
          {completedCount > 0 && onResetChecklist && (
            <button
              onClick={onResetChecklist}
              className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-slate-200 px-2 py-0.5 rounded bg-slate-900 border border-slate-800 hover:bg-slate-800 transition-all"
              title="Reset all checklist items"
            >
              <RotateCcw className="h-3 w-3" />
              <span>Reset</span>
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
        <div
          className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full rounded-full transition-all duration-300"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* Category Pills */}
      {categories.length > 2 && (
        <div className="flex items-center gap-1.5 overflow-x-auto py-1">
          <Filter className="h-3.5 w-3.5 text-slate-500 shrink-0" />
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-2.5 py-1 rounded-md text-[11px] font-semibold tracking-wider uppercase transition-all whitespace-nowrap ${
                selectedCategory === cat
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      {/* Checklist Grid */}
      <div className="space-y-3">
        {filteredItems.map((item) => (
          <div
            key={item.id}
            onClick={() => onToggleItem(item.id)}
            className={`cursor-pointer rounded-xl p-4 border transition-all ${
              item.is_checked
                ? 'bg-emerald-950/20 border-emerald-500/40 hover:border-emerald-500/60'
                : 'glass-card border-slate-800/90 hover:border-slate-700'
            }`}
          >
            <div className="flex items-start gap-3">
              {/* Checkbox Icon */}
              <div className="mt-0.5 text-indigo-400 shrink-0">
                {item.is_checked ? (
                  <CheckCircle2 className="h-5 w-5 text-emerald-400" />
                ) : (
                  <Square className="h-5 w-5 text-slate-500 hover:text-slate-300" />
                )}
              </div>

              {/* Item Info */}
              <div className="flex-1">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1">
                  <h4 className={`text-sm font-bold ${item.is_checked ? 'line-through text-slate-400' : 'text-slate-100'}`}>
                    {item.field_name}
                  </h4>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                      {item.category}
                    </span>
                    {item.source_reference && (
                      <span className="text-[10px] text-slate-400 font-mono">
                        Ref: {item.source_reference}
                      </span>
                    )}
                  </div>
                </div>

                {/* Why needed */}
                <p className="text-xs text-slate-400 mb-2">
                  <span className="text-slate-300 font-medium">Why it matters:</span> {item.why_needed}
                </p>

                {/* Bilingual Tips */}
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800/80 text-xs space-y-1">
                  {(languageMode === 'dual' || languageMode === 'en') && (
                    <p className="text-slate-300">
                      <span className="text-indigo-400 font-semibold mr-1.5">Action Tip:</span>
                      {item.english_tip}
                    </p>
                  )}
                  {(languageMode === 'dual' || languageMode === 'hinglish') && (
                    <p className="text-slate-300 font-sans">
                      <span className="text-cyan-400 font-semibold mr-1.5">हिंदी Tip:</span>
                      {item.hinglish_tip}
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
