# 🐄 Building a Knowledge Graph from Unstructured Dairy Science Texts

Welcome to this repository! This project demonstrates how to build a **knowledge graph** from unstructured text data — specifically, publicly available **Journal of Dairy Science** papers.

## 🚀 Pipeline Overview

The workflow consists of the following steps:

### 1. Preprocessing
- Cleaning text data
- Chunking into manageable sections
- Tagging with metadata and assigning UUIDs for tracking

### 2. Node and Edge Extraction
- Using **LLM (`LLaMA 70B` was used in this project but you can choose any LLM fitting your machine)** to identify entities (nodes) and their relationships (edges)

### 3. Graph Data Storage
- Storing graph data in **CSV format** for simplicity (avoiding complex stacks like Neo4j to keep the stack minimal and focus on core concepts, ensuring this project remains easy to run and extend without complicated dependencies.)

### 4. Community Detection
- Applying the **Leiden algorithm** to identify clusters or communities within the graph

### 5. Visualization
- Inspired by the **Microsoft GraphRAG** project, allowing clear graph structure representation

## 🧠 Filter Knowledge Graph via Query

Beyond basic graph construction, this project adds an **interactive query feature** — enabling users to "talk" to the knowledge graph and retrieve related sub-graphs.

### Example Query
> **What feed additives can be used to reduce methane emissions?**

### How it Works
1. **Node Embedding:** Nodes are embedded with edge information.
2. **Semantic Filtering:** Cosine similarity filters nodes semantically close to the query.
3. **Retrieval:** The system retrieves the top 100 related nodes along with their edges and communities.
4. **Sub-Graph Extraction:** Outputs the relevant sub-graph for visualization and further analysis.

## 🎯 Sample Output

- **Graph data (CSV):** Stored in `./data/graph_nodes.csv` and `./data/graph_edges.csv`
- **Community detection results:** `./results/communities.csv`
- **Query output:** Relevant sub-graphs saved in `./results/sub_graph.csv`

---
