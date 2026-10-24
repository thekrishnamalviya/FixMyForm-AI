import React, { useState, useRef } from 'react';
import { 
  UploadCloud, 
  FileText, 
  Sparkles, 
  FileCheck, 
  AlertCircle, 
  Eye, 
  Loader2, 
  Clipboard 
} from 'lucide-react';

export default function DocumentUpload({ 
  onAnalyze, 
  onSelectSample, 
  isAnalyzing, 
  isDemoMode,
  onOpenConfig
}) {
  const [activeTab, setActiveTab] = useState('file'); // 'file' or 'text'
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [rawText, setRawText] = useState('');
  const [previewData, setPreviewData] = useState(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const fileInputRef = useRef(null);

  // Drag and drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      processSelectedFile(e.target.files[0]);
    }
  };

  const processSelectedFile = async (file) => {
    setUploadError(null);
    setSelectedFile(file);
    setIsPreviewLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/extract-preview', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to extract text preview');
      }

      const data = await res.json();
      setPreviewData(data);
    } catch (err) {
      console.error(err);
      setUploadError(err.message);
    } finally {
      setIsPreviewLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setUploadError(null);

    if (activeTab === 'file') {
      if (!selectedFile) {
        setUploadError('Please select or drop a PDF or Image form file first.');
        return;
      }
      onAnalyze({ file: selectedFile });
    } else {
      if (!rawText.trim()) {
        setUploadError('Please paste the form text or instructions.');
        return;
      }
      onAnalyze({ text: rawText });
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto my-6 px-4">
      
      {/* Container card */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-2xl relative overflow-hidden">
        
        {/* Glow ambient effect */}
        <div className="absolute -top-24 -right-24 w-72 h-72 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Section title & mode pill */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 relative z-10">
          <div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight font-['Outfit']">
              Analyze Application Form
            </h2>
            <p className="text-sm text-slate-400 mt-0.5">
              Powered exclusively by <span className="text-indigo-400 font-semibold">Gemma 4</span> for zero-hallucination document intelligence
            </p>
          </div>

          {/* Tab selector */}
          <div className="flex items-center bg-slate-900 border border-slate-800 rounded-xl p-1 self-start sm:self-auto">
            <button
              type="button"
              onClick={() => setActiveTab('file')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'file'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <FileText className="h-3.5 w-3.5" />
              <span>Upload PDF / Image</span>
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('text')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'text'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Clipboard className="h-3.5 w-3.5" />
              <span>Paste Text</span>
            </button>
          </div>
        </div>

        {/* Form input area */}
        <form onSubmit={handleSubmit} className="relative z-10">
          {activeTab === 'file' ? (
            <div>
              {/* Drag & Drop Area */}
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
                  dragActive 
                    ? 'border-indigo-400 bg-indigo-500/10 scale-[1.01]' 
                    : selectedFile
                    ? 'border-indigo-500/50 bg-slate-900/60 hover:border-indigo-400'
                    : 'border-slate-700/80 bg-slate-900/40 hover:border-slate-600 hover:bg-slate-900/60'
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg,.webp,.txt"
                  onChange={handleFileInput}
                  className="hidden"
                  id="file-upload-input"
                />

                {selectedFile ? (
                  <div className="flex flex-col items-center justify-center gap-2">
                    <div className="h-12 w-12 rounded-xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center">
                      <FileCheck className="h-6 w-6" />
                    </div>
                    <p className="text-sm font-semibold text-white">
                      {selectedFile.name}
                    </p>
                    <p className="text-xs text-slate-400">
                      {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB · Click or drag to change file
                    </p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center gap-3">
                    <div className="h-12 w-12 rounded-xl bg-slate-800 text-slate-400 flex items-center justify-center group-hover:text-indigo-400">
                      <UploadCloud className="h-6 w-6 text-indigo-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-200">
                        Drag and drop your form document here, or <span className="text-indigo-400 font-semibold">browse</span>
                      </p>
                      <p className="text-xs text-slate-500 mt-1">
                        Supports PDF, Scanned Images (PNG, JPG), or Plain Text (up to 25 MB)
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Real-time Document Text Preview Drawer */}
              {isPreviewLoading && (
                <div className="flex items-center gap-2 mt-3 px-3 py-2 rounded-lg bg-slate-900/60 text-xs text-slate-400">
                  <Loader2 className="h-3.5 w-3.5 animate-spin text-indigo-400" />
                  <span>Extracting text and checking for scanned layers...</span>
                </div>
              )}

              {previewData && !isPreviewLoading && (
                <div className="mt-3 p-3 rounded-lg bg-slate-900/70 border border-slate-800/80 text-xs text-slate-300">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-semibold text-slate-200 flex items-center gap-1.5">
                      <Eye className="h-3.5 w-3.5 text-indigo-400" />
                      Extracted Text Preview ({previewData.page_count} pages, {previewData.char_count} chars)
                    </span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${
                      previewData.is_scanned 
                        ? 'bg-amber-500/10 text-amber-300 border border-amber-500/20' 
                        : 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20'
                    }`}>
                      {previewData.is_scanned ? 'Scanned / Low Text' : 'Searchable Text PDF'}
                    </span>
                  </div>
                  <p className="text-slate-400 font-mono text-[11px] line-clamp-2">
                    {previewData.preview_snippet || '[No text snippet extracted]'}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div>
              <textarea
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                placeholder="Paste the official form instructions, guidelines, eligibility criteria, or notification text here..."
                rows={6}
                className="w-full bg-slate-900/70 border border-slate-800 rounded-xl p-4 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 font-mono"
                id="raw-text-input"
              />
            </div>
          )}

          {/* Error notice */}
          {uploadError && (
            <div className="flex items-start gap-2 mt-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
              <AlertCircle className="h-4 w-4 shrink-0 mt-0.5 text-rose-400" />
              <div>
                <p className="font-semibold">Document Analysis Notice</p>
                <p className="text-rose-300/90 mt-0.5">{uploadError}</p>
                {isDemoMode && (
                  <button
                    type="button"
                    onClick={onOpenConfig}
                    className="mt-1 text-indigo-400 underline font-medium hover:text-indigo-300"
                  >
                    View Gemma 4 Setup Guide to configure your API key →
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Action Row */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mt-6">
            
            {/* Quick demo pills */}
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <span className="text-xs text-slate-500 hidden sm:inline">Or try sample:</span>
              <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto">
                <button
                  type="button"
                  onClick={() => onSelectSample('form_122b')}
                  className="px-2.5 py-1 rounded-lg bg-indigo-950/70 hover:bg-indigo-900 text-indigo-300 text-xs font-medium border border-indigo-500/30 whitespace-nowrap"
                >
                  ⚖️ Form 122B
                </button>
                <button
                  type="button"
                  onClick={() => onSelectSample('passport')}
                  className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 whitespace-nowrap"
                >
                  🛂 Passport
                </button>
                <button
                  type="button"
                  onClick={() => onSelectSample('scholarship')}
                  className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 whitespace-nowrap"
                >
                  🎓 Scholarship
                </button>
                <button
                  type="button"
                  onClick={() => onSelectSample('tax_12bb')}
                  className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 whitespace-nowrap"
                >
                  💼 Form 12BB
                </button>
              </div>
            </div>

            {/* Primary Submit Button */}
            <button
              type="submit"
              disabled={isAnalyzing}
              className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold text-sm shadow-lg shadow-indigo-500/25 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform active:scale-95"
              id="btn-analyze-document"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Processing with Gemma 4...</span>
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" />
                  <span>Analyze with Gemma 4</span>
                </>
              )}
            </button>

          </div>
        </form>

      </div>
    </div>
  );
}
