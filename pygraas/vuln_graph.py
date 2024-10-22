import networkx as nx
import matplotlib.pyplot as plt


class VulnerabilityGraph:
    def __init__(self, graph):
        self.graph = graph

    def build_vulnerability_graph(self):
        pass

    def _mark_vulnerables(self):
        pass

    def _set_vulnerable(self, package_name: str, cve: str):
        self.graph[package_name]["is_vulnerable"] = True
        self.graph[package_name]["cve"] = cve
        self.graph[package_name]["color"] = "red"

    def visualize_graph(self):
        node_colors = [self.graph.nodes[node]["color"] for node in self.graph.nodes]
        nx.draw(
            self.graph, with_labels=True, node_color=node_colors, font_weight="bold"
        )
        plt.show()
