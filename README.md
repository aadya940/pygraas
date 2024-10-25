### Notes

Requires: `Git` & `PyDeps`.

PyGraas executes shell commands internally, hence `git` and `pydeps` need to 
be configured correctly and be added to system path.

Data Source: https://github.com/pyupio/safety-db

### Examples

```
from pygraas import DependencyGraph, VulnerabilityGraph

# Dependency Analysis
g = DependencyGraph("chainopy", "https://github.com/aadya940/chainopy")
g.build_graph()
g.visualize_graph()
nodes = g.get_nodes()
print(nodes)

# Vulnerability Analysis
v = VulnerabilityGraph(g)
v.build_vulnerability_graph()
vulnerable_nodes = v.get_vulnerables()
print(vulnerable_nodes)
```


