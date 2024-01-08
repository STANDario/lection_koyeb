import sys
import os

sys.path.append(os.path.abspath(".."))

project = 'Dogs Rest API'
copyright = '2024, standario'
author = 'standario'

extensions = ["sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
