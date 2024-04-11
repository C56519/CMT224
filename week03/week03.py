import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import operator
import json
from scipy import stats

# 1 加载数据集
data = []
with open("./week03/reddit-2016-sample-1.json") as json_file:
    data = json.load(json_file)
# 打印数据集长度
print(f"Number of posts: {len(data)}")
# 打印前五个
for post in data[:5]:
    print(post)

# 2 创建图对象(有向图)
G = nx.DiGraph()
# 直接添加边，自动把节点也添加了
for post in data:
    G.add_edge(post["SOURCE"], post["TARGET"])
# 打印数量
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
print(f"Number of posts: {len(data)}")

# 3 密度
print(f"Density (or sparsity): {nx.density(G):.5f}") #note, nx.density(G) not G.density()
degree_sequence = [degree for (node, degree) in nx.degree(G)]
print("Descriptive Statistics:\n")
print(f"Mean degree: {np.mean(degree_sequence):.2f}")
print(f"Std. deviation: {np.std(degree_sequence):.2f}")
print(f"Range: {np.amin(degree_sequence)} to {np.amax(degree_sequence)}")
print(f"Median degree: {np.median(degree_sequence)}")
# 按度排列
reverse_sorted_degree_sequence = sorted(degree_sequence, reverse=True)
print(reverse_sorted_degree_sequence[:20])
print(reverse_sorted_degree_sequence[-20:])

# 小世界网络：社交网络符合小世界网络，任意两个节点最短路径长度相对较短，而形成紧密的群集，具有较高的平均聚类系数
# 4 平均聚类系数
print(f"Average clustering coefficient in the network: {nx.average_clustering(G):.3f}")

# 5 连通性 连通组件
# 5.1 判断图的连通性
strongly_connected = nx.is_strongly_connected(G)    # 全图是否是强连通
weakly_connected = nx.is_weakly_connected(G)        # 全图是否是弱连通
print(f"Is the entire network strongly connected: {strongly_connected}")
print(f"Is the entire network weakly connected: {weakly_connected}")
# 5.2 计算图的强连通、弱连通分量
number_scc_components = nx.number_strongly_connected_components(G)
number_wcc_components = nx.number_weakly_connected_components(G)
print(f"Number of strongly connected components: {number_scc_components}")
print(f"Number of weakly connected components: {number_wcc_components}")
# 5.3 计算每个强连通分量有多少个节点？
# 创建所有强连通分量列表
scc_components = nx.strongly_connected_components(G)
# 创建所有强连通分量节点列表
number_of_nodes_per_strongly_connected_component = []
# 计算每个强连通分量节点个数
for component in scc_components:
    number_of_nodes_per_strongly_connected_component.append(len(component))
# 排序
number_of_nodes_per_strongly_connected_component = sorted(number_of_nodes_per_strongly_connected_component, reverse=True)
print("Number of nodes in the 100 largest strongly connected components:\n")
print(number_of_nodes_per_strongly_connected_component[:100], "...")

# 5.4 计算每个弱连接组件有多少个节点？
# 省略写法
number_of_nodes_per_weakly_connected_component = sorted([len(wcc) for wcc in nx.weakly_connected_components(G)], reverse=True)
print("\nNumber of nodes in the 100 largest weakly connected components:\n")
print(number_of_nodes_per_weakly_connected_component[:100], "...\n\n")

# 5.5
# 这里直接结果表明：存在一个超大的强连通组件，节点数多达 1630 个，所以我们可以继续分析这个子网络
# (1) 实例化所有强连通组件，返回一个列表
strongly_connected_components = nx.strongly_connected_components(G)
# (2) 按照len也就是节点数来排列
strongly_connected_components_sorted_by_number_of_nodes = sorted(
    strongly_connected_components, 
    key=len,
    reverse=True # 反顺序，就是从大到小排列
)
# (3) 取最多节点的强连通组件
list_of_nodes_in_largest_strongly_connected_component = strongly_connected_components_sorted_by_number_of_nodes[0]
# (4) 利用最大的强连通组件创建子图
LSCC = G.subgraph(list_of_nodes_in_largest_strongly_connected_component).copy()
# (5) 对比子图和整个图的信息
# 子图和全部图的节点数
print(f"Number of nodes in G: {G.number_of_nodes()}")
print(f"Number of nodes in the largest strongly connected component of G: {LSCC.number_of_nodes()}")
# 子图和全部图的边数
print(f"Number of edges in G: {G.number_of_edges()}")
print(f"Number of edges in the largest strongly connected component of G: {LSCC.number_of_edges()}")
# 单独查看子图的 最短路径长度 和 平均聚类系数
print(f"Average shortest path length in G's largest strongly connected component: {nx.average_shortest_path_length(LSCC):.2f}")
print(f"Average clustering coefficient in G's largest strongly connected component: {nx.average_clustering(LSCC):.2f}")

