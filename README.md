# PyGraas: A Vulnerability Analysis and Restriction Layer for Python Packages

## Overview
PyGraas provides a runtime safety mechanism by offering a Graph Analytics and Restriction layer on top of Python packages. It helps in identifying vulnerable dependencies and allows for the restriction of unsafe functions.

## Features
- **Dependency Graph**: Build a DependencyGraph for Python packages.
- **Vulnerability Detection**: Identify vulnerable Python dependencies using VulnerabilityGraph and analyze these graphs.
- **Function Restrictions**: Block vulnerable functions, even those deep in the call stack.
- **Graph Export**: Export graphs as GEXF files for further analysis.
- **User-Friendly API**: Easy to use and integrate into existing projects.

## Installation
To install PyGraas, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aadya940/pygraas.git
   cd pygraas
   ```

2. **Install Dependencies**:
   You can install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the Package**:
   You can install the package using:
   ```bash
   pip install .
   ```

## Usage
Here's a quick example of how to use PyGraas to analyze a package:

### Example: Generating a Dependency Graph
```python
from pygraas import DependencyGraph

# Create a DependencyGraph for the 'numpy' package
g = DependencyGraph(package_name="numpy", package_url="https://github.com/numpy/numpy")

# Build the graph with a maximum depth of 4
graph = g.build_graph(max_bacon=4)

# Get the nodes and edges
nodes = g.get_nodes()
edges = g.get_edges()

print("Nodes:", nodes)
print("Edges:", edges)
```

### Example: Analyzing Vulnerabilities
```python
from pygraas import VulnerabilityGraph

# Create a VulnerabilityGraph based on the DependencyGraph
v = VulnerabilityGraph(graph)

# Build the vulnerability graph
vulnerability_graph = v.build_vulnerability_graph()

# Get vulnerable packages
vulnerables = v.get_vulnerables(details=True)
print("Vulnerable Packages:", vulnerables)
```

## Notes
- **Requirements**: 
  - Ensure you have `Git` and `PyDeps` installed and configured correctly in your system path.
  - Data Source: Vulnerability data is sourced from [Safety DB](https://github.com/pyupio/safety-db).

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the contributors and the open-source community for their support and contributions.

### Examples

Refer `examples/test.ipynb`.


