import React from 'react';
import ReactMarkdown from 'react-markdown';
import { AlertCircle, CheckCircle, Code } from 'lucide-react';

export function AnalysisResult({ result }) {
    if (!result) return null;

    const { lines, complexity, ai_feedback, issues } = result;

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Summary Cards */}
            <div className="grid grid-cols-3 gap-4">
                <StatsCard icon={<Code />} label="Lines" value={lines} />
                <StatsCard icon={<AlertCircle />} label="Complexity" value={complexity} />
                <StatsCard icon={<CheckCircle />} label="Issues" value={issues.length} />
            </div>

            {/* AI Summary */}
            {ai_feedback && (
                <div className="glass-panel p-6">
                    <h3 className="text-[var(--text-accent)] font-semibold mb-3 flex items-center gap-2">
                        AI Summary
                    </h3>
                    <div className="prose prose-invert max-w-none text-sm leading-relaxed text-[var(--text-primary)]">
                        {ai_feedback.summary}
                        {ai_feedback.summary === "Analysis failed" && ai_feedback.issues && (
                            <div className="mt-3 p-3 bg-red-500/20 rounded text-red-200 font-mono text-xs">
                                {ai_feedback.issues[0]?.message}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Detailed Issues */}
            {issues.length > 0 && (
                <div className="space-y-3">
                    <h3 className="text-[var(--text-primary)] font-semibold text-sm uppercase tracking-wider opacity-70">
                        Issues Found
                    </h3>
                    {issues.map((issue, idx) => (
                        <div key={idx} className={`p-4 rounded-lg border flex gap-3 ${issue.severity === 'critical' ? 'bg-red-500/10 border-red-500/30' :
                            issue.severity === 'high' ? 'bg-orange-500/10 border-orange-500/30' :
                                'bg-[var(--bg-tertiary)] border-[var(--border-color)]'
                            }`}>
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                    <span className={`text-xs px-2 py-0.5 rounded uppercase font-bold ${issue.severity === 'critical' ? 'bg-red-500 text-white' :
                                        issue.severity === 'high' ? 'bg-orange-500 text-white' :
                                            'bg-gray-600 text-gray-200'
                                        }`}>{issue.severity}</span>
                                    <span className="text-xs font-mono text-[var(--text-secondary)]">Line {issue.line}</span>
                                </div>
                                <p className="text-sm font-medium text-[var(--text-primary)]">{issue.message}</p>
                                {issue.suggestion && (
                                    <p className="text-xs text-[var(--text-secondary)] mt-1 ml-1 pl-2 border-l-2 border-[var(--text-secondary)]">
                                        Suggested: {issue.suggestion}
                                    </p>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

function StatsCard({ icon, label, value }) {
    return (
        <div className="glass-panel p-4 flex items-center gap-4">
            <div className="p-2 rounded-full bg-[var(--bg-primary)] text-[var(--primary-color)]">
                {React.cloneElement(icon, { size: 20 })}
            </div>
            <div>
                <div className="text-xs text-[var(--text-secondary)] uppercase">{label}</div>
                <div className="text-xl font-bold font-mono text-[var(--text-primary)]">{value}</div>
            </div>
        </div>
    );
}