# (6) 判断该子图是否支持“小世界”属性
# 首先生成随机网络，规格与子图节点数、边数相同
R = nx.gnm_random_graph(LSCC.number_of_nodes(), LSCC.number_of_edges(), seed=100, directed=True)
# 在随机网络中，生成强连通组件列表并按照节点数量排序，且取大的那个
R_LSCC_nodes = sorted(nx.strongly_connected_components(R), key=len, reverse=True)[0]
# 在具有最多节点数的强连通组件下，生成子网
R_LSCC = R.subgraph(R_LSCC_nodes).copy()
# 单独查看子图的 最短路径长度 和 平均聚类系数
print(f"Average shortest path length in a random network: {nx.average_shortest_path_length(R_LSCC):.3f}")
print(f"Average clustering coefficient in a random network: {nx.average_clustering(R_LSCC):.3f}")
# 将随机网络结果与(5)中子图的结果对比
# 平均聚类系数高于随机图，平均最短路径长度与随即网络相似，说明(5)中子图部分支持“小世界”属性


# 6 互惠性
# 在社会网络分析中，互惠性（Reciprocity）是衡量有向网络中边互相指向的程度的指标。
# 在社会心理学中，互惠原则是指对一个积极行动以另一个积极行动回应，以此奖励善意行为的社会规范，对于负面行动也同样适用，例如报复行为或者针锋相对的策略。
# 在有向图或网络中，如果一个节点 A 指向另一个节点 B，当节点 B 以相同的方式回应，即 B 也指向 A 时，我们称这两个节点之间存在互惠的关系。
# 在网络层面，互惠性为网络中互惠边占总边数的比例。这个比例越高，表明网络中的互惠关系越普遍。
# 在社交网络中，互惠性可能指的是相互关注的用户；在经济交易网络中，互惠性可能体现在双方互相进行商品或服务交换。

# 6.1 图的整体互惠性密度
print(f"Overall Reciprocity of G: {nx.overall_reciprocity(G):.3f}")
print(f"Density of G : {nx.density(G):.5f}")
# 子图的整体互惠性和密度
print(f"Overall Reciprocity of G's largest strongly connected component: {nx.overall_reciprocity(LSCC):.2f}")
print(f"Density of G's largest strongly connected component : {nx.density(LSCC):.4f}")

# 6.2 计算每个节点的互惠性
reciprocity_per_node = nx.reciprocity(G, G.nodes())     # 参数是一个图，一个图的节点列表，返回一个字典：节点和对应的互惠性
print("\nIndividual Reciprocity for 5 example nodes in G (id, reciprocity):")
print(list(reciprocity_per_node.items())[:5])
# 将上述字典的所有值(互惠性)提出来生成一个列表
reciprocity_values = list(reciprocity_per_node.values())
# 描述性统计：所有节点的平均互惠性、标准差、范围(最大最小值)、互惠性中位数
print("\nDescriptive Statistics:\n")
print(f"Mean reciprocity: {np.mean(reciprocity_values):.2f}")
print(f"Std. deviation: {np.std(reciprocity_values):.2f}")
print(f"Range: {np.amin(reciprocity_values)} to {np.amax(reciprocity_values)}")
print(f"Median reciprocity: {np.median(reciprocity_values)}")

# 通过互惠性，我们可以进一步研究
# 7 度
# 7.1 度、入度、出度
# 创建节点顺序列表，一般是id顺序
nodeOrder = list(G.nodes())
# 计算所有节点的度(入度+出度)
degree_per_node = G.degree(nodeOrder)
print("\nDegree for 6 example nodes in G (id, in+out degree):") 
print(list(degree_per_node)[:6])    # 形式是：节点id: 度 ('6241', 18)
# 计算所有节点的入度和出度
in_degree_per_node = G.in_degree(nodeOrder)
print("\nIn degree for 6 example nodes in G (id, in degree):") 
print(list(in_degree_per_node)[:6])
out_degree_per_node = G.out_degree(nodeOrder)
print("\nOut degree for 6 example nodes in G (id, out degree):") 
print(list(out_degree_per_node)[:6])

