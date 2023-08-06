# Presto

> One of Chopin's 24 Preludes. A virtuosic prelude, presents a technical challenge with its rapid hold-and-release of eighth notes against quarter notes in the right hand, involving chromatic movement.

# Usage

Install with:

```bash
pip install detect-probe
```

Include presto in a project with:

```python
from detect_probe.service import ProbeService

probe_svc = ProbeService(token='3da7f868f6790d1a562b8f10e7e0785597670000')
probe_svc.start()
```

You can stop the probe process gracefully during app shutdown with:

```python
probe_svc.stop()
```

# Developer guide

Make changes then install locally before testing:
```
pip install .
```

To publish a new version on [PyPy](https://pypi.org/project/detect-probe/):
```commandline
python -m build
python -m twine upload --repository pypi dist/*
```