import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import json
from pydeps.pydeps import pydeps
from pydeps import cli
import subprocess
import os
from copy import deepcopy
import shutil

from .depgraph import DependencyGraph
from ._cloner import _clone_package

with open("pygraas/insecure_full.json", "r") as _f:
    INSECURE_FULL = json.loads(_f.read())


class VulnerabilityGraph:
    def __init__(self, graph: DependencyGraph):
        self.graph = deepcopy(graph)
        self.checked_packages = set()

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
            _clone_package(self.graph.package_name, self.graph.package_url)

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

            if vulnerabilities:
                node, _bool = self._get_graph_node(_package)
                if _bool:
                    self._mark_vulnerable(node, vulnerabilities, _package)

        # Cleanup
        if self.graph.package_name in os.listdir("."):
            shutil.rmtree(self.graph.package_name)

        return self.graph

    def _get_graph_node(self, package):
        try:
            node = self.graph.graph.nodes[package]
            assert node is not None
            return node, True
        except KeyError as e:
            return _, False

    def _mark_vulnerable(self, node, vulnerabilities, package):
        if package not in self.checked_packages:
            assert "CVE" in node.keys()
            assert "version" in node.keys()
            assert "advisory" in node.keys()
            assert "is_vulnerable" in node.keys()
            assert "color" in node.keys()

            if not node["is_vulnerable"]:
                node["is_vulnerable"] = True
                node["color"] = "red"
                _cve, _v, _advisory = self._get_vulnerability_metadata(vulnerabilities)
                node["CVE"] = _cve
                node["version"] = _v
                node["advisory"] = _advisory
                self.checked_packages.add(package)

    def _get_vulnerability_metadata(self, vulnerabilities):
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
