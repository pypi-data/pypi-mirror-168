# PyBlockWorld

Eine an Minecraft angelehnte Welt aus Blöcken.

## Installation

Die Installation erfolgt über ``pip install pyblockworld``.

## API

```python
    from pyblockworld import World

    # Eine Funktion, die beim Drücken der B-Taste aufgerufen werden soll
    def b_key_pressed(world:World):
        print("b pressed. player at", world.player_position())
        x,y,z = world.player_position()

        # Neue Blöcke können mit setBlock gesetzt werden
        # Verfügbare Materialien stehen in World.MATERIALS
        print("Block types", World.MATERIALS)
        world.setBlock(x,y,z, "default:brick")

        # Mehrere Blöcke auf einmal setzen
        x,y,z = x,y,z+3
        world.setBlocks(x,y,z, x+3,y+3,z+3, "default:brick")
        
    world = World("DEMO WORLD")
    # Die Funktion für die build-Taste (b) wird zugewiesen
    world.build_key_function = b_key_pressed
    # Die Welt wird gestartet
    world.run()
```
