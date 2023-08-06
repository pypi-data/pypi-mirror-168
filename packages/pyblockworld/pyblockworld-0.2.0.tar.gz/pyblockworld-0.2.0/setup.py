# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyblockworld']
install_requires = \
['pyglet>=1.5.26,<2.0.0']

setup_kwargs = {
    'name': 'pyblockworld',
    'version': '0.2.0',
    'description': 'Minecraft like Block world in Python',
    'long_description': 'Eine an Minecraft angelehnte Welt aus Blöcken.\n\n\n```python\n    def b_key_pressed(world:World):\n        print("b pressed. player at", world.player_position())\n        x,y,z = world.player_position()\n        world.setBlock(x,y,z, "default:brick")\n        \n    world = World("DEMO WORLD")\n    print("Block types", World.MATERIALS)\n    world.build_key_function = b_key_pressed\n    world.run()\n```\n',
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
