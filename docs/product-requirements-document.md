### **Grape Product Requirements Document (PRD)**

### **Goals and Background Context**

#### **Goals**

*   To enhance AI reliability by ensuring every piece of information delivered is verifiable and directly traceable to its source within a knowledge graph.
*   To break down knowledge silos by enabling the creation of logical bridges between different structured knowledge sources.
*   To offer an intuitive interface for non-specialists to explore, edit, and query complex knowledge bases, thereby improving human-computer interaction.
*   To provide tools that visualize and demystify the logical steps taken by the AI agent, making its reasoning process fully transparent.

#### **Background Context**

The core problem Grape addresses is that knowledge is often compartmentalized, making it difficult to gain a comprehensive, reliable overview of a subject. While Large Language Models (LLMs) are powerful, their "black box" nature and lack of source transparency limit their trustworthiness for critical applications.

Grape is designed to solve this by merging the natural language capabilities of LLMs with the logical rigor of knowledge graphs. It will be a system where users can build, explore, and query complex knowledge corpuses through a conversational agent, with the assurance that all information is reliably sourced and the AI's reasoning is fully transparent.

#### **Change Log**

| Date | Version | Description | Author |
| :--- | :--- | :--- | :--- |
|      | 1.0     | Initial Draft | Youssef Mehili |

### **Requirements**

#### **Functional**

1.  **FR1:** The system shall automatically generate a Knowledge Graph by analyzing the content of user-uploaded PDF documents.
2.  **FR2:** The system shall automatically generate a Knowledge Graph by analyzing the content of a user-provided web page URL.
3.  **FR3:** The system shall allow users to import a pre-existing Knowledge Graph in the standard RDF format.
4.  **FR4:** A graphical user interface shall be provided to display the Knowledge Graph visually.
5.  **FR5:** Users shall be able to manually edit the information within a node by interacting with it on the visual graph.
6.  **FR6:** Users shall be able to manually add, delete, or modify the links (relationships) between nodes on the visual graph.
7.  **FR7:** The system shall provide an AI-assisted editing tool that accepts natural language commands to manipulate the graph (e.g., "select nodes related to ontology," "delete information before 2020").
8.  **FR8:** The system shall include a conversational agent (Gentoo KGBot) that allows users to query the Knowledge Graph using natural language questions.
9.  **FR9:** The conversational agent's responses must be generated exclusively from the information contained within the active Knowledge Graph.
10. **FR10:** The agent must translate the user's natural language question into a formal SPARQL query to retrieve information from the graph.
11. **FR11:** Users shall be able to select a specific portion of the graph, constraining the conversational agent's context to only that subset of information for its answers.
12. **FR12:** Alongside its text-based answer, the system shall generate a second, dynamic graph that visualizes the reasoning path the agent took through the Knowledge Graph.
13. **FR13:** The reasoning path visualization must display the specific nodes and links the agent traversed to construct its answer in near real-time.

#### **Non Functional**

1.  **NFR1 (Usability):** The user interface must be intuitive and usable by non-specialists with minimal to no prior training in knowledge graph technology.
2.  **NFR2 (Reliability):** Every statement of fact in the agent's responses must be 100% traceable to a node or link within the Knowledge Graph. The agent shall not infer or invent information.
3.  **NFR3 (Performance):** The reasoning path visualization should update interactively, without perceptible lag, as the agent formulates its response.
4.  **NFR4 (Compatibility):** The system must adhere to standard RDF formats for import/export to ensure interoperability with other graph-based tools.
5.  **NFR5 (Security):** User-uploaded documents and the knowledge graphs derived from them must be stored securely, ensuring data privacy and integrity.

### **User Interface Design Goals**

#### **Overall UX Vision**

The user experience should feel like an intellectual co-pilot. The interface will be clean, professional, and data-forward, prioritizing the knowledge graph itself. It should empower users to feel in control of a complex system through intuitive interactions, making sophisticated data exploration accessible and transparent. The core loop is: **build, see, ask, and understand.**

