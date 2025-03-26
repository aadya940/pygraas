"""Graph Analytics on Dependency and Vulnerability Graphs."""

from collections import Counter
import networkx as nx
import graphblas_algorithms as ga
import os
from functools import cache
import matplotlib.pyplot as plt
import numpy as np


@cache
def _get_gb_graph(graph: nx.Graph):
    """Get the nxp graph."""
    return ga.Graph.from_networkx(graph)


def get_degree_distribution(graph: nx.Graph):
    """Plots the degree distribution of the vulnerable graph nodes."""
    _degree_count = [deg for _, deg in graph.degree()]
    degree_freq = Counter(_degree_count)
    degrees, counts = zip(*sorted(degree_freq.items()))
    return degrees, counts


def plot_degree_distribution(graph: nx.Graph, vulnerable_only=False):
    """Plots the in-degree and out-degree distribution of the graph."""
    if vulnerable_only:
        nodes = [n for n in graph.nodes if graph.nodes[n].get("is_vulnerable", False)]
    else:
        nodes = graph.nodes

    in_degrees = [graph.in_degree(n) for n in nodes]
    out_degrees = [graph.out_degree(n) for n in nodes]

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(
        in_degrees, bins=np.arange(max(in_degrees) + 1) - 0.5, color="blue", alpha=0.7
    )
    plt.title("In-Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.hist(
        out_degrees, bins=np.arange(max(out_degrees) + 1) - 0.5, color="red", alpha=0.7
    )
    plt.title("Out-Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()


def compute_shortest_paths_and_diameter(graph: nx.Graph):
    """Compute shortest paths between all pairs of vulnerable nodes and find diameters."""
    vulnerable_nodes = [
        n for n in graph.nodes if graph.nodes[n].get("is_vulnerable", False)
    ]
    vulnerable_subgraph = graph.subgraph(vulnerable_nodes)
    # Full graph diameter
    full_diameter = nx.diameter(graph) if nx.is_connected(graph) else float("inf")
    # Vulnerable subgraph diameter
    vulnerable_diameter = (
        nx.diameter(vulnerable_subgraph)
        if nx.is_connected(vulnerable_subgraph)
        else float("inf")
    )

    return full_diameter, vulnerable_diameter


def calculate_pagerank_and_cycles(graph: nx.Graph):
    """Calculate PageRank of vulnerable nodes and check for cycles."""
    vulnerable_nodes = [
        n for n in graph.nodes if graph.nodes[n].get("is_vulnerable", False)
    ]
    _graph = _get_gb_graph(graph)
    pagerank = nx.pagerank(_graph, nodes=vulnerable_nodes)
    return pagerank


def calculate_cut_size(graph: nx.Graph):
    """Calculate the cut size between vulnerable and non-vulnerable nodes."""
    vulnerable_nodes = [
        n for n in graph.nodes if graph.nodes[n].get("is_vulnerable", False)
    ]
    non_vulnerable_nodes = [n for n in graph.nodes if n not in vulnerable_nodes]
    _graph = _get_gb_graph(graph)
    cut_size = nx.cut_size(_graph, vulnerable_nodes, non_vulnerable_nodes)
    return cut_size


def find_structural_holes(graph: nx.Graph):
    """Find structural holes in the graph using NetworkX."""
    _graph = _get_gb_graph(graph)
    structural_holes = nx.structural_holes(_graph)
    return structural_holes
