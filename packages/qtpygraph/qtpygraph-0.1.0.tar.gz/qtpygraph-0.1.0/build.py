"""QtPyGraph setup script for building wheel."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import toml
from setuptools import find_packages

metadata = toml.load('pyproject.toml')['tool']['poetry']
short_description = (  # pylint: disable=invalid-name
    'A pythonic interface to the Qt Graphics View Framework using qtpy.'
)
long_description = Path('README.rst').read_text(encoding='utf-8')

kwargs = {
    'author': metadata['authors'],
    'classifiers': metadata['classifiers'],
    'description': short_description,
    'license': metadata['license'],
    'long_description_content_type': 'text/x-rst',
    'long_description': long_description,
    'name': metadata['name'],
    'packages': find_packages(),
    'python_requires': '>=3.8,<3.11',
    'version': metadata['version'],
    'zip_safe': False,
}


def build(setup_kwargs: dict[str, Any]) -> None:
    """Force poetry to build with these kwargs."""
    setup_kwargs.update(**kwargs)
