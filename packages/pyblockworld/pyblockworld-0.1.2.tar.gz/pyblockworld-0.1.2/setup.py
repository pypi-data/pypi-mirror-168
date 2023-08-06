# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyblockworld']
install_requires = \
['pyglet>=1.5.26,<2.0.0']

setup_kwargs = {
    'name': 'pyblockworld',
    'version': '0.1.2',
    'description': 'Minecraft like Block world in Python',
    'long_description': 'Eine an Minecraft angelehnte Welt aus Blöcken.',
    'author': 'Marco Bakera',
    'author_email': 'marco@bakera.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
