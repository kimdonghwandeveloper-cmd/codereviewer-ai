import React, { useState } from 'react';
import axios from 'axios';
import { Layout } from './components/Layout';
import { CodeEditor } from './components/CodeEditor';
import { AnalysisResult } from './components/AnalysisResult';
import { Play, Loader2, Sparkles } from 'lucide-react';

// Default code snippet for demo
const DEFAULT_CODE = `def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# This function is inefficient for large n
print(calculate_fibonacci(10))
`;

function App() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filename, setFilename] = useState('main.py');

  const handleFileUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setCode(e.target.result);
      setFilename(file.name);
    };
    reader.readAsText(file);
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('/api/analyze', {
        code: code,
        language: 'python', // You could detect this from filename extension in the future
        use_ai: true
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'mysecretkey'
        }
      });

      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to analyze code.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setCode(DEFAULT_CODE);
    setResult(null);
    setError(null);
    setFilename('main.py');
    // Optional: Reset file input if needed
  };

  return (
    <Layout onNewAnalysis={handleReset}>
      <div className="h-full flex flex-col relative overflow-hidden bg-[var(--bg-primary)]">

        {/* Top Gradient */}
        <div className="absolute top-0 left-0 right-0 h-64 bg-gradient-to-b from-[#1a1a1a] to-transparent pointer-events-none opacity-50 z-0"></div>

        {/* Content Container */}
        <div className="flex-1 flex flex-col z-10 max-w-7xl mx-auto w-full p-6 relative">

          {/* Welcome Header */}
          {!result && (
            <div className="mb-12 mt-12 text-center animate-fade-in transition-all duration-500">
              <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-red-400 mb-4 tracking-tight">
                Donghwan님, 안녕하세요
              </h1>
              <p className="text-[var(--text-secondary)] text-xl font-light">
                무엇을 도와드릴까요? 코드를 분석해 드립니다.
              </p>
            </div>
          )}

          {/* Editor Section - Always Visible, Full Width initially */}
          <div className={`flex flex-col gap-4 transition-all duration-500 w-full h-full max-w-4xl mx-auto z-10`}>
            {/* Action Bar */}
            <div className="flex justify-between items-center px-1">
              <h2 className="text-sm font-medium text-[var(--text-secondary)] uppercase tracking-wider flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[var(--primary-color)]"></span>
                Input Code
              </h2>
              <button
                onClick={handleAnalyze}
                disabled={isLoading}
                className="px-6 py-2 rounded-full bg-[var(--text-primary)] text-[var(--bg-primary)] font-semibold hover:opacity-90 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-white/5 active:scale-95"
              >
                {isLoading ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
                <span>{isLoading ? 'Analyzing...' : 'Run Analysis'}</span>
              </button>
            </div>

            <CodeEditor
              code={code}
              onChange={(val) => setCode(val)}
              filename={filename}
              onFileUpload={handleFileUpload}
            />
          </div>

          {/* BACKDROP for Dismissing Result */}
          {result && (
            <div
              className="fixed inset-0 z-40 bg-black/20 backdrop-blur-[1px] cursor-pointer"
              onClick={() => setResult(null)}
              title="Click to close report"
            ></div>
          )}

          {/* Results Overlay Drawer */}
          {result && (
            <div className="fixed top-0 right-0 bottom-0 w-[500px] bg-[var(--bg-secondary)] border-l border-[var(--border-color)] shadow-2xl z-50 flex flex-col animate-slide-in-right">
              <div className="flex-1 overflow-y-auto p-6">
                <div className="mb-6 flex items-center justify-between">
                  <div className="text-sm font-medium text-[var(--text-secondary)] uppercase tracking-wider flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-[var(--secondary-color)]"></span>
                    Analysis Report
                  </div>
                  <button onClick={() => setResult(null)} className="text-[var(--text-secondary)] hover:text-white">
                    ✕
                  </button>
                </div>
                <AnalysisResult result={result} />
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="w-full max-w-4xl mt-4 p-4 rounded-lg bg-red-900/20 border border-red-500/30 text-red-200 text-center animate-fade-in mx-auto z-20">
              {error}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

export default App;
