'use client';

import { useState } from 'react';

export default function QueryView() {
  const [query, setQuery] = useState('');

  return (
    <div className="flex h-full gap-4">
      {/* Chat Panel */}
      <div className="flex-1 bg-white rounded-lg border border-[#E5E7EB] flex flex-col">
        {/* Chat Header */}
        <div className="px-6 py-4 border-b border-[#E5E7EB]">
          <h3 className="text-lg font-semibold text-[#1C1C1C]">Gentoo KGBot</h3>
          <p className="text-sm text-[#6B7280] mt-1">Ask questions about your knowledge graph</p>
        </div>

        {/* Chat Messages Area */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="mb-4">
              <svg
                className="w-16 h-16 text-[#E57373]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <h4 className="text-lg font-semibold text-[#1C1C1C] mb-2">Start a Conversation</h4>
            <p className="text-[#6B7280] max-w-md">
              Ask Gentoo KGBot anything about your knowledge graph. All answers are sourced directly
              from your data.
            </p>
            <div className="mt-6 space-y-2 text-sm text-[#6B7280]">
              <p>• Responses are 100% traceable to graph nodes</p>
              <p>• See the reasoning path visualization</p>
              <p>• Natural language understanding</p>
            </div>
          </div>
        </div>

        {/* Chat Input */}
        <div className="px-6 py-4 border-t border-[#E5E7EB]">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question about your knowledge graph..."
              className="flex-1 px-4 py-3 text-sm border border-[#E5E7EB] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#E57373] focus:border-transparent placeholder:text-[#6B7280]"
              disabled
            />
            <button
              className="px-6 py-3 bg-[#E57373] text-white rounded-lg font-medium hover:bg-[#D55555] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              disabled
            >
              Send
            </button>
          </div>
        </div>
      </div>

      {/* Reasoning Panel */}
      <div className="w-96 bg-white rounded-lg border border-[#E5E7EB] p-6">
        <div className="flex flex-col h-full">
          <h3 className="text-lg font-semibold text-[#1C1C1C] mb-4">Reasoning Path</h3>
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center text-[#6B7280]">
              <div className="mb-4">
                <svg
                  className="w-20 h-20 text-[#E5E7EB] mx-auto"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                  />
                </svg>
              </div>
              <p className="mb-2 font-medium">Visual Reasoning Path</p>
              <p className="text-sm">
                When the agent responds, this panel will show the logical path it took through your
                knowledge graph
              </p>
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-[#E5E7EB] text-xs text-[#6B7280]">
            <p>💡 The reasoning path updates in real-time as the agent constructs its answer</p>
          </div>
        </div>
      </div>
    </div>
  );
}
