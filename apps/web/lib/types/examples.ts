// Example usage of shared types in the web app
// Import from lib/types
import { KnowledgeGraph, GraphNode, GraphLink } from '@/lib/types';

// Example: Type-safe graph data
const exampleGraph: KnowledgeGraph = {
  id: '1',
  name: 'Medical Knowledge Graph',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

const exampleNode: GraphNode = {
  id: 'node-1',
  label: 'Disease',
  properties: {
    name: 'Type 2 Diabetes',
    category: 'endocrine',
  },
};

const exampleLink: GraphLink = {
  id: 'link-1',
  source: 'node-1',
  target: 'node-2',
  label: 'causes',
  properties: {
    confidence: 0.95,
  },
};

export { exampleGraph, exampleNode, exampleLink };
