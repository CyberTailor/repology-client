# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2023-2024 Anna <cyber@sysrq.in>

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'repology-client'
author = 'Anna <cyber@sysrq.in>'
copyright = f'2024, {author}'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_prompt',
]

try:
    import notfound.extension
    extensions.append('notfound.extension')

    notfound_urls_prefix = None
except ModuleNotFoundError:
    pass

try:
    import sphinx_sitemap
    extensions.append('sphinx_sitemap')

    sitemap_locales = [None]
    sitemap_url_scheme = '{link}'
except ModuleNotFoundError:
    pass

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    'aiohttp': ('https://docs.aiohttp.org/en/stable', None),
}

autodoc_default_flags = [
    'members',
    'show-inheritance',
    'inherited-members',
    'undoc-members',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'aiohttp_theme'
html_permalinks_icon = '#'
html_theme_options = {
    'description': 'Asynchronous Python wrapper for Repology API',
    'canonical_url': 'https://repology-client.sysrq.in/',
}
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}

html_static_path = ['_static']
html_title = f'{project} {release}'
html_baseurl = 'https://repology-client.sysrq.in/'
