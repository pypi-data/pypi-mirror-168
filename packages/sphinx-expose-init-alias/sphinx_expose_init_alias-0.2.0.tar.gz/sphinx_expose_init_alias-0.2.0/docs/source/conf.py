# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys

sys.path.insert(0, "../")

import sphinx_expose_init_alias.__about__

project = 'sphinx_expose_init_alias'
copyright = '2022, cmsxbc'
author = 'cmsxbc'
release = str(sphinx_expose_init_alias.__about__.__version__)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_expose_init_alias'
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_typehints = "both"
sphinx_expose_init_alias_as_attr = False
sphinx_expose_init_alias_show_description = False
sphinx_expose_init_alias_with_not_alias = False



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
