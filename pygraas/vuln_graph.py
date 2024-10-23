import networkx as nx
import matplotlib.pyplot as plt
import json
from .depgraph import DependencyGraph

with open("pygraas/insecure_full.json", "r") as _f:
    INSECURE_FULL = json.loads(_f.read())


class VulnerabilityGraph:
    def __init__(self, graph: DependencyGraph):
        self.graph = graph

    def build_vulnerability_graph(self):
        _nodes = self.graph.get_nodes()

        for node in _nodes:
            for vul_package in INSECURE_FULL.keys():
                if vul_package.lower() in node.lower():  # Case-insensitive comparison
                    vulnerabilities = INSECURE_FULL[vul_package]

                    # Check if vulnerabilities is a single dict or a list of dicts
                    if isinstance(vulnerabilities, dict):
                        vulnerabilities = [
                            vulnerabilities
                        ]  # Wrap single dict in a list

                    elif not isinstance(vulnerabilities, list):
                        continue  # If it's neither, skip to next package

                    for vuln in vulnerabilities:
                        # Ensure the vuln is a dictionary and contains the required keys
                        if isinstance(vuln, dict) and "cve" in vuln and "v" in vuln:
                            self._set_vulnerable(
                                node, vuln["cve"], vuln["v"]
                            )  # Set vulnerability

        return self.graph

    def _set_vulnerable(self, package_name: str, cve: str, version: str):
        if package_name in self.graph.graph.nodes:
            self.graph.graph.nodes[package_name]["is_vulnerable"].append(True)
            self.graph.graph.nodes[package_name]["CVE"].append(cve)
            self.graph.graph.nodes[package_name]["version"].append(version)

            if not self.graph.graph.nodes[package_name]["color"] != "red":
                self.graph.graph.nodes[package_name]["color"] = "red"

    def visualize_graph(self):
        node_colors = [
            self.graph.graph.nodes[node]["color"] for node in self.graph.graph.nodes
        ]
        nx.draw(
            self.graph.graph,
            with_labels=True,
            node_color=node_colors,
            font_weight="bold",
        )
        plt.show()
