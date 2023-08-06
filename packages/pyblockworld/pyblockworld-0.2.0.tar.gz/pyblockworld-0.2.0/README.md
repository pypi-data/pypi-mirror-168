Eine an Minecraft angelehnte Welt aus Blöcken.


```python
    def b_key_pressed(world:World):
        print("b pressed. player at", world.player_position())
        x,y,z = world.player_position()
        world.setBlock(x,y,z, "default:brick")
        
    world = World("DEMO WORLD")
    print("Block types", World.MATERIALS)
    world.build_key_function = b_key_pressed
    world.run()
```
