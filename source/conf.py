# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'noimemo'
copyright = '2023, noim'
author = 'noim'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sphinx_fontawesome

extensions = [
    "sphinx.ext.githubpages",
    "myst_parser",
    "sphinx_markdown_tables",
    "sphinxcontrib.mermaid",
    "sphinx_fontawesome",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
