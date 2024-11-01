### PyGraas: A Vulnerability Analysis and Restriction Layer for Python Packages.

We ensure runtime safety by providing a Graph Analytics and
Restriction layer on top of Python Packages.

##### Features:
🟢  Build DependencyGraph for Python Packages.
🟢 Detect Vulnerable Python Dependencies using VulnerabilityGraph, analyse
these graphs.
🟢 Block Vulnerable functions, even the ones deep in the call stack.
🟢 A toolkit for security of python packages and graph analytics.
🟢 Easy to use API.

### Installation
🔴 Download the wheel from `https://github.com/aadya940/pygraas`.
🔴 pip install (.whl file).
🔴 Follow `Examples` section.

### Notes
```
> Requires: `Git` & `PyDeps`.
> PyGraas executes shell commands internally, hence `git` and `pydeps` need to 
be configured correctly and be added to system path. 

> Data Source: https://github.com/pyupio/safety-db
```

### Examples

Refer `examples/test.ipynb`.


