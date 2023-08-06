# PyBlockWorld

Eine an Minecraft angelehnte Welt aus Blöcken.

## Installation

Die Installation erfolgt über ``pip install pyblockworld``.

## API

```python
    from pyblockworld import World

    class MyWorld(World):
        def __init__(self):
            super().__init__()

        # Eine Funktion, die beim Drücken der B-Taste aufgerufen werden soll
        def build_key_pressed(world:World):
            print("B pressed.")
            x,y,z = world.player_position()

            # Neue Blöcke können mit setBlock gesetzt werden.
            # Verfügbare Materialien stehen in World.MATERIALS und umfassen
            # air, default:brick, default:stone, default:sand, default:grass
            print("Block types", World.MATERIALS)
            world.setBlock(x,y,z, "default:brick")

            # Mehrere Blöcke auf einmal abseits des Spielers platzieren
            x,y,z = x,y,z+3
            world.setBlocks(x,y,z, x+3,y+3,z+3, "default:grass")
        
    # Erstellen einer neuen Welt
    my_world = MyWorld()
    # Die Welt wird gestartet
    my_world.run()

```

## Quellen

Der Quellcode basiert auf dem Code von [SensorCraft](https://github.com/AFRL-RY/SensorCraft),
der wiederum auf dem Code von [Craft](https://github.com/fogleman/Craft/) basiert.