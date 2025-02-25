# 🐄 Building a Knowledge Graph from Unstructured Dairy Science Texts

Welcome to this repository! This project demonstrates how to build a **knowledge graph** from unstructured text data — specifically, publicly available **Journal of Dairy Science** papers.

## 🚀 Pipeline Overview

The workflow consists of the following steps:
<div style="text-align: center;">
  <img src="https://github.com/EnhongLiu/BoAI_Talk/blob/8786c3728844ccc4a8b9fa9ce13675ce10321704/z_pics/Overall%20Flow.png" width="700" height="auto" alt="Bovi-Talk Workflow">
</div>  

### 1. Preprocessing
- Cleaning text data
- Chunking into manageable sections
- Tagging with metadata and assigning UUIDs for tracking
- [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/tree/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/1_Preprocessing)

### 2. Node and Edge Extraction
- Using **LLM** to identify entities (nodes) and their relationships (edges). `LLaMA 70B` was used in this project but you can choose any LLM fitting your machine.
- [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/tree/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/2_Nodes%26Edges_Extraction)

### 3. Graph Data Storage
- Storing graph data in **CSV format** for simplicity (avoiding complex stacks like Neo4j to keep the stack minimal and focus on core concepts, ensuring this project remains easy to run and extend without complicated dependencies.)
- [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/tree/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/3_Graph_Data_Storage%26Ingestion)

### 4. Community Detection
- Applying the **Leiden algorithm** to identify clusters or communities within the graph
- [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/blob/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/4_Community_Building/community_building.py)

### 5. Visualization
- Inspired by the **Microsoft GraphRAG** project, allowing clear graph structure representation
- [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/blob/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/4_Community_Building/visualization.py)

## 🧠 Filter Knowledge Graph via Query

Beyond basic graph construction, this project adds an **interactive query feature** — enabling users to "talk" to the knowledge graph and retrieve related sub-graphs.

### Example Query
> **What feed additives can be used to reduce methane emissions?**

### How it Works
1. **Node Embedding:** Nodes are embedded with edge information. [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/blob/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/5_Sub_Community_Via_Semantic_Filtering/semantic_filtering_nodes.py)
2. **Semantic Filtering:** Cosine similarity filters nodes semantically close to the query. [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/blob/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/5_Sub_Community_Via_Semantic_Filtering/semantic_filtering_nodes.py)
3. **Retrieval:** The system retrieves the top 100 related nodes along with their edges and communities. [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/blob/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/5_Sub_Community_Via_Semantic_Filtering/sub_community.py)
4. **Sub-Graph Extraction:** Outputs the relevant sub-graph for visualization and further analysis. [Example Code](https://github.com/EnhongLiu/Build_Knowledge_Graphs_From_Unstructured_Data_With_Semantic_Filtering/blob/f5f7c10ad96147bd51cc490bd0d360cf47c19fe9/5_Sub_Community_Via_Semantic_Filtering/sub_community.py)

## 🎯 Sample Output

- **Graph nodes and edges, along with metadata:** Stored in `./data/graph_nodes.csv`
- **Community detection results:** `./results/communities.csv`
- **Knowledge graph output:**
<div style="text-align: center;">
  <img src="https://github.com/EnhongLiu/BoAI_Talk/blob/8786c3728844ccc4a8b9fa9ce13675ce10321704/z_pics/Overall%20Flow.png" width="700" height="auto" alt="Bovi-Talk Workflow">
</div> 
- **Subgraph output after query filtering:**  
<div style="text-align: center;">
  <img src="https://github.com/EnhongLiu/BoAI_Talk/blob/8786c3728844ccc4a8b9fa9ce13675ce10321704/z_pics/Overall%20Flow.png" width="700" height="auto" alt="Bovi-Talk Workflow">
</div> 

---
