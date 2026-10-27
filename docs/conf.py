"""Sphinx configuration for the Orange County Lettings documentation.

Sphinx imports the Django project to read its docstrings, so Django is started here first.
"""

import os
import sys

import django

# -- Django setup --------------------------------------------------------------
# Make the project importable from docs/.
sys.path.insert(0, os.path.abspath('..'))

# settings.py refuses to start without a key. A documentation build has no .env file:
# a fake key is enough, nothing is signed while building the docs.
os.environ.setdefault('SECRET_KEY', 'fake-key-for-docs-build')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
django.setup()

# -- Project information -------------------------------------------------------
project = 'Orange County Lettings'
copyright = '2026, Jonathan Zvara'
author = 'Jonathan Zvara'

# -- General configuration -----------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',   # reads the docstrings of the code
    'sphinx.ext.napoleon',  # understands the Google style used in the docstrings
]
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'fr'

# -- HTML output ---------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'
