import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# G.add_edges_from() 从列表中建边
edges = [
    (1, 3),
    (1, 2),
    (2, 3),
    (3, 4)
]
G.add_edges_from(edges)

fig1, ax1 = plt.subplots(figsize=(5, 5))
nx.draw(G,
        ax=ax1,
        with_labels=True,
        )
plt.show()