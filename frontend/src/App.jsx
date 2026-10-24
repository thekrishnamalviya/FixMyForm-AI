import React, { useState, useEffect, useCallback } from 'react';
import { AlertCircle, X } from 'lucide-react';
import Navbar from './components/Navbar';
import DemoModeBanner from './components/DemoModeBanner';
import HeroBanner from './components/HeroBanner';
import DocumentUpload from './components/DocumentUpload';
import AnalysisDashboard from './components/AnalysisDashboard';
import RawSourceModal from './components/RawSourceModal';
import ConfigModal from './components/ConfigModal';

export default function App() {
  const [systemStatus, setSystemStatus] = useState(null);
  const [languageMode, setLanguageMode] = useState('dual'); // 'dual', 'en', 'hinglish'
  const [analysisData, setAnalysisData] = useState(null);
  const [activeSampleId, setActiveSampleId] = useState('passport');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isConfigOpen, setIsConfigOpen] = useState(false);
  const [isRawSourceOpen, setIsRawSourceOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const fetchSystemStatus = useCallback(async () => {
    try {
      const res = await fetch('/api/status');
      if (res.ok) {
        const data = await res.json();
        setSystemStatus(data);
      }
    } catch (err) {
      console.error('Failed to fetch system status:', err);
    }
  }, []);

  const loadSampleForm = useCallback(async (sampleId) => {
    setIsAnalyzing(true);
    setErrorMessage(null);
    try {
      const res = await fetch(`/api/samples/${sampleId}`);
      if (!res.ok) {
        throw new Error(`Failed to load sample form: ${sampleId}`);
      }
      const data = await res.json();
      setAnalysisData(data);
      setActiveSampleId(sampleId);
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message);
    } finally {
      setIsAnalyzing(false);
    }
  }, []);

  // Fetch system status and initial sample on mount
  useEffect(() => {
    fetchSystemStatus();
    loadSampleForm('passport');
  }, [fetchSystemStatus, loadSampleForm]);

  // Analyze custom document or text
  const handleAnalyze = async ({ file, text }) => {
    setIsAnalyzing(true);
    setErrorMessage(null);

    const formData = new FormData();
    if (file) {
      formData.append('file', file);
    } else if (text) {
      formData.append('raw_text', text);
    }

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        if (data.error_code === 'GEMMA_NOT_CONFIGURED') {
          // Strictly handle missing Gemma API: do not fake AI
          setErrorMessage(
            'Gemma 4 API key is not configured in backend environment variables. ' +
            'FixMyForm AI strictly refuses to fake AI responses. ' +
            'Please configure GEMMA_API_KEY in backend/.env, or click any sample form below to view verified analyses.'
          );
          setIsConfigOpen(true);
          return;
        }
        throw new Error(data.detail || data.message || 'Analysis failed');
      }

      setAnalysisData(data);
      setActiveSampleId(null);
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Toggle checklist item status
  const handleToggleChecklistItem = (itemId) => {
    if (!analysisData || !analysisData.missing_info_checklist) return;

    const updatedChecklist = analysisData.missing_info_checklist.map((item) => {
      if (item.id === itemId) {
        return { ...item, is_checked: !item.is_checked };
      }
      return item;
    });

    setAnalysisData({
      ...analysisData,
      missing_info_checklist: updatedChecklist,
    });
  };

  // Reset checklist to original states
  const handleResetChecklist = () => {
    if (!analysisData || !analysisData.missing_info_checklist) return;
    const resetList = analysisData.missing_info_checklist.map(item => ({
      ...item,
      is_checked: false
    }));
    setAnalysisData({
      ...analysisData,
      missing_info_checklist: resetList
    });
  };

  const handleResetView = () => {
    setAnalysisData(null);
    setActiveSampleId(null);
    setErrorMessage(null);
  };

  const isDemo = systemStatus?.demo_mode_active ?? true;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      
      {/* Top Navbar */}
      <Navbar
        systemStatus={systemStatus}
        languageMode={languageMode}
        setLanguageMode={setLanguageMode}
        onOpenConfig={() => setIsConfigOpen(true)}
        onSelectSample={loadSampleForm}
      />

      {/* Demo Mode Notice Banner */}
      {isDemo && (
        <DemoModeBanner
          onOpenConfig={() => setIsConfigOpen(true)}
          onSelectSample={loadSampleForm}
          activeSampleId={activeSampleId}
        />
      )}

      {/* Error Alert Banner */}
      {errorMessage && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
          <div className="flex items-start justify-between gap-3 p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-200 text-xs sm:text-sm">
            <div className="flex items-start gap-2.5">
              <AlertCircle className="h-5 w-5 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-rose-200">Document Processing Notice</p>
                <p className="text-rose-300/90 mt-0.5">{errorMessage}</p>
              </div>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="p-1 rounded-lg hover:bg-rose-900/40 text-rose-400 hover:text-rose-200 transition-all shrink-0"
              aria-label="Dismiss error"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <main className="flex-1 pb-16">
        
        {/* If no analysis data is loaded, show Hero & Upload */}
        {!analysisData ? (
          <div>
            <HeroBanner onSelectSample={loadSampleForm} />
            <DocumentUpload
              onAnalyze={handleAnalyze}
              onSelectSample={loadSampleForm}
              isAnalyzing={isAnalyzing}
              isDemoMode={isDemo}
              onOpenConfig={() => setIsConfigOpen(true)}
            />
          </div>
        ) : (
          <div>
            {/* Top quick switcher & upload toggler */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Current Form:</span>
                <span className="font-bold text-slate-200">
                  {analysisData.form_title}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleResetView}
                  className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium shadow-sm transition-all"
                  id="btn-upload-another"
                >
                  + Upload Another Form
                </button>
              </div>
            </div>

            {/* Analysis Dashboard */}
            <AnalysisDashboard
              data={analysisData}
              languageMode={languageMode}
              onReset={handleResetView}
              onViewRawSource={() => setIsRawSourceOpen(true)}
              onToggleChecklistItem={handleToggleChecklistItem}
              onResetChecklist={handleResetChecklist}
            />
          </div>
        )}

      </main>

      {/* Footer crediting Gemma 4 */}
      <footer className="w-full border-t border-slate-900 bg-slate-950/90 py-6 px-4 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>
            FixMyForm AI — Built exclusively with <strong className="text-slate-300">Google Gemma 4</strong> open document understanding model.
          </p>
          <p className="flex items-center gap-3">
            <span>React + Tailwind CSS + FastAPI</span>
            <span>·</span>
            <button
              onClick={() => setIsConfigOpen(true)}
              className="text-indigo-400 hover:underline"
            >
              Gemma 4 Setup &amp; Specs
            </button>
          </p>
        </div>
      </footer>

      {/* Source Text Modal */}
      <RawSourceModal
        isOpen={isRawSourceOpen}
        onClose={() => setIsRawSourceOpen(false)}
        rawText={analysisData?.raw_text_snippet}
        documentName={analysisData?.document_name}
      />

      {/* Configuration & Setup Modal */}
      <ConfigModal
        isOpen={isConfigOpen}
        onClose={() => setIsConfigOpen(false)}
        systemStatus={systemStatus}
        onStatusRefresh={fetchSystemStatus}
      />

    </div>
  );
}
