# QE Metrics Documentation

## Quick Start

Generate the html pages, simply do

```bash
cd docs
make html
```

That it will generate the html documentation under _build/html/

## Updating documentation

Adding new modules in the documentation, make sure that the module directory has `__init__.py` file.

The update is also simply as running the following from the root directory of the project

```bash
sphinx-apidoc -o docs .
```
