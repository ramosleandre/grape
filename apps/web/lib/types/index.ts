export interface KnowledgeGraph {
  id: string;
  name: string;
  createdAt: string; // ISO 8601
  updatedAt: string; // ISO 8601
}

export interface GraphNode {
  id: string;
  label: string;
  properties: Record<string, any>;
}

export interface GraphLink {
  id: string;
  source: string; // ID of source GraphNode
  target: string; // ID of target GraphNode
  label: string;
  properties: Record<string, any>;
}
