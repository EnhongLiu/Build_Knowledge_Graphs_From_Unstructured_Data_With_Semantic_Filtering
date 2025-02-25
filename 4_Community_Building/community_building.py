import networkx as nx
import pandas as pd
import igraph as ig
import leidenalg

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

# Convert NetworkX graph to igraph for Leiden algorithm
ig_graph = ig.Graph.TupleList(G.edges(data=False), directed=False)

# Apply Leiden algorithm for community detection
partition = leidenalg.find_partition(ig_graph, leidenalg.ModularityVertexPartition)

# Map Leiden communities back to NetworkX graph
for i, community in enumerate(partition):
    for node in community:
        G.nodes[str(ig_graph.vs[node]['name'])]['community'] = i

# Extract and sort communities
communities = [sorted([ig_graph.vs[node]['name'] for node in community]) for community in partition]

# Output number of communities and their members
print("Number of Communities =", len(communities))
print(communities)
