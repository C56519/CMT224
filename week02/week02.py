import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# 1 读文件创建图对象
G = nx.read_edgelist("./week02/twitch_sample.edgelist")
# 画图，先看看图的整体结构
fig1, ax1 = plt.subplots(figsize=(12,12)) # create a new Figure and Axis for plotting 
nx.draw(G, ax=ax1) # use a NetworkX draw function (not matplotlib) to draw the Graph 
plt.show() # show the result

# 2 分析数量
print(f"Number of nodes: {G.number_of_nodes()}")    # 节点数量
print(f"Number of edges: {G.number_of_edges()}")    # 边数量

# 3 分析图的密度or稀疏性Density (or sparsity) 值为0-1之间
# 在一个完全连接的网络中，每一对节点之间都存在一条边，这样的网络密度为1或100%。相反，如果网络中没有任何边，那么网络的密度为0。
print(f"Density (or sparsity): {nx.density(G):.3f}")

# 4 分析图的度degree
# 在网络或图中，一个节点的"度"（Degree）指的是与该节点直接相连的边的数量
# 方法一：直接输出每个节点对应的度
print(nx.degree(G))     # 计算图中所有节点的度
# 方法二：先生成节点度序列，再输出所有度
degree_sequence = [d for (n, d) in nx.degree(G)] # Compressed version of the above
print(degree_sequence)
# 方法三：计算平均度、度的标准偏差
print(f"Descriptive Statistics:\n")
print(f"Mean degree: {np.mean(degree_sequence):.2f}")
print(f"Std. Deviation: {np.std(degree_sequence):.2f}")

# 5 度的可视化
# (1) 排序度序列
degree_sequence = sorted(degree_sequence, reverse=True)
# (2) 画图
# 5.1 排名图：按照度数从大到小（或从小到大）排序
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 12))
ax1.plot(degree_sequence, color="r", marker=".")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank (of each node)")
# 5.2 度的直方图：统计具有相同度数的节点数量
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree Histogram Plot")
ax2.set_xlabel("Degree")
ax2.set_ylabel("Number of nodes")
plt.show()

# 6 路径
# 路径是从一个节点到另一个节点的一系列边的序列，它代表了节点之间的“距离”。这种距离可以用于模拟和测量网络中的（假设的）信息流动。
# 性质：1. 两个节点之间可能存在多个路径，可能长度不同 2. 专注于简单路径(一条路径中，每个节点只能出现一次)，专注于最短路径
# 6.1 找出所有最短路径
# (1) 首先确定两个节点
some_node_id = "3181"
some_other_node_id = "24321"
# (2) 找出该两个节点的所有存在的最短路径
shortest_paths = nx.all_shortest_paths( 
    G,
    some_node_id,
    some_other_node_id)
print(f"Shortest paths from {some_node_id} to {some_other_node_id}:")
for path in shortest_paths:
 print(f" --> ".join(path))
# 6.2 输出最短路径长度
some_shortest_path_length = nx.shortest_path_length(G, some_node_id, some_other_node_id)
print(f"Shortest path length from {some_node_id} to {some_other_node_id} is {some_shortest_path_length}")
# 6.3 图中所有点所有路径的平均距离
print(f"Average shortest path length in the network: {nx.average_shortest_path_length}")

# 7 偏心率 Eccentricity
# 该节点到网络中所有其他节点的最大距离。具体来说，对于网络中的一个节点 v，其偏心率定义为从 v 到所有其他节点的最短路径中的最大距离。
# 偏心率提供了一个衡量节点在网络中相对边缘化程度的指标
# 一个偏心率高的节点意味着它至少与网络中的一个节点相距较远，而偏心率低的节点则表示它与网络中的所有其他节点都相对较近且在网络中的位置更为中心
# (1) 输出所有节点的偏心率
print(nx.eccentricity(G, v=some_node_id))
print(nx.eccentricity(G))
# (2) 构建偏心率序列
eccentricity_sequence = list(nx.eccentricity(G).values())
# (3) 计算整体偏心率
# 所有节点之间的最大分离度，所有节点之间的最小分离度，平均分离度，所有节点间的中位数分离度
print(f"Maximum degree of separation across all nodes (as path length): {np.amax(eccentricity_sequence)}")
print(f"Minimum degree of separation across all nodes (as path length): {np.amin(eccentricity_sequence)}")
print(f"Average degree of separation (as path length): {np.mean(eccentricity_sequence)}")
print(f"Median degree of separation across all nodes (as path length): {np.median(eccentricity_sequence)}")