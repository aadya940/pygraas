import pickle
import networkx as nx
import os


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
        try:
            graph = nx.read_gexf(filename)
            return graph
        except:
            _replace_weight_in_gexf(filename)
            graph = nx.read_gexf(filename)
            return graph
    else:
        raise ValueError(f"File format {file_format} not supported.")


def _replace_weight_in_gexf(file_path):
    """
    Opens a GEXF file and replaces weight="&quot;2&quot;" with weight="2".

    Parameters:
        file_path (str): Path to the GEXF file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Replace the target string
        for i in range(9):
            content = content.replace(f'weight="&quot;{i}&quot;"', 'weight=f"{i}"')

        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Replacements made successfully in '{file_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
