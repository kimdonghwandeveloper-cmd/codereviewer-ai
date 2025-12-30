import React from 'react';
import Editor from '@monaco-editor/react';

export function CodeEditor({ code, onChange }) {
    return (
        <div className="flex-1 min-h-[500px] border border-[var(--border-color)] rounded-lg overflow-hidden glass-panel shadow-2xl relative">
            <div className="absolute top-0 left-0 right-0 h-8 bg-[var(--bg-tertiary)] flex items-center px-4 text-xs font-mono text-[var(--text-secondary)] z-10 border-b border-[var(--border-color)]">
                main.py
            </div>
            <Editor
                height="100%"
                defaultLanguage="python"
                value={code}
                onChange={onChange}
                theme="vs-dark"
                options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    padding: { top: 40 },
                    scrollBeyondLastLine: false,
                    fontFamily: "Fira Code, monospace",
                    smoothScrolling: true,
                }}
            />
        </div>
    );
}
