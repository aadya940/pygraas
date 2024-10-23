### Notes

Requires: `Git` & `PyDeps`.

PyGraas executes shell commands internally, hence `git` and `pydeps` need to 
be configured correctly and be added to system path.

### Examples

```
from pygraas import DependencyGraph

g = DependencyGraph("chainopy", "https://github.com/aadya940/chainopy")
g.build_graph()
g.visualize_graph()
nodes = g.get_nodes()
print(nodes)
```
