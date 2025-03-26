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
from unittest.mock import patch

from ._utils import get_package, _cleanup_dir

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
                "-vv",
                f"--max-bacon={max_bacon if max_bacon is not None else 2}",
                "--pylib-all",
                "--cluster",
                "--show-cycles",
                f"--dot-output={self.dot_file}",  # Save the DOT file
                "--show-dot",
                self.package_name,
            ]

            try:
                with patch("pydeps.dot.display_svg") as mock_fetch:
                    mock_fetch.return_value = None
                    result = pydeps(**cli.parse_args(_args))
            except SystemExit as e:
                _cleanup_dir(self.package_name)
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