#### **Key Interaction Paradigms**

The UI will be built around three primary modes of interaction:

1.  **Direct Manipulation:** A visual, canvas-like area where users can directly interact with the graph (pan, zoom, click, drag-and-drop) to explore and make manual edits.
2.  **Conversational Command:** Text-based input areas for both the graph editing AI and the Gentoo KGBot, allowing users to perform complex actions using natural language.
3.  **Visual Feedback:** The dynamic "reasoning path" graph will provide real-time, animated feedback that directly correlates with the agent's textual response, visually connecting the answer to the evidence.

#### **Core Screens and Views**

*   **Project Dashboard:** A landing area to manage different knowledge graphs (projects). Users can create a new graph (from PDF/URL), import an existing one (RDF), or open a recent project.
*   **Graph Workspace View:** This is the main interface, likely a multi-panel layout:
    *   **Main Panel:** The interactive knowledge graph visualization.
    *   **Side Panel (Inspector):** Displays details of a selected node or link and provides editing fields.
    *   **Top Bar/Panel:** Contains the AI-assisted editing command input.
*   **Query & Reasoning View:**
    *   **Chat Interface:** A dedicated area for conversing with the Gentoo KGBot.
    *   **Reasoning Panel:** A synchronized view showing the "reasoning path" graph as the agent responds.

#### **Accessibility: WCAG AA**

The application will be designed to meet WCAG 2.1 AA standards, ensuring it is usable by people with a wide range of disabilities.

#### **Branding**

The branding will be clean, modern, and professional, evoking a sense of intelligence and clarity. We will use a color palette that emphasizes readability and helps differentiate elements in the graph visualization (e.g., node types, link types). A simple, clear logo for "Grape" will be needed.

#### **Target Device and Platforms: Web Responsive**

The primary platform will be a responsive web application, optimized for desktop and tablet use where screen real estate is sufficient for graph visualization. A mobile-optimized "read-only" or query-focused view may be considered for smaller screens.

### **Technical Assumptions**

#### **Repository Structure: Monorepo**

A monorepo is recommended to manage the entire project's code in a single repository. This approach will simplify dependency management and ensure consistency, especially for shared code (like data types) between the frontend and backend services.

#### **Service Architecture: Serverless on Google Cloud**

A serverless architecture using **Google Cloud Functions** is recommended for the backend. This is well-suited for the modular nature of the project (PDF processing, graph manipulation, querying) and offers benefits in scalability and cost-efficiency. **Cloud Run** is also a viable alternative for the containerized FastAPI services.

#### **Testing Requirements: Full Testing Pyramid**

The project will adhere to a full testing pyramid strategy, including:
*   **Unit Tests:** For individual functions and components.
*   **Integration Tests:** To verify interactions between different services (e.g., API and database).
*   **End-to-End (E2E) Tests:** To validate critical user flows through the entire system.

#### **Additional Technical Assumptions and Requests**

*   **Hosting:** All project components will be deployed and hosted on the **Google Cloud Platform**. The Next.js frontend can be hosted on **Firebase Hosting** or **Vercel** (which integrates well with GCP), with backend services on **Cloud Run** (ideal for FastAPI).
*   **Frontend:** The frontend will be built with the **Next.js** framework (a React framework). The graph visualization will be implemented using the **react-force-graph** library.
*   **Backend:** The backend API will be built with **Python** using the **FastAPI** framework.
*   **Database:** The core of the system will be a **Graph Database** that supports the RDF model and SPARQL queries. For the hackathon, using a managed service from the **Google Cloud Marketplace**, such as **Neo4j Aura**, is the recommended approach.
*   **LLM Integration:** The architecture will primarily leverage Google's **Vertex AI Platform** and its **Gemini family of models** for the LLM-driven tasks. The system should still be designed to treat the specific model endpoint as a configurable component to allow for flexibility.

### **Epic List**