# 7.2 通过度来找出网络中那些只出不进、只进不出的节点
only_referenced_by_others = []      # 只进不出列表
never_referenced_by_others = []     # 只出不进列表
mix = []
no_edges = []
# 对于网络中的每一个节点
for node in nodeOrder:
    # 计算其入度和出度
    in_degree = G.in_degree(node)
    out_degree = G.out_degree(node)
    
    # 是否只进不出
    if in_degree > 0 and out_degree == 0:
        only_referenced_by_others.append(node)
    # 是否只出不进
    elif in_degree == 0 and out_degree > 0:
        never_referenced_by_others.append(node)
    # 是否有进有出
    elif in_degree > 0 and out_degree > 0:
        mix.append(node)
    # 该节点没有边
    else:
        no_edges.append(node)

print(f"Total number of communities (nodes): {len(nodeOrder)}")     # 所有节点数
print()
print(f"Number that are only referenced by others (only 'target' nodes): {len(only_referenced_by_others)}")     # 只进不出的节点数
print(f"Number that are never referenced (i.e., only reference others / only 'source' nodes): {len(never_referenced_by_others)}") # 只出不进的节点数
print(f"Number that reference others and are referenced by others: {len(mix)}") # 有进有出的节点数
print(f"Number that have no edges : {len(no_edges)}")   # 没有边的节点数


