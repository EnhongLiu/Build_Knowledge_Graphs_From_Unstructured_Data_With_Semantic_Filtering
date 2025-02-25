import seaborn as sns
import random
from pyvis.network import Network
from IPython.display import display, HTML

# Create a mapping from node to community, from the Leiden community clustering
node_to_community = {}
for i, community in enumerate(partition):
    for node in community:
        node_to_community[ig_graph.vs[node]['name']] = i


# Get the nodes from semantic search
matched_nodes = [node for node, score in top_nodes]

# Find the communities containing those nodes
matched_communities = {node_to_community[node] for node in matched_nodes if node in node_to_community}

# Extract all nodes in the matched communities, sorted
communities_with_nodes = [
    sorted([node for node, comm in node_to_community.items() if comm == community_id])
    for community_id in matched_communities
]

print("Total communities:", len(communities_with_nodes))

palette = "hls"

## Now add these colors to communities and make another dataframe
def colors2Community(communities) -> pd.DataFrame:
    ## Define a color palette
    p = sns.color_palette(palette, len(communities)).as_hex()
    random.shuffle(p)
    rows = []
    group = 0
    for community in communities:
        color = p.pop()
        group += 1
        for node in community:
            rows += [{"node": node, "color": color, "group": group}]
    df_colors = pd.DataFrame(rows)
    return df_colors


colors = colors2Community(communities_with_nodes)


for index, row in colors.iterrows():
    G.nodes[row['node']]['group'] = row['group']
    G.nodes[row['node']]['color'] = row['color']
    G.nodes[row['node']]['size'] = G.degree[row['node']]

graph_output_directory = "/Workspace/Users/el839@cornell.edu/3_OntologyLLM/Data/Results/index_test_100_filtered_topic.html"

net = Network(
    notebook=False,
    cdn_resources="remote",
    height="900px",
    width="100%",
    select_menu=True,
    filter_menu=False,
)

net.from_nx(G)
net.force_atlas_2based(central_gravity=0.015, gravity=-31)
net.show(graph_output_directory, notebook=False)

display(HTML(graph_output_directory))