*   **Epic 1: Foundation & Core Infrastructure:** Establish the project setup, a basic Next.js frontend, a FastAPI backend, and the core Knowledge Graph import/export functionality. This ensures the foundational pieces are in place and connected.
*   **Epic 2: Interactive Graph Visualization & Manual Editing:** Implement the visual graph interface, allowing users to see their imported graph and perform manual edits (modify nodes, add/delete links).
*   **Epic 3: AI-Powered Graph Manipulation & Querying:** Introduce the AI agents. This includes implementing the AI-assisted editing commands and the core functionality of the Gentoo KGBot to answer questions based on the graph.
*   **Epic 4: Reasoning Path Visualization & Contextual Querying:** Develop the final layer of transparency by implementing the dynamic reasoning path graph and the ability to constrain the agent's context to a subgraph.
*   **Epic 5: GCP Deployment & Operational Readiness:** Configure the full Google Cloud Platform infrastructure, set up CI/CD pipelines, and implement monitoring, logging, and security best practices for a production-ready application.

### **Epic 1: Foundation & Core Infrastructure**

**Epic Goal:** To establish the complete project skeleton, including the monorepo, a basic Next.js frontend, and a functional FastAPI backend. This epic delivers the core capability of importing a knowledge graph into the system, ensuring the foundational pieces are in place and correctly connected before more complex features are built.

#### **Story 1.1: Project Scaffolding**

**As a** developer,
**I want** a properly configured monorepo with separate Next.js and FastAPI packages,
**so that** I have a stable and organized environment for building and testing the application.

**Acceptance Criteria:**
1.  A monorepo is initialized with appropriate tooling (e.g., npm workspaces).
2.  A boilerplate Next.js application is created within the monorepo (`apps/web`).
3.  A boilerplate FastAPI application is created within the monorepo (`apps/api`).
4.  A shared package (`packages/shared-types`) is created for common TypeScript types.
5.  A developer can run the frontend and backend applications concurrently with a single command.
6.  Linters and code formatters are configured for both applications.

#### **Story 1.2: Basic UI Application Shell**

**As a** user,
**I want** to see the main application layout with all its key panels,
**so that** I can understand the structure of the workspace.

**Acceptance Criteria:**
1.  The Next.js application displays a multi-panel layout as defined in the UI goals (Main Panel, Side Panel, Top Bar, Query/Reasoning View).
2.  Each panel contains placeholder text or a simple wireframe indicating its future purpose.
3.  The main layout is responsive and adjusts appropriately for tablet and desktop screen sizes.
4.  There is a clear area designated for graph visualization.

#### **Story 1.3: Knowledge Graph Import API**

**As a** developer,
**I want** a FastAPI endpoint that can accept and store a user-uploaded Knowledge Graph in RDF format,
**so that** data can be brought into the system for later processing.

**Acceptance Criteria:**
1.  A FastAPI endpoint `/import/rdf` is created that accepts a file upload.
2.  The endpoint validates that the uploaded file is a valid RDF file.
3.  Upon successful validation, the graph data is saved to a new instance in the graph database (e.g., Neo4j Aura).
4.  The API returns a success response with a unique ID for the newly imported graph.
5.  The API returns a meaningful error response if the file is invalid or the import fails.

#### **Story 1.4: Connect UI to RDF Import Endpoint**

**As a** user,
**I want** to be able to upload an RDF file through the user interface,
**so that** I can import my existing knowledge graphs into Grape.

**Acceptance Criteria:**
1.  The UI shell contains a clearly labeled "Import RDF" button.
2.  Clicking the button opens a system file selector.
3.  Selecting a valid RDF file and confirming triggers a call to the `/import/rdf` API endpoint.
4.  The UI displays a loading indicator while the file is being uploaded and processed.
5.  The UI displays a clear success message upon a successful API response.
6.  The UI displays a helpful error message if the API returns an error.

### **Epic 2: Interactive Graph Visualization & Manual Editing**

