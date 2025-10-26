'use client';

import dynamic from 'next/dynamic';
import type { GraphNode, GraphLink } from '@/lib/types';
import WikidataInput from './WikidataInput';
import { useGraphData } from '@/lib/hooks/useGraphData';

// Dynamically import ForceGraph2D to avoid SSR issues
const ForceGraph2D = dynamic(() => import('react-force-graph-2d'), { ssr: false });

export default function GraphView() {
  const { data, loading, error } = useGraphData(); // No initial graph ID - start with empty state

  // Handler for Wikidata entity loading
  const handleWikidataLoad = (entityData: { nodes: GraphNode[]; links: GraphLink[] }) => {
    // WikidataInput handles its own data loading
    // We keep this handler for compatibility but the data is managed by the hook
    // In a future refactor, WikidataInput could be updated to use the hook's loadWikidataEntity
    console.log('Wikidata data loaded:', entityData);
  };

  return (
    <div className="flex h-full gap-4">
      {/* Main Panel - Graph Visualization Area */}
      <div className="flex-1 bg-white rounded-lg border border-[#E5E7EB] p-6">
        {/* Wikidata Input */}
        <WikidataInput onEntityLoad={handleWikidataLoad} />

        {loading && (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#E57373]"></div>
            <p className="mt-4 text-[#6B7280]">Loading graph...</p>
          </div>
        )}

        {error && (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="text-red-500 mb-4">
              <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <p className="text-[#1C1C1C] font-semibold mb-2">Failed to load graph</p>
            <p className="text-[#6B7280] text-sm">{error}</p>
          </div>
        )}

        {!loading && !error && (
          <div className="h-full">
            <ForceGraph2D
              graphData={data}
              nodeLabel={(node) => (node as GraphNode).label}
              nodeColor={() => '#E57373'}
              linkColor={() => '#6B7280'}
              linkLabel={(link) => (link as GraphLink).label}
              enableZoomInteraction={true}
              enablePanInteraction={true}
              enableNodeDrag={true}
              width={undefined}
              height={undefined}
              nodeRelSize={6}
              linkWidth={2}
              linkDirectionalArrowLength={3.5}
              linkDirectionalArrowRelPos={1}
              nodeCanvasObject={(node, ctx, globalScale) => {
                const label = (node as GraphNode).label;
                const fontSize = 12 / globalScale;
                ctx.font = `${fontSize}px Sans-Serif`;
                const textWidth = ctx.measureText(label).width;
                const bckgDimensions = [textWidth, fontSize].map((n) => n + fontSize * 0.2);

                // Draw node circle
                ctx.fillStyle = '#E57373';
                ctx.beginPath();
                ctx.arc(node.x!, node.y!, 6, 0, 2 * Math.PI, false);
                ctx.fill();

                // Draw label background
                ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.fillRect(
                  node.x! - bckgDimensions[0] / 2,
                  node.y! + 8,
                  bckgDimensions[0],
                  bckgDimensions[1]
                );

                // Draw label text
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = '#1C1C1C';
                ctx.fillText(label, node.x!, node.y! + 8 + bckgDimensions[1] / 2);
              }}
            />
          </div>
        )}
      </div>

      {/* Side Panel - Inspector */}
      <div className="w-80 bg-white rounded-lg border border-[#E5E7EB] p-6">
        <div className="flex flex-col h-full">
          <h3 className="text-lg font-semibold text-[#1C1C1C] mb-4">Node Inspector</h3>
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center text-[#6B7280]">
              <p className="mb-2">Select a node to view details</p>
              <p className="text-sm">Node properties and relationships will appear here</p>
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
