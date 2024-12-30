import pickle
import networkx as nx
from networkx_gdf import read_gdf, write_gdf

__all__ = [
    "export_graph",
    "load_graph",
]


def export_graph(graph, filename, file_format="gexf"):
    """Export NetworkX graph in various file formats.

    Parameters
    ----------
    graph : networkx.Graph or networkx.MultiDiGraph
        The NetworkX graph to be exported.
    filename : str
        Name of the file with its extension (e.g., file2.gexf).
    file_format : str, optional
        Export graph with format `file_format`. Currently, only supporting
        `gexf`.

    Returns
    -------
    None
    """
    if file_format == "gexf":
        nx.write_gexf(graph, filename)
        return None
    else:
        raise ValueError(f"File format {file_format} not supported.")


def load_graph(filename, file_format="gexf"):
    """Load a NetworkX graph from various file formats.

    Parameters
    ----------
    filename : str
        Name of the file with its extension (e.g., filename.gexf).
    file_format : str, optional
        Load graph with format `file_format`. Currently, only supporting
        `gexf`.

    Returns
    -------
    graph : networkx.Graph or networkx.MultiDiGraph
        The loaded NetworkX graph.
    """
    if file_format == "gexf":
        graph = nx.read_gexf(filename)
        return graph
    else:
        raise ValueError(f"File format {file_format} not supported.")
