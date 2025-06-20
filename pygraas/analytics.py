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

def plot_degree_distribution(graph: nx.Graph, vulnerable_only=False, filename=None):
    """Plots the in-degree and out-degree distribution of the graph."""
    if vulnerable_only:
        nodes = [n for n in graph.nodes if graph.nodes[n].get("is_vulnerable", True)]
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

    if not filename:
        plt.tight_layout()
        plt.show()
        return
    
    plt.savefig(filename)
    return

def vulnerable_diameter(graph: nx.Graph):
    """Compute diameters of vulnerable nodes and find ."""
    if not nx.is_weakly_connected(graph):
        return float('inf')
    
    graph = graph.to_undirected()

    vul_nodes = [node for node, attr in graph.nodes(data=True) if attr["color"] == "red"]
    subgraph_nodes = set(vul_nodes)

    # Find all shortest paths between pairs of non-vulnerable nodes.
    for i, source in enumerate(vul_nodes):
        for target in vul_nodes[i + 1:]:
            # Get the shortest path between source and target
            shortest_path = nx.shortest_path(graph, source=source, target=target)
            # Add all nodes in the path to the subgraph
            subgraph_nodes.update(shortest_path)

    print("Subgraph Nodes are: ",subgraph_nodes)

    _vul = graph.subgraph(list(subgraph_nodes))

    if nx.is_connected(_vul):
        return nx.diameter(_vul.to_undirected())
    else:
        if not nx.is_connected(graph):
            print("Original graph is disconnected.")
        else:      
            print("Impossible, shouldn't be the case.")
            raise
        
    print("Subgraph is disconnected, diameter is 'infy'")
    return float("inf")

def pagerank_and_cycles(graph: nx.Graph):
    """Calculate PageRank of vulnerable nodes and check for cycles."""
    vulnerable_nodes = [
        n for n in graph.nodes if graph.nodes[n].get("is_vulnerable", True)
    ]

    _graph = _get_gb_graph(graph)
    pagerank = nx.pagerank(_graph)
    vul_pagerank = {}

    for node in pagerank:
        if node in vulnerable_nodes:
            vul_pagerank[node] = pagerank[node]

    return vul_pagerank


def cut_size(graph: nx.Graph):
    """Calculate the cut size between vulnerable and non-vulnerable nodes."""
    vulnerable_nodes = [
        n for n in graph.nodes if graph.nodes[n].get("is_vulnerable", True)
    ]
    non_vulnerable_nodes = [n for n in graph.nodes if n not in vulnerable_nodes]
    _graph = _get_gb_graph(graph)
    cut_size = nx.cut_size(_graph, vulnerable_nodes, non_vulnerable_nodes)
    return cut_size

def analyse(graph):
    analysis = {}
    analysis["diameter"] = vulnerable_diameter(graph)
    analysis["pagerank"] = pagerank_and_cycles(graph)
    analysis["cut-size"] = cut_size(graph)
    return analysis

def vulnerable_cycles(graph):
    """
    Return all cycles in the graph that contain at least one vulnerable node.

    Parameters:
    - G: A NetworkX graph with node attribute 'is_vulnerable' set to True or False.

    Returns:
    - List of cycles, where each cycle is a list of nodes.
    """
    cycles = list(nx.simple_cycles(graph))
    vulnerable_cycles = [
        cycle for cycle in cycles
        if any(graph.nodes[node].get("is_vulnerable", False) for node in cycle)
    ]
    return vulnerable_cycles

def effective_size(graph):
    return nx.structuralholes.effective_size(graph)

def constraint(graph):
    return nx.structuralholes.constraint(graph)

def is_dag(graph):
    return nx.is_directed_acyclic_graph(graph)

def v_structures(graph):
    if is_dag(graph):
        pass
    else:
        print("The given graph is not")

    return nx.dag.v_structures(graph)
