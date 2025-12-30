import React from 'react';
import { Sidebar } from './Sidebar';

export function Layout({ children }) {
    return (
        <div className="flex h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans overflow-hidden">
            <Sidebar />
            <main className="flex-1 flex flex-col relative overflow-hidden">
                {children}
            </main>
        </div>
    );
}
