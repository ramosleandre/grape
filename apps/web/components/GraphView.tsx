'use client';

export default function GraphView() {
  return (
    <div className="flex h-full gap-4">
      {/* Main Panel - Graph Visualization Area */}
      <div className="flex-1 bg-white rounded-lg border border-[#E5E7EB] p-6">
        <div className="flex flex-col items-center justify-center h-full text-center">
          <div className="mb-4">
            <svg
              className="w-24 h-24 text-[#E5E7EB]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-[#1C1C1C] mb-2">
            Knowledge Graph Visualization
          </h3>
          <p className="text-[#6B7280] max-w-md">
            This area will display your interactive knowledge graph. 
            You'll be able to pan, zoom, and click on nodes to explore relationships.
          </p>
          <div className="mt-6 space-y-2 text-sm text-[#6B7280]">
            <p>• Pan and zoom to navigate</p>
            <p>• Click nodes to inspect details</p>
            <p>• Drag to rearrange layout</p>
          </div>
        </div>
      </div>

      {/* Side Panel - Inspector */}
      <div className="w-80 bg-white rounded-lg border border-[#E5E7EB] p-6">
        <div className="flex flex-col h-full">
          <h3 className="text-lg font-semibold text-[#1C1C1C] mb-4">
            Node Inspector
          </h3>
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center text-[#6B7280]">
              <p className="mb-2">Select a node to view details</p>
              <p className="text-sm">
                Node properties and relationships will appear here
              </p>
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-[#E5E7EB]">
            <button
              className="w-full px-4 py-2 bg-[#E57373] text-white rounded-lg font-medium hover:bg-[#D55555] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              disabled
            >
              Edit Node
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
