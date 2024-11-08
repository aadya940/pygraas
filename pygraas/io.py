import pickle
import networkx as nx
from networkx_gdf import read_gdf, write_gdf

__all__ = [
    "export_graph",
    "load_graph",
]


def export_graph(graph, filename, file_format="pickle"):
    """Export NetworkX graph in various file formats.

    Parameters
    ----------
    graph : networkx.Graph or networkx.MultiDiGraph
        The NetworkX graph to be exported.
    filename : str
        Name of the file with its extension (e.g., file1.pickle, file2.gdf).
    file_format : str, optional
        The format to export the graph to. Supported formats include 'pickle',
        'gdf', 'graphml', 'gml', 'json', 'edgelist', 'adjlist'.
        Default is 'pickle'.

    Returns
    -------
    None
    """
    if file_format == "pickle":
        _save_graph_pickle(graph, filename)
    elif file_format == "gdf":
        _save_graph_gdf(graph, filename)
    elif file_format == "graphml":
        _save_graph_graphml(graph, filename)
    elif file_format == "gml":
        _save_graph_gml(graph, filename)
    elif file_format == "json":
        _save_graph_json(graph, filename)
    elif file_format == "edgelist":
        _save_graph_edgelist(graph, filename)
    elif file_format == "adjlist":
        _save_graph_adjlist(graph, filename)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")


def load_graph(filename, file_format="pickle"):
    """Load a NetworkX graph from various file formats.

    Parameters
    ----------
    filename : str
        Name of the file with its extension (e.g., file1.pickle, file2.gdf).
    file_format : str, optional
        The format of the file to load the graph from. Supported formats include
        'pickle', 'gdf', 'graphml', 'gml', 'json', 'edgelist', 'adjlist'.
        Default is 'pickle'.

    Returns
    -------
    graph : networkx.Graph or networkx.MultiDiGraph
        The loaded NetworkX graph.
    """
    if file_format == "pickle":
        return _load_graph_pickle(filename)
    elif file_format == "gdf":
        return _load_graph_gdf(filename)
    elif file_format == "graphml":
        return _load_graph_graphml(filename)
    elif file_format == "gml":
        return _load_graph_gml(filename)
    elif file_format == "json":
        return _load_graph_json(filename)
    elif file_format == "edgelist":
        return _load_graph_edgelist(filename)
    elif file_format == "adjlist":
        return _load_graph_adjlist(filename)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")


# Export Helper Functions
def _save_graph_pickle(graph, filename):
    try:
        with open(filename, "wb") as f:
            pickle.dump(graph, f)
        print(f"Graph successfully saved to {filename} (pickle format).")
    except IOError as e:
        print(f"Failed to save graph (pickle): {e}")


def _save_graph_gdf(graph, filename):
    try:
        write_gdf(graph, filename)
        print(f"Graph successfully saved to {filename} (GDF format).")
    except IOError as e:
        print(f"Failed to save graph (GDF): {e}")


def _save_graph_graphml(graph, filename):
    try:
        nx.write_graphml(graph, filename)
        print(f"Graph successfully saved to {filename} (GraphML format).")
    except Exception as e:
        print(f"Failed to save graph (GraphML): {e}")


def _save_graph_gml(graph, filename):
    try:
        nx.write_gml(graph, filename)
        print(f"Graph successfully saved to {filename} (GML format).")
    except Exception as e:
        print(f"Failed to save graph (GML): {e}")


def _save_graph_json(graph, filename):
    try:
        nx.node_link_data(graph)
        nx.write_gml(graph, filename)
        print(f"Graph successfully saved to {filename} (JSON format).")
    except Exception as e:
        print(f"Failed to save graph (JSON): {e}")


def _save_graph_edgelist(graph, filename):
    try:
        nx.write_edgelist(graph, filename)
        print(f"Graph successfully saved to {filename} (Edge List format).")
    except Exception as e:
        print(f"Failed to save graph (Edge List): {e}")


def _save_graph_adjlist(graph, filename):
    try:
        nx.write_adjlist(graph, filename)
        print(f"Graph successfully saved to {filename} (Adjacency List format).")
    except Exception as e:
        print(f"Failed to save graph (Adjacency List): {e}")


# Load Helper Functions
def _load_graph_pickle(filename):
    try:
        with open(filename, "rb") as f:
            graph = pickle.load(f)
        print(f"Graph successfully loaded from {filename} (pickle format).")
        return graph
    except IOError as e:
        print(f"Failed to load graph (pickle): {e}")
        raise


def _load_graph_gdf(filename):
    try:
        graph = read_gdf(filename)
        print(f"Graph successfully loaded from {filename} (GDF format).")
        return graph
    except IOError as e:
        print(f"Failed to load graph (GDF): {e}")
        raise


def _load_graph_graphml(filename):
    try:
        graph = nx.read_graphml(filename)
        print(f"Graph successfully loaded from {filename} (GraphML format).")
        return graph
    except Exception as e:
        print(f"Failed to load graph (GraphML): {e}")
        raise


def _load_graph_gml(filename):
    try:
        graph = nx.read_gml(filename)
        print(f"Graph successfully loaded from {filename} (GML format).")
        return graph
    except Exception as e:
        print(f"Failed to load graph (GML): {e}")
        raise


def _load_graph_json(filename):
    try:
        graph = nx.node_link_data(nx.read_gml(filename))
        print(f"Graph successfully loaded from {filename} (JSON format).")
        return graph
    except Exception as e:
        print(f"Failed to load graph (JSON): {e}")
        raise


def _load_graph_edgelist(filename):
    try:
        graph = nx.read_edgelist(filename, create_using=nx.MultiDiGraph)
        print(f"Graph successfully loaded from {filename} (Edge List format).")
        return graph
    except Exception as e:
        print(f"Failed to load graph (Edge List): {e}")
        raise


def _load_graph_adjlist(filename):
    try:
        graph = nx.read_adjlist(filename, create_using=nx.MultiDiGraph)
        print(f"Graph successfully loaded from {filename} (Adjacency List format).")
        return graph
    except Exception as e:
        print(f"Failed to load graph (Adjacency List): {e}")
        raise
