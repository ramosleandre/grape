'use client';

import { useState } from 'react';
import TopBar from '@/components/TopBar';
import GraphView from '@/components/GraphView';
import QueryView from '@/components/QueryView';

type TabType = 'graph' | 'query';

export default function WorkspacePage() {
  const [activeTab, setActiveTab] = useState<TabType>('graph');

  return (
    <div className="flex flex-col h-screen bg-[#FDFDFD]">
      {/* Top Bar */}
      <TopBar projectName="My Knowledge Graph" />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Tab Navigation */}
        <div className="bg-white border-b border-[#E5E7EB]">
          <div className="px-6 flex gap-1">
            <button
              onClick={() => setActiveTab('graph')}
              className={`px-6 py-4 text-sm font-medium transition-colors relative ${
                activeTab === 'graph' ? 'text-[#E57373]' : 'text-[#6B7280] hover:text-[#1C1C1C]'
              }`}
            >
              Graph View
              {activeTab === 'graph' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E57373]" />
              )}
            </button>
            <button
              onClick={() => setActiveTab('query')}
              className={`px-6 py-4 text-sm font-medium transition-colors relative ${
                activeTab === 'query' ? 'text-[#E57373]' : 'text-[#6B7280] hover:text-[#1C1C1C]'
              }`}
            >
              Query View
              {activeTab === 'query' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E57373]" />
              )}
            </button>
          </div>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-hidden p-6">
          {activeTab === 'graph' ? <GraphView /> : <QueryView />}
        </div>
      </div>
    </div>
  );
}
