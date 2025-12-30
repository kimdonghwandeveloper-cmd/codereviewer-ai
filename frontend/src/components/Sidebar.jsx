import React from 'react';
import { History, Plus, MessageSquare } from 'lucide-react';

export function Sidebar() {
    return (
        <div className="w-[260px] flex-shrink-0 bg-[var(--bg-secondary)] border-r border-[var(--border-color)] flex flex-col">
            {/* Header / New Chat */}
            <div className="p-3">
                <button className="w-full flex items-center gap-3 px-3 py-3 rounded-md border border-[var(--border-color)] hover:bg-[var(--bg-tertiary)] transition-colors text-sm text-left text-[var(--text-primary)]">
                    <Plus size={16} />
                    <span>New Analysis</span>
                </button>
            </div>

            {/* History List */}
            <div className="flex-1 overflow-y-auto px-3 py-2 space-y-2">
                <div className="text-xs font-semibold text-[var(--text-secondary)] px-3 mb-2">Recent</div>

                {/* Dummy Items */}
                {['Authentication Logic', 'Data Processing', 'API Endpoint'].map((item, i) => (
                    <button key={i} className="w-full flex items-center gap-3 px-3 py-3 rounded-md hover:bg-[var(--bg-tertiary)] group transition-colors text-sm text-[var(--text-primary)]">
                        <MessageSquare size={16} className="text-[var(--text-secondary)] group-hover:text-[var(--text-primary)]" />
                        <span className="truncate">{item}</span>
                    </button>
                ))}
            </div>

            {/* Footer */}
            <div className="p-3 border-t border-[var(--border-color)] text-xs text-[var(--text-secondary)]">
                CodeReviewer AI v1.0
            </div>
        </div>
    );
}
