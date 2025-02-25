import networkx as nx
import pandas as pd
from databricks_langchain import DatabricksEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nodes = pd.concat([dfg1['node_1'], dfg1['node_2']], axis=0).unique()

# Create NetworkX graph
G = nx.Graph()

# Add nodes to the graph
for node in nodes:
    G.add_node(str(node))

# Add edges to the graph
for index, row in dfg1.iterrows():
    G.add_edge(
        str(row["node_1"]),
        str(row["node_2"]),
        title=row["edge"],
        weight=row['count']
    )

node_texts = {}

for node in G.nodes:
    # Get all edges for the current node
    edges = G.edges(node, data=True)
    # Collect edge descriptions (e.g., 'title' field or use a placeholder if missing)
    edge_descriptions = [str(data.get('title', '')) for _, _, data in edges]
    # Concatenate all edge descriptions to form the node text
    node_texts[node] = " ".join(edge_descriptions) if edge_descriptions else "No edge info"

# Generate text embeddings using the embed_query method
node_embeddings = {node: db_embeddings.embed_query(text) for node, text in node_texts.items()}


# Function to find top matching nodes for a given query
def search_nodes(query, node_embeddings, top_k=100):
    query_embedding = np.array(db_embeddings.embed_query(query)).reshape(1, -1)
    
    similarities = {
        node: cosine_similarity(query_embedding, np.array(emb).reshape(1, -1))[0][0]
        for node, emb in node_embeddings.items()
    }
    
    # Sort nodes by similarity score
    return sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]


# Test: search for nodes related to an specific question
query = "what feed additives can be used to reduce methane emission"
top_nodes = search_nodes(query, node_embeddings)