**Epic Goal:** To provide a rich, interactive visual interface for the user's knowledge graph. This epic will deliver the core functionality of exploring the graph's structure and making manual edits to its nodes and relationships, empowering users to directly curate their knowledge base.

#### **Story 2.1: Basic Knowledge Graph Visualization**

**As a** user,
**I want** to see my imported knowledge graph displayed visually,
**so that** I can explore its structure and understand the relationships between entities.

**Acceptance Criteria:**
1.  After a graph is imported, the main panel of the workspace displays a graph visualization using the `react-force-graph` library.
2.  A new FastAPI endpoint `/graph/{graph_id}` is created to fetch the data of a specific graph from the database.
3.  The Next.js frontend calls this API endpoint to retrieve the graph data for the selected project.
4.  Nodes and links from the graph data are rendered correctly on the canvas.
5.  The user can interact with the graph by panning and zooming.

#### **Story 2.2: Node Inspection and Editing**

**As a** user,
**I want** to click on a node to view its detailed information and edit it,
**so that** I can correct, update, or enrich the concepts in my graph.

**Acceptance Criteria:**
1.  Clicking on a node in the graph visualization selects and highlights it.
2.  The properties and metadata of the selected node are displayed in the Side Panel (Inspector).
3.  The fields in the Side Panel are editable.
4.  A new FastAPI endpoint `PATCH /graph/{graph_id}/node/{node_id}` is created to handle updates to a node.
5.  Saving the changes in the Side Panel triggers an API call to the update endpoint.
6.  The graph visualization and inspector panel reflect the updated information upon a successful response.

#### **Story 2.3: Manual Node and Link Creation**

**As a** user,
**I want** to manually add new nodes and create links between them,
**so that** I can expand my knowledge graph with new information directly from the interface.

**Acceptance Criteria:**
1.  The UI provides a clear and intuitive action to add a new, empty node to the graph canvas.
2.  The UI allows a user to create a directional link between two existing nodes (e.g., by dragging from a source node to a target node).
3.  Adding a node triggers a `POST /graph/{graph_id}/node` API call.
4.  Adding a link triggers a `POST /graph/{graph_id}/link` API call.
5.  The graph visualization updates immediately to show the new node or link.
6.  Newly created nodes and links can be immediately selected and edited via the inspector panel.

#### **Story 2.4: Manual Node and Link Deletion**

**As a** user,
**I want** to delete nodes and links from the graph,
**so that** I can remove irrelevant or incorrect information.

**Acceptance Criteria:**
1.  The UI provides a clear action to delete a selected node or a selected link.
2.  A confirmation prompt is displayed before any destructive action is taken (e.g., "Are you sure you want to delete this node?").
3.  Deleting a node triggers a `DELETE /graph/{graph_id}/node/{node_id}` API call.
4.  Deleting a link triggers a `DELETE /graph/{graph_id}/link/{link_id}` API call.
5.  The graph visualization updates immediately to remove the deleted element.

### **Epic 3: AI-Powered Graph Manipulation & Querying**

**Epic Goal:** To introduce the two primary AI agents into the Grape application. This epic will deliver the functionality for users to generate graphs automatically from documents and to manipulate and query their knowledge graphs using natural language, transforming the tool from a manual editor into an intelligent knowledge co-pilot.

#### **Story 3.1: LLM-Powered Knowledge Graph Generation**

**As a** user,
**I want** to provide a PDF document or a URL,
**so that** the system can automatically analyze the content and generate a knowledge graph for me.

**Acceptance Criteria:**
1.  The UI is updated with options to "Create Graph from PDF" and "Create Graph from URL".
2.  A new FastAPI endpoint `/generate/graph` is created that accepts a file upload (PDF) or a URL.
3.  The backend service uses a Vertex AI (Gemini) model to parse the document, extract key entities and their relationships, and structure them into a valid RDF format.
4.  The generated graph data is saved to a new instance in the graph database.
5.  The API returns a success response with the new graph's ID, which then loads in the visualization panel.
6.  The UI provides clear feedback on the generation process (e.g., "Analyzing document...", "Building graph...").

