import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import json
from pydeps.pydeps import pydeps
from pydeps import cli
import subprocess
import os
import re
from copy import deepcopy
import shutil
import random
from functools import cached_property
from collections import Counter
import seaborn as sns
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque

from ._depgraph import DependencyGraph
from ._utils import _clone_package, _cleanup_dir

import importlib.resources

with importlib.resources.open_text("pygraas", "insecure_full.json") as _f:
    content = _f.read()
    INSECURE_FULL = json.loads(content)


class VulnerabilityGraph:
    """Class to build and analyze a vulnerability graph based on a dependency graph."""

    def __init__(self, graph: DependencyGraph, allow_clone=False):
        """
        Initialize the VulnerabilityGraph.

        Parameters:
        - graph (DependencyGraph): The dependency graph to analyze.
        - allow_clone (bool): Whether to allow cloning the package.
        """
        self.graph = deepcopy(graph)
        self.checked_packages = set()
        self.allow_clone = allow_clone

    def build_vulnerability_graph(self):
        """Builds the vulnerability graph by checking each package in \
        the graph against the INSECURE_FULL list."""

        # Get & Parse the external dependencies sent to `stdout`.
        _args = [
            "pydeps",
            "-vv",
            f"--max-bacon={self.graph.max_bacon}",
            "--external",
            f"{self.graph.package_name}",
        ]

        if not (self.graph.package_name in os.listdir(".")):
            _clone_package(
                self.graph.package_name, self.graph.package_url, clone=self.allow_clone
            )

        result = subprocess.run(
            _args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"pydeps failed: {result.stderr}")

        try:
            result_list = json.loads(result.stdout)
        except json.JSONDecodeError:
            raise ValueError("Failed to decode pydeps output")

        vul_base = INSECURE_FULL.get(self.graph.package_name) or INSECURE_FULL.get(
            self.graph.package_name.lower()
        )
        if vul_base:
            _node, __bool = self._get_graph_node(self.graph.package_name)
            if __bool:
                self._mark_vulnerable(_node, vul_base, self.graph.package_name)

        # A function to get relevant nodes from graph if vulnerable.
        for _package in result_list:
            vulnerabilities = INSECURE_FULL.get(_package) or INSECURE_FULL.get(
                _package.lower()
            )
            node, _bool = self._get_graph_node(_package)

            try:
                node["external"] = True
            except:
                print(f"Passed external assignment for {_package}")
                pass

            if vulnerabilities:
                node, _bool = self._get_graph_node(_package)
                if _bool:
                    self._mark_vulnerable(node, vulnerabilities, _package)

        # Cleanup
        _cleanup_dir(self.graph.package_name)

        return self.graph

    def _get_graph_node(self, package):
        """Retrieve the graph node for a given package."""
        try:
            node = self.graph.graph.nodes[package]
            assert node is not None
            return node, True
        except KeyError as e:
            return None, False

    def _mark_vulnerable(self, node, vulnerabilities, package):
        """Mark a node as vulnerable and update its metadata."""
        if package not in self.checked_packages:
            assert "CVE" in node.keys()
            assert "version" in node.keys()
            assert "advisory" in node.keys()
            assert "is_vulnerable" in node.keys()
            assert "color" in node.keys()

            if node["is_vulnerable"] == False:
                node["is_vulnerable"] = True
                node["color"] = "red"
                _cve, _v, _advisory = self._get_vulnerability_metadata(vulnerabilities)
                node["CVE"] = str(_cve)
                node["version"] = str(_v)
                node["advisory"] = str(_advisory)
                self.checked_packages.add(package)

    def _get_vulnerability_metadata(self, vulnerabilities):
        """Extract vulnerability metadata from the vulnerabilities list."""
        if isinstance(vulnerabilities, dict):
            vulnerabilities = [vulnerabilities]

        _cve = []
        _v = []
        _advisory = []

        if isinstance(vulnerabilities, list):
            for vul_dict in vulnerabilities:
                _cve.append(vul_dict["cve"])
                _v.append(vul_dict["v"])
                _advisory.append(vul_dict["advisory"])

        return _cve, _v, _advisory

    def get_vulnerables(self, details=False):
        """Get a list of vulnerable nodes in the graph.

        Parameters:
        - details (bool): Whether to return detailed information about vulnerabilities.

        Returns:
        - List: A list of vulnerable nodes.
        """
        vulnerables = []
        for node in self.graph.graph.nodes:
            if self.graph.graph.nodes[node]["is_vulnerable"] == True:
                if details:
                    vulnerables.append({node: self.graph.graph.nodes(data=True)[node]})
                else:
                    vulnerables.append(node)

        return vulnerables

    def get_degree(self, node, details=True):
        """Get the in-degree and out-degree of a node.

        Parameters:
        - node (str): The node to analyze.
        - details (bool): Whether to return detailed degree information.

        Returns:
        - dict or int: Degree information or just the degree value.
        """
        if details:
            in_degree = self.graph.graph.in_degree(node)
            out_degree = self.graph.graph.out_degree(node)

            return {
                "in_degree": in_degree,
                "out_degree": out_degree,
            }

        return self.graph.graph.degree(node)

    def get_vulnerable_public_nodes(self, vul_package):
        """List of Public Nodes that have a path to a vulnerable package.
        Computed Parallely."""
        vulnerables = self.get_vulnerables()

        assert vul_package in vulnerables
        paths = []

        def check_node(node):
            if not (("._" in node) or (node.startswith("_")) or (node in vulnerables)):
                if nx.has_path(self.graph.graph, node, vul_package):
                    return {f"{node} - {vul_package}": True}
            return None

        with ThreadPoolExecutor() as executor:
            future_to_node = {
                executor.submit(check_node, node): node for node in self.graph.graph
            }

            for future in as_completed(future_to_node):
                result = future.result()
                if result is not None:
                    paths.append(result)

        return paths

    def plot_vulnerable_degree_distribution(self, save=False, path=None):
        """plot degree distribution as a matplotlib histogram."""
        _graph = self.graph
        vul_nodes = self.get_vulnerables()
        _degree_count = [self.graph.graph.degree(node) for node in vul_nodes]
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
                os.makedirs("distribution_vul/", exist_ok=True)
                plt.savefig(f"distribution_vul/{self.graph.package_name}_dist_vul.png")
        plt.show()

    def get_nearest_vulnerable_modules(self):
        """Optimized function to find the nearest "transparent" vertices for each vulnerable vertex."""
        # Get the list of vulnerable nodes
        _vul_nodes = self.get_vulnerables()
        _gph = self.graph.graph

        # Initialize the BFS queue and the transparent set
        queue = deque(_vul_nodes)  # Use deque for faster pops
        transparent_set = set()
        visited = set(_vul_nodes)  # Track visited nodes to avoid redundant processing

        while queue:
            # Pop the first vulnerable vertex from the queue
            vul_node = queue.popleft()

            # Iterate through each neighbor of the vulnerable node
            for neighbor in _gph[vul_node]:
                if neighbor in visited:
                    continue  # Skip already visited neighbors

                visited.add(neighbor)  # Mark the neighbor as visited
                if _gph.nodes.get(neighbor, {}).get("external", False):
                    # Add black-box neighbors to the queue
                    queue.append(neighbor)
                else:
                    # Mark non-external neighbors as "transparent" and add to the set
                    transparent_set.add(neighbor)
                    self.graph.graph.nodes[neighbor][
                        "nearest_transparent_vulnerable"
                    ] = True

        # Return the union of the transparent set as the required patches
        return list(transparent_set)

    def save_graph(self, path):
        """Save the vulnerability graph to a file."""
        nx.write_gexf(self.graph.graph, path)
