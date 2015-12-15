#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
extensions = [
    # 'sphinx.ext.intersphinx',
    # 'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]
# intersphinx_mapping = {'http://docs.python.org/': None}

primary_domain = 'py'
default_role = 'py:obj'

# Show todo and todolists
todo_include_todos = True

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'COS Development'
copyright = '2014-2015, Center for Open Science'
version = release = '1.0'
exclude_patterns = ['_build']
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# Example configuration for intersphinx: refer to the Python standard library.