#### **Story 3.2: AI-Assisted Graph Editing Backend**

**As a** developer,
**I want** a backend service that translates natural language commands into specific graph manipulation actions,
**so that** users can perform complex edits with simple text commands.

**Acceptance Criteria:**
1.  A new FastAPI endpoint `/graph/{graph_id}/edit-ai` is created that accepts a natural language command as a text string.
2.  The service uses a Vertex AI (Gemini) model to interpret the command's intent (e.g., select, delete, add link).
3.  The service translates the intent into a specific sequence of graph database operations.
4.  The service executes these operations on the specified graph.
5.  The API returns a confirmation of the action performed (e.g., "Deleted 15 nodes dated before 2020.").
6.  The service can handle at least three distinct types of commands: selection, deletion based on properties, and link creation.

#### **Story 3.3: AI-Assisted Editing UI Integration**

**As a** user,
**I want** to type commands in natural language in the UI to edit the graph,
**so that** I can perform complex or bulk edits efficiently.

**Acceptance Criteria:**
1.  The AI-assisted editing command input in the top bar is now functional.
2.  Submitting a command in the input triggers a call to the `/graph/{graph_id}/edit-ai` endpoint.
3.  The UI displays a loading indicator while the command is being processed.
4.  The graph visualization automatically refreshes to show the result of the executed command.
5.  The confirmation message from the API is displayed to the user in the UI.

#### **Story 3.4: Gentoo KGBot Backend (SPARQL Generation)**

**As a** developer,
**I want** a backend service that can translate a user's natural language question into a SPARQL query,
**so that** I can reliably retrieve sourced answers from the knowledge graph.

**Acceptance Criteria:**
1.  A new FastAPI endpoint `/graph/{graph_id}/query-agent` is created that accepts a natural language question.
2.  The service uses a Vertex AI (Gemini) model to analyze the question and convert it into a valid SPARQL query.
3.  The service executes the SPARQL query against the specified graph in the database.
4.  The service formats the query results into a clear, human-readable text answer.
5.  The response from the endpoint includes both the text answer and the raw data/nodes retrieved by the SPARQL query.

#### **Story 3.5: Gentoo KGBot UI Integration**

**As a** user,
**I want** to ask questions in the chat interface and receive answers based on the graph,
**so that** I can easily find information within my knowledge base.

**Acceptance Criteria:**
1.  The chat interface in the Query & Reasoning View is now functional.
2.  Submitting a question triggers a call to the `/graph/{graph_id}/query-agent` endpoint.
3.  The text answer from the API is displayed in the chat history.
4.  The UI provides a clear separation between user questions and agent responses.
5.  The chat interface includes a "thinking" or "processing" indicator while waiting for the API response.

### **Epic 4: Reasoning Path Visualization & Contextual Querying**

**Epic Goal:** To provide full transparency into the AI's reasoning process and give users advanced control over the query context. This epic will implement the dynamic reasoning path visualization and the ability to constrain the Gentoo KGBot to a specific subgraph, solidifying Grape's position as a reliable and verifiable knowledge tool.

#### **Story 4.1: Subgraph Selection for Context**

**As a** user,
**I want** to select a specific part of the graph,
**so that** I can constrain the Gentoo KGBot to answer questions using only that subset of information.

**Acceptance Criteria:**
1.  The UI provides a tool for selecting multiple nodes and links (e.g., a lasso or box select tool).
2.  Once a selection is made, a "Set as Context" button becomes active.
3.  Clicking "Set as Context" highlights the selected subgraph and visually distinguishes it from the rest of the graph.
4.  Subsequent queries to the `/graph/{graph_id}/query-agent` endpoint now include an array of the selected node/link IDs to define the context.
5.  The backend service modifies its SPARQL query generation to only consider the provided subgraph.

#### **Story 4.2: Real-time Reasoning Path Visualization**

