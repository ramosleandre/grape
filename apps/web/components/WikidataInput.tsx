/**
 * WikidataInput Component
 *
 * Allows users to input a Wikidata URL or Entity ID and visualize the entity's knowledge graph.
 */

'use client';

import { useState } from 'react';
import { fetchWikidataGraph, fetchWikidataGraphFromUrl } from '@/lib/api/graph';
import type { GraphNode, GraphLink } from '@/lib/types';

interface WikidataInputProps {
  onEntityLoad: (data: { nodes: GraphNode[]; links: GraphLink[] }) => void;
}

export default function WikidataInput({ onEntityLoad }: WikidataInputProps) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleVisualize = async () => {
    if (!input.trim()) {
      setError('Please enter a Wikidata URL or Entity ID');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Determine if input is a URL or entity ID
      const isUrl = input.startsWith('http://') || input.startsWith('https://');

      const data = isUrl
        ? await fetchWikidataGraphFromUrl(input.trim())
        : await fetchWikidataGraph(input.trim());

      onEntityLoad({
        nodes: data.nodes,
        links: data.links,
      });
    } catch (err) {
      console.error('Failed to load Wikidata entity:', err);
      setError(err instanceof Error ? err.message : 'Failed to load Wikidata entity');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleVisualize();
    }
  };

  return (
    <div className="mb-4">
      <div className="flex gap-2">
        <div className="flex-1">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter Wikidata URL or Entity ID (e.g., Q90 for Paris)"
            className="w-full px-4 py-2 border border-[#E5E7EB] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#E57373] focus:border-transparent"
            disabled={loading}
          />
        </div>
        <button
          onClick={handleVisualize}
          disabled={loading || !input.trim()}
          className="px-6 py-2 bg-[#E57373] text-white rounded-lg font-medium hover:bg-[#D55555] transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Loading...</span>
            </>
          ) : (
            <span>Visualize</span>
          )}
        </button>
      </div>

      {error && (
        <div className="mt-2 text-sm text-red-500 flex items-center gap-2">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span>{error}</span>
        </div>
      )}

      <div className="mt-2 text-xs text-[#6B7280]">
        <p>Try: Q90 (Paris), Q5 (Human), Q2 (Earth), or paste a full Wikidata URL</p>
      </div>
    </div>
  );
}
