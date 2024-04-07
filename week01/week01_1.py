import networkx as nx
import matplotlib.pyplot as plt

"""
1. 初始化图
2. 添加节点、边
3. 打印所有节点和边
4. 可视化
"""

# 1. 初始化一个图对象
G = nx.Graph()


# 2. 添加节点、边
# 2.1 往图里添加节点
G.add_node(1)
G.add_node(2)
G.add_node("A")

# 2.2 往图里添加边
G.add_edge(1, 2)
G.add_edge(1, "A")
# 2.2.1 无节点直接添加边，快速建图
G.add_edge(1, "B")
# 2.2.2 G.add_edges_from() 从列表中建边
edges = [
        (1, 3),
        ("A", "B")
        ]
G.add_edges_from(edges)


# 3. 打印所有节点和边
print(G.nodes())    # 打印节点
print(G.edges())    # 打印边


# 4. 可视化
fig1, ax1 = plt.subplots(figsize=(5, 5))  # figsize 该参数用来调整图形宽高

'''
parameters:
G   要绘制的图
ax  要绘制的轴
with_labels     是否可视化图中元素的标签名
labels = ({1:"1!", 2:"2!", "A":"A!"})      设置元素的标签名
'''
nx.draw(G,
        ax=ax1,
        with_labels=True,
        )
plt.show()
