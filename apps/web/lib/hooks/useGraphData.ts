/**
 * useGraphData Hook
 *
 * Custom React hook for managing graph data state and operations.
 */

import { useState, useCallback, useEffect } from 'react';
import { fetchGraphData, fetchWikidataGraph } from '@/lib/api/graph';
import type { GraphNode, GraphLink } from '@/lib/types';

export interface UseGraphDataReturn {
  data: { nodes: GraphNode[]; links: GraphLink[] };
  loading: boolean;
  error: string | null;
  refetch: (graphId?: string) => Promise<void>;
  loadWikidataEntity: (entityId: string) => Promise<void>;
  clearError: () => void;
}

/**
 * Hook for managing graph data fetching and state
 *
 * @param initialGraphId - Optional initial graph ID to fetch on mount
 * @returns Graph data state and operations
 */
export function useGraphData(initialGraphId?: string): UseGraphDataReturn {
  const [data, setData] = useState<{ nodes: GraphNode[]; links: GraphLink[] }>({
    nodes: [],
    links: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refetch = useCallback(
    async (graphId?: string) => {
      try {
        setLoading(true);
        setError(null);
        const graphData = await fetchGraphData(graphId || initialGraphId || 'placeholder');
        setData({
          nodes: graphData.nodes,
          links: graphData.links,
        });
      } catch (err) {
        console.error('Failed to fetch graph data:', err);
        setError(err instanceof Error ? err.message : 'Failed to fetch graph data');
      } finally {
        setLoading(false);
      }
    },
    [initialGraphId]
  );

  const loadWikidataEntity = useCallback(async (entityId: string) => {
    try {
      setLoading(true);
      setError(null);
      const graphData = await fetchWikidataGraph(entityId);
      setData({
        nodes: graphData.nodes,
        links: graphData.links,
      });
    } catch (err) {
      console.error('Failed to load Wikidata entity:', err);
      setError(err instanceof Error ? err.message : 'Failed to load Wikidata entity');
    } finally {
      setLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Auto-load initial data on mount only if initialGraphId is provided
  useEffect(() => {
    if (initialGraphId) {
      refetch();
    } else {
      // No initial graph to load, set loading to false
      setLoading(false);
    }
  }, [initialGraphId, refetch]);

  return {
    data,
    loading,
    error,
    refetch,
    loadWikidataEntity,
    clearError,
  };
}
