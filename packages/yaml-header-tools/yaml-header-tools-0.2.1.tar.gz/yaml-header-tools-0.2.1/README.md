# YAML Header Tools

A python package to manage yaml header in markdown document


YAML-Headers for markdown documents are described in:
https://pandoc.org/MANUAL.html#extension-yaml_metadata_block

They are used by many systems to include metadata in markdown documents.

This python package can be installed using `pip`, e.g.:
```bash
pip install --user .
```

# Usage

The following example loads a yaml header from a markdown file.

```python
from yaml_header_tools import *

header = get_header_from_file("testfile.md")
```

# Running the tests

After installation of the package run (within the project folder):

```bash
pytest
```


# Contributers

The original authors of this package are:

- Alexander Schlemmer
- Daniel Hornung
- Timm Fitschen

# License

Copyright (C) 2019-2022 Research Group Biomedical Physics, Max Planck Institute for
Dynamics and Self-Organization Göttingen.

All files in this repository are licensed under a [GNU Affero General Public
License](LICENCE.md) (version 3 or later).

