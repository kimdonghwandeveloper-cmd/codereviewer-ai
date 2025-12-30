import React from 'react';
import Editor from '@monaco-editor/react';

export function CodeEditor({ code, onChange, filename, onFileUpload }) {
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            onFileUpload(file);
        }
    };

    return (
        <div className="flex-1 min-h-[500px] border border-[var(--border-color)] rounded-xl overflow-hidden glass-panel shadow-2xl relative flex flex-col">
            {/* Header */}
            <div className="h-10 bg-[var(--bg-secondary)] flex items-center justify-between px-4 text-xs font-mono text-[var(--text-secondary)] border-b border-[var(--border-color)]">
                <span className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
                    {filename || 'main.py'}
                </span>

                <label className="cursor-pointer hover:text-[var(--text-primary)] transition-colors flex items-center gap-1.5 px-2 py-1 rounded hover:bg-[var(--bg-tertiary)]">
                    <input type="file" className="hidden" accept=".py,.txt,.js,.jsx,.ts,.tsx" onChange={handleFileChange} />
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>
                    <span>Open File</span>
                </label>
            </div>

            {/* Editor */}
            <div className="flex-1">
                <Editor
                    height="100%"
                    defaultLanguage="python"
                    value={code}
                    onChange={onChange}
                    theme="vs-dark"
                    options={{
                        minimap: { enabled: false },
                        fontSize: 14,
                        padding: { top: 20 },
                        scrollBeyondLastLine: false,
                        fontFamily: "Fira Code, monospace",
                        smoothScrolling: true,
                        lineHeight: 1.6,
                        renderLineHighlight: 'none',
                        contextmenu: false,
                    }}
                />
            </div>
        </div>
    );
}
