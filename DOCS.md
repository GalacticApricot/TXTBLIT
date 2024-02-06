# TXTBLIT: PyGame-style ASCII Art Frame Rendering Library

TXTBLIT is a Python library designed for rendering ASCII art frames with PyGame-style features. It provides a simple interface for creating and managing screens, objects, scenes, animations, and more. TXTBLIT is built to be user-friendly, allowing developers to easily create interactive ASCII art applications.

## Installation

TXTBLIT relies on external libraries such as `getkey` for input handling. To install the required dependencies, use the following:

```bash
pip install getkey
```

## Usage

```python
from txtblit import *
```

## Classes

### `screen`

#### `__init__(self, width=100, height=34, clock=60)`

- `width`: Width of the screen in characters.
- `height`: Height of the screen in characters.
- `clock`: Clock speed for updating the screen.

Creates a new screen with the specified width, height, and clock speed.

#### `_inp(self)`

Handles input asynchronously, allowing for interactive user input.

#### `update(self)`

Updates the screen, rendering objects and handling input.

#### `clear(self)`

Clears the screen and removes all objects.

#### `oninput(self, func)`

Registers a callback function for handling user input.

### `scene`

#### `__init__(self, objects: list, screen=None)`

- `objects`: List of objects to include in the scene.
- `screen`: Screen to associate with the scene.

Creates a new scene with the specified objects and an optional screen.

#### `load(self)`

Clears the screen and loads the objects of the scene.

#### `add(self, object)`

Adds an object to the scene.

### `animation`

#### `__init__(self, frames: list)`

- `frames`: List of frames for the animation.

Creates a new animation with the specified frames.

### `animator`

#### `__init__(self, object)`

- `object`: The object to animate.

Creates an animator for the specified object.

#### `update(self)`

Updates the animation frame based on the clock speed.

### `object`

#### `__init__(self)`

Creates a new object.

#### `new(self, image: str, x: int, y: int, screen: screen)`

Creates a new object with the provided image, position, and screen.

#### `rect(self, width: int, height: int, x: int, y: int, screen: screen)`

Creates a new object with a rectangular image, position, and screen.

#### `move(self, vector: tuple)`

Moves the object by the specified vector.

#### `animate(self, animation: list, delay=0, loop=True)`

Sets the animation frames, delay, and looping behavior.

#### `update(self)`

Updates the object, including animation and collision detection.

#### `center(self, offset=(0, 0))`

Centers the object on the screen with an optional offset.

#### `delete(self)`

Deletes the object and removes it from the screen.

### `player`

#### `__init__(self, object: object, health: int)`

- `object`: The player's object.
- `health`: Initial health of the player.

Creates a player with the specified object and health.

#### `hit(self, amount: int)`

Reduces the player's health by the specified amount and returns the updated health.

### `enemy`

#### `__init__(self, object: object, health: int, damage: int)`

- `object`: The enemy's object.
- `health`: Initial health of the enemy.
- `damage`: Damage inflicted by the enemy.

Creates an enemy with the specified object, health, and damage.

### Utility Functions

#### `ml(text)`

Formats text into multiple lines with a maximum line length of 75 characters.

#### `istouching(a: object, b: object)`

Checks if two objects are touching.

#### `FindFirstAncestorWhichIsA(object, objtype: str)`

Finds the first ancestor of the given object that matches the specified type.

#### `wrap(text, index)`

Wraps text to a new line after a specified index.
