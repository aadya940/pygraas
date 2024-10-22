import subprocess
import pydot
import networkx as nx
import matplotlib.pyplot as plt
import os
import shutil

from ._cloner import _clone_package

from pydeps.pydeps import pydeps
from pydeps import cli


class DependencyGraph:
    """Build a NetworkX Dependency Graph."""

    def __init__(self, package_name, package_url):
        self.package_name = package_name
        self.dot_file = f"{self.package_name}_deps.dot"
        self.graph = None
        self.package_url = package_url

        _clone = _clone_package(self.package_name, self.package_url)

        if self.package_name not in os.listdir("."):
            raise ValueError("Failed to clone.")

    def build_graph(self, max_bacon=2):
        _is_file = self._generate_dot_file(max_bacon=max_bacon)
        if _is_file:
            self._build_networkx_graph()
        self._cleanup_dir()
        return self.graph

    def _generate_dot_file(self, max_bacon, skip_private=False):
        """Generates the DOT file using pydeps."""
        _args = [
            "-vv",
            f"--max-bacon={max_bacon}",
            "--cluster",
            f"--dot-output={self.dot_file}",
            "--show-dot",
            self.package_name,
        ]

        if skip_private:
            _args.insert(-2, "-x _*")

        result = pydeps(**cli.parse_args(args))
        return True

    def _build_networkx_graph(self):
        """Reads the DOT file and builds a networkx graph."""
        graphs = pydot.graph_from_dot_file(self.dot_file)
        dot_graph = graphs[0]  # Assuming a single graph in the file

        # Convert pydot graph to networkx graph
        self.graph = nx.drawing.nx_pydot.from_pydot(dot_graph)
        print(
            f"Graph built with {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges."
        )

    def visualize_graph(self):
        """Visualizes the networkx graph using matplotlib."""
        if self.graph is None:
            raise ValueError("Graph is not built yet. Call `build_graph` first.")

        pos = nx.spring_layout(self.graph)
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=3000,
            font_size=10,
            font_weight="bold",
        )

        plt.show()

    def get_nodes(self):
        """Returns the list of nodes (packages) in the graph."""
        if self.graph is None:
            raise ValueError("Graph is not built yet. Call `build_graph` first.")

        return list(self.graph.nodes())

    def get_edges(self):
        """Returns the list of edges (dependencies) in the graph."""
        if self.graph is None:
            raise ValueError("Graph is not built yet. Call `build_graph` first.")

        return list(self.graph.edges())

    def _cleanup_dir(self):
        if self.package_name in os.listdir("."):
            shutil.rmtree(self.package_name)