# 7.3 度绘图，直观化度数分布
# 度的序列
degree_sequence = sorted(dict(G.degree(nodeOrder)).values(), reverse=True)  # in+out degree
in_degree_sequence = sorted(dict(G.in_degree(nodeOrder)).values(), reverse=True)
out_degree_sequence = sorted(dict(G.out_degree(nodeOrder)).values(), reverse=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
# 度数-排名图
ax1.plot(degree_sequence, "r-", marker=".", label="in+out")
ax1.plot(in_degree_sequence, "g-", marker=".", label="in")
ax1.plot(out_degree_sequence, "b-", marker=".", label="out")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")
ax1.legend()

# 双对数（Log-Log）图
# 常用于展示节点度数的分布，以便观察是否遵循幂律分布
# 幂律分布的特征是大多数节点有很少的连接，而少数节点（比如枢纽节点）有大量的连接
# 在双对数图中，如果节点度数遵循幂律分布，那么数据点将大致排列在一条直线上
ax2.loglog(degree_sequence, "r-", marker=".", label="in+out")
ax2.loglog(in_degree_sequence, "g-", marker=".", label="in")
ax2.loglog(out_degree_sequence, "b-", marker=".", label="out")
ax2.set_title("loglog")
ax2.set_ylabel("Degree")
ax2.set_xlabel("Rank")
ax2.legend()
plt.show()

# 7.4 度的描述
print("\nIn Degree Descriptive Statistics:\n")
# 入度
print(f"Mean in degree: {np.mean(in_degree_sequence):.2f}")     # 平均度
print(f"Std. deviation: {np.std(in_degree_sequence):.2f}")      # 度的标准差
print(f"Range: {np.amin(in_degree_sequence)} to {np.amax(in_degree_sequence)}") # 度的范围
print(f"Median in degree: {np.median(in_degree_sequence)}")     # 度的中位数
# 出度
print("\nOut Degree Descriptive Statistics:\n")
print(f"Mean in degree: {np.mean(out_degree_sequence):.2f}")
print(f"Std. deviation: {np.std(out_degree_sequence):.2f}")
print(f"Range: {np.amin(out_degree_sequence)} to {np.amax(out_degree_sequence)}")
print(f"Median in degree: {np.median(out_degree_sequence)}")

# 7.5 找重要角色：找网络中最活跃或最有影响力的分子
# 7.5.1 找最大进出度,也就是最活跃的，最有影响力的
# 从大到小排序
sorted_in_degree = sorted(in_degree_per_node, reverse=True, key=operator.itemgetter(1))
sorted_out_degree = sorted(out_degree_per_node, reverse=True, key=operator.itemgetter(1))
# 打印前五个最大的
print("\n5 nodes in G with the largest 'in' degree (id, in degree):")
print(sorted_in_degree[:5])
print("\n5 nodes in G with the largest 'out' degree (id, out degree):")
print(sorted_out_degree[:5])

# 7.5.2 找出前五十，最活跃的，最有影响力的部分
top_in_degree_nodes = set(node[0] for node in sorted_in_degree[:50])    # 找出入度前五十存到集合中
top_out_degree_nodes = set(node[0] for node in sorted_out_degree[:50])  # 找出出度前五十存到集合中
# 从上述两个集合中找交集
nodes_in_both = top_in_degree_nodes.intersection(top_out_degree_nodes)
print(f"Number of communities in both the top(largest) 50 'in' and 'out' degree lists: {len(nodes_in_both)}")

# 8 皮尔逊系数
# 皮尔逊相关系数可以衡量两个数据集之间的线性关系。该相关系数在 -1 和 +1 之间变化，其中 0 表示不相关。
# 如果 r 的值 < 0，则支持负相关
# 如果 r 的值 > 0，则支持正相关
# 如果 r 的值为 0，则不支持相关性
# (+/-) 0.2 至 0.3 范围内的值表示相关性较弱
# (+/-) 0.4 至 0.5 范围内的值表示中等相关性
# (+/-) 0.6 至 0.7 范围内的值表示强相关性
# (+/-) 0.8 至 1.0 范围内的值表明相关性非常强

# (1)提取入度出度序列的值
in_degree_sequence = list(dict(G.in_degree(nodeOrder)).values())
out_degree_sequence = list(dict(G.out_degree(nodeOrder)).values())
# 求皮尔逊系数
r, p = stats.pearsonr(in_degree_sequence, out_degree_sequence)
print(f"pearson r: {r:.3f}, {p:.3f}")

# 9 加权有向网络
# 为了避免重复的边，比如A评论B了多次，我们就没必要每一次建立一个边，只需要用边的权重来表示
W = nx.DiGraph()
for post in data:
    # 如果该边存在，权重加一
    if W.has_edge(post["SOURCE"], post["TARGET"]):
        W[post["SOURCE"]][post["TARGET"]]['weight'] += 1
    # 如果边不存在，添加边，初始化权重为1
    else:
        W.add_edge(post["SOURCE"], post["TARGET"], weight=1)

print(f"Number of nodes: {W.number_of_nodes()}")
print(f"Number of edges: {W.number_of_edges()}")
print(f"Total of edge weights: {W.size(weight='weight')} (Number of posts)")

# 9.1 节点强度：该节点可能有多个边，各个边上的权重综合称为节点强度。使用度数的一个参数来获取 weight="weight"
# 建立节点强度序列：整体、入、出
strength_sequence = sorted(dict(W.degree(nodeOrder, weight="weight")).values(), reverse=True)
in_strength_sequence = sorted(dict(W.in_degree(nodeOrder, weight="weight")).values(), reverse=True)
out_strength_sequence = sorted(dict(W.out_degree(nodeOrder, weight="weight")).values(), reverse=True)

# 画图，描述节点强度
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.plot(strength_sequence, "r-", marker=".", label="in+out")
ax1.plot(in_strength_sequence, "g-", marker=".", label="in")
ax1.plot(out_strength_sequence, "b-", marker=".", label="out")
ax1.set_title("Strength Rank Plot")
ax1.set_ylabel("Strength")
ax1.set_xlabel("Rank")
ax1.legend()

ax2.loglog(strength_sequence, "r-", marker=".", label="in+out")
ax2.loglog(in_strength_sequence, "g-", marker=".", label="in")
ax2.loglog(out_strength_sequence, "b-", marker=".", label="out")
ax2.set_title("loglog")
ax2.set_ylabel("Strength")
ax2.set_xlabel("Rank")
ax2.legend()
plt.show()

# 节点强度：平均、标准差、最小最大值、中位数
print("\nIn Strength Descriptive Statistics:\n")
print("Mean in strength: %.2f" % np.mean(in_strength_sequence))
print("Std. Deviation: %.2f \n" % np.std(in_strength_sequence))
print("Smallest in strength: %d" % np.amin(in_strength_sequence))
print("Largest in strength: %d \n" % np.amax(in_strength_sequence))
print("Median in strength: %.d\n\n" % np.median(in_strength_sequence))

print("\nOut Strength Descriptive Statistics:\n")
print("Mean out strength: %.2f" % np.mean(out_strength_sequence))
print("Std. Deviation: %.2f\n" % np.std(out_strength_sequence))
print("Smallest out strength: %d" % np.amin(out_strength_sequence))
print("Largest out strength: %d\n" % np.amax(out_strength_sequence))
print("Median out strength: %.d\n" % np.median(out_strength_sequence))