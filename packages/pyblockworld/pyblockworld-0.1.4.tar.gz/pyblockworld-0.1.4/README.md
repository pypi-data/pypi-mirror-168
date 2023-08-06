Eine an Minecraft angelehnte Welt aus Blöcken.


```python
    def b_key_pressed(world):
        print("b pressed. player at", world.player_position())

    world = World("DEMO")
    world.build_key_function = b_key_pressed
    world.run()
```
