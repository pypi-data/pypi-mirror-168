# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyblockworld']
install_requires = \
['pyglet>=1.5.26,<2.0.0']

setup_kwargs = {
    'name': 'pyblockworld',
    'version': '0.2.3',
    'description': 'Minecraft like Block world in Python',
    'long_description': '# PyBlockWorld\n\nEine an Minecraft angelehnte Welt aus Blöcken.\n\n## Installation\n\nDie Installation erfolgt über ``pip install pyblockworld``.\n\n## API\n\n```python\n    from pyblockworld import World\n\n    class MyWorld(World):\n        def __init__(self):\n            super().__init__()\n\n        # Eine Funktion, die beim Drücken der B-Taste aufgerufen werden soll\n        def build_key_pressed(world:World):\n            print("B pressed.")\n            x,y,z = world.player_position()\n\n            # Neue Blöcke können mit setBlock gesetzt werden.\n            # Verfügbare Materialien stehen in World.MATERIALS und umfassen\n            # air, default:brick, default:stone, default:sand, default:grass\n            print("Block types", World.MATERIALS)\n            world.setBlock(x,y,z, "default:brick")\n\n            # Mehrere Blöcke auf einmal abseits des Spielers platzieren\n            x,y,z = x,y,z+3\n            world.setBlocks(x,y,z, x+3,y+3,z+3, "default:grass")\n        \n    # Erstellen einer neuen Welt\n    my_world = MyWorld()\n    # Die Welt wird gestartet\n    my_world.run()\n\n```\n\n## Quellen\n\nDer Quellcode basiert auf dem Code von [SensorCraft](https://github.com/AFRL-RY/SensorCraft),\nder wiederum auf dem Code von [Craft](https://github.com/fogleman/Craft/) basiert.',
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
