"""po_core.config — package marker for importlib.resources.

This file makes `po_core.config` importable as a Python package so that
`importlib.resources.files("po_core.config")` can locate bundled YAML
configuration files (battalion_table.yaml, pareto_table.yaml, etc.) from
within an installed wheel or sdist.
"""
