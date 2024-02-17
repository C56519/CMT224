import networkx as nx
import matplotlib.pyplot as plt


# 边缘属性

G = nx.Graph()

# 添加边时同时设置边缘属性 ’weight‘
G.add_edge(1, 2, weight=5)
G.add_edge(2, 'A', weight=2)

# 打印边列表和边属性列表
g_edges = G.edges()
edge_weight_list = []
for u, v in g_edges:
    edge_weight = G[u][v]['weight']
    edge_weight_list.append(edge_weight)
print(f"List of edges: {g_edges}")
print(f"List of edge weight: {edge_weight_list}")

# 配置边缘属性
fig7, ax7 = plt.subplots()
nx.draw(G,
        ax=ax7,
        with_labels=True,
        edgelist=g_edges,
        width=edge_weight_list
       )
plt.show()