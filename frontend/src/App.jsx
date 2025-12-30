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

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      // Using proxy /api -> http://127.0.0.1:8000/api
      const response = await axios.post('/api/analyze', {
        code: code,
        language: 'python',
        use_ai: true
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'mysecretkey' // Hardcoded for demo convenience
        }
      });

      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to analyze code. Please check backend connection.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <div className="flex h-full">
        {/* Left: Editor Area */}
        <div className="flex-1 flex flex-col p-4 gap-4 min-w-[500px]">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-400"></span>
              Editor
            </h2>
            <button
              onClick={handleAnalyze}
              disabled={isLoading}
              className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? <Loader2 className="animate-spin" size={18} /> : <Play size={18} />}
              {isLoading ? 'Analyzing...' : 'Run Analysis'}
            </button>
          </div>

          <CodeEditor code={code} onChange={(val) => setCode(val)} />
        </div>

        {/* Right: Analysis Result Area */}
        <div className="flex-1 border-l border-[var(--border-color)] bg-[var(--bg-secondary)] p-6 overflow-y-auto">
          {!result && !isLoading && !error && (
            <div className="h-full flex flex-col items-center justify-center text-[var(--text-secondary)] opacity-50">
              <Sparkles size={48} className="mb-4" />
              <p className="text-lg">Ready to analyze your code</p>
              <p className="text-sm">Click "Run Analysis" to get AI insights.</p>
            </div>
          )}

          {error && (
            <div className="p-4 rounded bg-red-500/10 border border-red-500/50 text-red-500">
              <strong>Error:</strong> {error}
            </div>
          )}

          {isLoading && (
            <div className="h-full flex flex-col items-center justify-center space-y-4">
              <Loader2 size={40} className="animate-spin text-[var(--primary-color)]" />
              <p className="text-[var(--text-accent)] animate-pulse">Consulting AI experts...</p>
            </div>
          )}

          {result && <AnalysisResult result={result} />}
        </div>
      </div>
    </Layout>
  );
}

export default App;