**As a** user,
**I want** to see the agent's reasoning path visualized on a graph in real-time as it answers my question,
**so that** I can understand exactly how the AI arrived at its conclusion.

**Acceptance Criteria:**
1.  The Reasoning Panel, which was previously a placeholder, is now an active graph visualization canvas.
2.  The raw data/nodes returned from the `/graph/{graph_id}/query-agent` endpoint are used to populate this graph.
3.  The visualization should be dynamic: nodes and links appear on the reasoning graph sequentially, illustrating the "path" of logic.
4.  The final reasoning graph is a subgraph of the main knowledge graph, containing only the elements used to formulate the answer.
5.  The nodes and links in the reasoning graph are interactive (e.g., clickable to see details), mirroring the behavior of the main graph.

#### **Story 4.3: Highlighting and Cross-Interaction**

**As a** user,
**I want** the elements of the reasoning path to be highlighted in the main knowledge graph,
**so that** I can see the agent's path in the context of my entire knowledge base.

**Acceptance Criteria:**
1.  As the reasoning path is generated, the corresponding nodes and links in the main knowledge graph are simultaneously highlighted.
2.  Hovering over a node in the reasoning path graph also highlights the corresponding node in the main graph, and vice-versa.
3.  Clicking a node in the reasoning path selects it and displays its details in the main inspector panel.
4.  The highlighting provides a clear visual connection between the agent's answer, its reasoning, and the source knowledge.

### **Epic 5: GCP Deployment & Operational Readiness**

**Epic Goal:** To deploy the Grape application to the Google Cloud Platform, establishing a scalable, secure, and maintainable production environment. This epic covers the creation of infrastructure as code, the setup of a CI/CD pipeline for automated deployments, and the implementation of essential monitoring and logging.

#### **Story 5.1: Infrastructure as Code (IaC) for GCP**

**As a** developer,
**I want** the entire GCP infrastructure to be defined as code (e.g., using Terraform or Google Cloud Deployment Manager),
**so that** I can create, update, and replicate the production environment reliably and consistently.

**Acceptance Criteria:**
1.  IaC scripts are created to provision all required GCP resources (e.g., Cloud Run services, Firebase Hosting, Neo4j Aura instance, IAM roles).
2.  The infrastructure is configured with separate environments for development, staging, and production.
3.  The IaC scripts include configurations for networking (VPC, firewall rules) and security (service account permissions).
4.  Secrets and sensitive configuration (API keys, database credentials) are managed securely (e.g., using Google Secret Manager) and are not hardcoded.

#### **Story 5.2: CI/CD Pipeline for Automated Deployments**

**As a** developer,
**I want** a continuous integration and deployment (CI/CD) pipeline,
**so that** code changes are automatically tested and deployed to the appropriate GCP environment.

**Acceptance Criteria:**
1.  A CI/CD pipeline is configured using a tool like Google Cloud Build or GitHub Actions.
2.  On every commit to the main branch, the pipeline automatically runs linters, unit tests, and integration tests for both the frontend and backend.
3.  A successful build and test run on a release branch triggers an automatic deployment to the staging environment.
4.  A manual approval step is required to promote a build from staging to the production environment.
5.  The pipeline builds and pushes container images for the FastAPI backend to Google Artifact Registry.

#### **Story 5.3: Production Monitoring and Logging**

**As a** developer,
**I want** centralized logging and performance monitoring for the production application,
**so that** I can proactively identify issues, debug errors, and understand system performance.

**Acceptance Criteria:**
1.  The FastAPI backend is configured to send structured logs to Google Cloud Logging (Logging).
2.  The Next.js frontend is configured to report errors and performance metrics to a monitoring service (e.g., using Google Cloud Monitoring or a third-party tool).
3.  Key performance indicators (KPIs) such as API latency, error rates, and resource utilization are tracked in Google Cloud Monitoring dashboards.
4.  Alerts are configured in Google Cloud Monitoring to notify the team of critical issues (e.g., a spike in 5xx server errors, high CPU utilization).
