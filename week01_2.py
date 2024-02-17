import networkx as nx
import matplotlib.pyplot as plt

# 设置节点属性
# 在networkx中，可以编辑节点和边的属性，这里是节点属性

G = nx.Graph()

# G.add_edges_from() 从列表中建边
edges = [
    (1, 3),
    (1, 2),
    (2, 3),
    (3, 4)
]
G.add_edges_from(edges)


# 1 设置节点属性 color
# 每个节点都是一个字典，我们任意设一个key为"group"，值为red / blue
G.nodes[1]["group"] = "red"
G.nodes[2]["group"] = "blue"
G.nodes[3]["group"] = "blue"
G.nodes[4]["group"] = "blue"
print(G.nodes(data=True))
# nx.get_node_attributes()获取指定属性，返回一个字典
node_colors = nx.get_node_attributes(G, name='group')
node_color_list = list(node_colors.values())

# 2 按照属性查找节点
blue_nodes = []
for node, attributes in G.nodes(data=True):
    if attributes['group'] == 'blue':
        blue_nodes.append(node)
print(blue_nodes)

# 3. 配置节点属性
fig1, ax1 = plt.subplots(figsize=(5, 5))
nx.draw(G,
        ax=ax1,
        with_labels=True,
        node_color=node_color_list # 绘制节点属性 color
        )
plt.show()