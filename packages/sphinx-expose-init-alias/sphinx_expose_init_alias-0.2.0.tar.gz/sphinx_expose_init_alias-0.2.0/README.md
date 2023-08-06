# sphinx-expose-init-alias
![pypi](https://img.shields.io/pypi/v/sphinx-expose-init-alias)
[![Main](https://github.com/cmsxbc/sphinx-expose-init-alias/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/cmsxbc/sphinx-expose-init-alias/actions/workflows/main.yml)

Generate doc of exposed stuff in \_\_init\_\_.py  as alias

## What-Is-Wanted

We sometimes do "re-expose" in `__init__.py` to improve experience of using our library.
Such as

```Python
# lib/a.py

def foo():
  ...

# lib/__init__.py

from .a import foo


```

But the `foo` in `lib/__init__.py` will only occur in docs when use `sphinx.ext.autodoc` if we put it in the `__all__` in `lib/__init__.py`.
And wrose thing is that the content is just like a stuff defined in `lib/__init__.py`, which is a bit confused and duplicated.

## Demo

See this repo's github pages: [sphinx-expose-init-alias Docs](https://cmsxbc.github.io/sphinx-expose-init-alias/)

## Usage

```reStructuredText
# docs/lib.rst

.. autoaliasmodule:: lib
  :members:

```
