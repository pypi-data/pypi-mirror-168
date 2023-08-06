# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyblockworld']
install_requires = \
['pyglet>=1.5.26,<2.0.0']

setup_kwargs = {
    'name': 'pyblockworld',
    'version': '0.2.1',
    'description': 'Minecraft like Block world in Python',
    'long_description': '# PyBlockWorld\n\nEine an Minecraft angelehnte Welt aus Blöcken.\n\n## Installation\n\nDie Installation erfolgt über ``pip install pyblockworld``.\n\n## API\n\n```python\n    from pyblockworld import World\n\n    # Eine Funktion, die beim Drücken der B-Taste aufgerufen werden soll\n    def b_key_pressed(world:World):\n        print("b pressed. player at", world.player_position())\n        x,y,z = world.player_position()\n\n        # Neue Blöcke können mit setBlock gesetzt werden\n        # Verfügbare Materialien stehen in World.MATERIALS\n        print("Block types", World.MATERIALS)\n        world.setBlock(x,y,z, "default:brick")\n\n        # Mehrere Blöcke auf einmal setzen\n        x,y,z = x,y,z+3\n        world.setBlocks(x,y,z, x+3,y+3,z+3, "default:brick")\n        \n    world = World("DEMO WORLD")\n    # Die Funktion für die build-Taste (b) wird zugewiesen\n    world.build_key_function = b_key_pressed\n    # Die Welt wird gestartet\n    world.run()\n```\n',
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
