from pygraas import DependencyGraph

g = DependencyGraph("chainopy", "https://github.com/aadya940/chainopy")
g.build_graph()
g.visualize_graph()
nodes = g.get_nodes()
print(nodes)
