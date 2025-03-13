import subprocess
import pydot
import networkx as nx
import matplotlib.pyplot as plt
import os
import shutil
import sys
import seaborn as sns
from collections import Counter
import threading  # Import threading module

from ._utils import get_package

from pydeps.pydeps import pydeps
from pydeps import cli


class DependencyGraph:
    """Build a NetworkX Dependency Graph."""

    def __init__(self, package_name: str, package_url: str, allow_clone=True):
        """
        Initialize the DependencyGraph.

        Parameters:
        - package_name (str): The name of the package to analyze.
        - package_url (str): The URL of the package repository.
        - allow_clone (bool): Whether to allow cloning the package.
        """
        self.package_name = package_name.lower()
        self.dot_file = f"{self.package_name}_deps.dot"
        self.graph = None
        self.package_url = package_url
        self.max_bacon = None  # Max. Tree Depth

        _get_pkg = get_package(
            package_name=package_name, package_url=package_url, clone=allow_clone
        )

        if self.package_name not in os.listdir("."):
            raise ValueError("Failed to clone.")

    def build_graph(self, max_bacon=2):
        """
        Build the dependency graph.

        Parameters:
        - max_bacon (int): The maximum depth of dependencies to include.

        Returns:
        - Graph: The constructed dependency graph.
        """
        _is_file = self._generate_dot_file(
            max_bacon=max_bacon,
        )
        self.max_bacon = max_bacon
        if _is_file:
            self._build_networkx_graph()

        nx.set_node_attributes(self.graph, False, "is_vulnerable")
        nx.set_node_attributes(self.graph, "None", "CVE")
        nx.set_node_attributes(self.graph, "None", "version")
        nx.set_node_attributes(self.graph, "None", "advisory")
        nx.set_node_attributes(self.graph, "blue", "color")
        nx.set_node_attributes(self.graph, False, "external")
        nx.set_node_attributes(self.graph, False, "nearest_transparent_vulnerable")
        return self.graph

    def _generate_dot_file(self, max_bacon):
        """Generates the DOT file using pydeps."""
        
        def run_pydots():
            _args = [
                "-vv",  # Verbose
                f"--max-bacon={max_bacon}",
                "--pylib-all",
                "--cluster",  # Cluster dependencies for clarity
                f"--dot-output={self.dot_file}",
                "--show-dot",
                self.package_name,  # The package to analyze
            ]
            try:
                result = pydeps(**cli.parse_args(_args))
            except SystemExit as e:
                if e.code != 0:
                    raise RuntimeError(f"pydeps failed with exit code {e.code}")

        # Start the thread
        thread = threading.Thread(target=run_pydots)
        thread.start()
        thread.join()  # Wait for the thread to complete

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

    def plot_degree_distribution(self, save=False, path=None):
        """Plots the degree distribution of the vulnerable graph nodes."""
        _graph = self.graph
        _degree_count = [deg for _, deg in _graph.degree()]
        degree_freq = Counter(_degree_count)
        degrees, counts = zip(*sorted(degree_freq.items()))
        sns.barplot(x=list(degrees), y=list(counts), color="blue")
        plt.xlabel("Degree")
        plt.ylabel("Frequency")
        plt.title("Degree Distribution")
        if save:
            if path:
                plt.savefig(path)
            else:
                os.makedirs("distribution/", exist_ok=True)
                plt.savefig(f"distribution/{self.package_name}_dist.png")
        plt.show()
