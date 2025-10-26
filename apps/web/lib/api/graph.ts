/**
 * API client functions for graph data fetching
 */

import type { GraphNode, GraphLink } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
  metadata?: Record<string, unknown>;
}

/**
 * Fetch graph data for a specific graph ID
 *
 * @param graphId - The unique identifier of the graph
 * @returns Promise resolving to graph data with nodes and links
 */
export async function fetchGraphData(graphId: string): Promise<GraphData> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/graph/${graphId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch graph data: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data as GraphData;
  } catch (error) {
    console.error('Error fetching graph data:', error);
    throw new Error(
      error instanceof Error
        ? `Failed to fetch graph data: ${error.message}`
        : 'Failed to fetch graph data'
    );
  }
}

/**
 * Fetch Wikidata graph for a specific entity
 *
 * @param entityId - Wikidata entity ID (e.g., "Q90" for Paris)
 * @param depth - Depth of traversal (1-3, default: 1)
 * @returns Promise resolving to graph data with nodes and links
 */
export async function fetchWikidataGraph(entityId: string, depth: number = 1): Promise<GraphData> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/wikidata/visualize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ entity_id: entityId, depth }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail ||
          `Failed to fetch Wikidata graph: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    return data as GraphData;
  } catch (error) {
    console.error('Error fetching Wikidata graph:', error);
    throw new Error(
      error instanceof Error
        ? `Failed to fetch Wikidata graph: ${error.message}`
        : 'Failed to fetch Wikidata graph'
    );
  }
}

/**
 * Fetch Wikidata graph from a Wikidata URL
 *
 * @param wikidataUrl - Full Wikidata URL (e.g., "https://www.wikidata.org/wiki/Q90")
 * @param depth - Depth of traversal (1-3, default: 1)
 * @returns Promise resolving to graph data with nodes and links
 */
export async function fetchWikidataGraphFromUrl(wikidataUrl: string, depth: number = 1): Promise<GraphData> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/wikidata/visualize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ wikidata_url: wikidataUrl, depth }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail ||
          `Failed to fetch Wikidata graph: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    return data as GraphData;
  } catch (error) {
    console.error('Error fetching Wikidata graph from URL:', error);
    throw new Error(
      error instanceof Error
        ? `Failed to fetch Wikidata graph: ${error.message}`
        : 'Failed to fetch Wikidata graph'
    );
  }
}
