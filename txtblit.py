from os import system, name
import threading, time
from getkey import getkey, keys

def handle(*args):
  pass

def _blank(width, height):
  list = []
  d =  ''
  for i in range(height):
    d = ''
    for i in range(width):
      d = d + ' '
    list.append(d)
  return list


class screen:
  def __init__(self, width=100, height=34, clock=60):
    self.width = width
    self.height = height
    self.center = (width // 2, height // 2)
    list = []
    d =  ''
    for i in range(height):
      d = ''
      for i in range(width):
        d = d + ' '
      list.append(d)
    self.context = list
    self.objects = []
    self.clock = 0
    self.max = clock
    self._inputfunction = handle
    self._inputbuffer = ''
    self._prev = ''
    self.la = []
    d = ''
    for _ in range(width + 2):
      d = d + '█'
    self._bar = d
    threading.Thread(target=self._inp).start()
  def _inp(self):
    while True:
      key = getkey()
      if key == keys.ENTER:
        self._inputfunction(self._inputbuffer)
        self._inputbuffer = ''
      elif key == keys.BACKSPACE:
        self._inputbuffer = self._inputbuffer[:-1]
      else:
        self._inputbuffer = self._inputbuffer + key
      time.sleep(0)
  def update(self):
    self.la = self.context
    final = self._bar
    self.clock += 1
    if self.clock == self.max:
      self.clock = 0
    self.context = _blank(self.width, self.height)
    for object in self.objects:
      object.update()
      if isinstance(object.image, str):
        object.image = [object.image]
      for xi in range(len(object.image)):
        line = self.context[object.y + xi]
        objstr = object.image[xi]
        width = len(objstr)        
        self.context[object.y + xi] = f'{line[:object.x]}{objstr}{line[(object.x + width):]}'
    for i in self.context:
      final = f'{final}\n█{i}█'
    final = f'{final}\n{self._bar}'
    final = f'{final}\n{self._inputbuffer}'
    if final != self._prev:
      system('cls' if name == 'nt' else 'clear')
      print(final)
    self._prev = final
  def clear(self):
    for object in self.objects:
      object.delete()
    self.objects = []
    list = []
    d =  ''
    for i in range(self.height):
      d = ''
      for i in range(self.width):
        d = d + ' '
      list.append(d)
    self.context = list
  def oninput(self, func):
    self._inputfunction = func


class scene:
  def __init__(self, objects: list, screen=None):
    self.objects = objects
    if not screen:
      screen = self.objects[0]._screen
    self.screen = screen
    for i in self.objects:
      for x, v in enumerate(self.screen.objects):
        if i == v:
          self.screen.objects.pop(x)
  def load(self):
    self.screen.clear()
    self.screen.objects = self.objects
  def add(self, object):
    self.objects.append(object)
    for i, v in enumerate(self.screen.objects):
      if object == v:
        self.screen.objects.pop(i)
    

class animation:
  def __init__(self, frames: list):
    self.frames = frames
    self.frame = 0
    self.last = len(frames)
    self.delay = 0
    self.parent = None
    self.loop = True

class animator:
  def __init__(self, object):
    self.parent = object
    self.animation = animation([object.image])
    self.animation.parent = self
  def update(self):
    if self.animation.last != len(self.animation.frames):
      self.animation.last = len(self.animation.frames)
    if self.parent._screen.clock == 0 or self.parent._screen.clock % (self.animation.delay + 1) == 0:
      if self.animation.last != 1:
        self.animation.frame += 1
      self.parent.image = self.animation.frames[self.animation.frame]
      if self.animation.frame == self.animation.last - 1:
        if self.animation.loop:
          self.animation.frame = -1
        else:
          self.animation.frame -= 1
    
    

class object:
  def __init__(self):
    self.image = ''
    self.animator = animator(self)
    self.x = 0
    self.y = 0
    self.position = (0, 0)
    self._height = 0
    self._width = 0
  def new(self, image: str, x: int, y: int, screen: screen):
    imagel = image.split('\n')
    self._screen = screen
    self.parent = screen
    self.image = imagel
    self.animator = animator(self)
    self.x = x
    self.y = y
    self.position = (x, y)
    self._height = len(imagel)
    lines = []
    for line in imagel:
      lines.append(len(line))
    self._width = max(lines)
    screen.objects.append(self)
  def rect(self, width: int, height: int, x: int, y: int, screen: screen):
    stri = ''
    for _ in range(width):
      stri = f'{stri}█'
    for _ in range(height-1):
      temp = ''
      for _ in range(width):
        temp = f'{temp}█'
      stri = f'{stri}\n{temp}'
    strib = stri.split('\n')
    self._screen = screen
    self.parent = screen
    self.image = strib
    self.animator = animator(self)
    self.x = x
    self.y = y
    self.position = (x, y)
    self._height = height
    self._width = width
    screen.objects.append(self)
  def move(self, vector: tuple):
    self.x += vector[0]
    self.y += vector[1]
  def animate(self, animation: list, delay=0, loop=True):
    for i, v in enumerate(animation):
      animation[i] = v.split('\n')
    self.animator.animation.frames = animation
    self.animator.animation.delay = delay
    self.animator.animation.loop = loop
  def update(self):
    if self.animator.animation != [self.image]:
      self.animator.update()
      if isinstance(self.parent, enemy) and self.parent.damage > 0:
        for i in self._screen.objects:
          if isinstance(i, player) and istouching(self, i.object):
            i.health -= self.parent.damage
  def center(self, offset=(0, 0)):
    self.x = (self._screen.center[0] - self._width // 2) + offset[0]
    self.y = (self._screen.center[1] - self._height // 2) + offset[1]
  def delete(self):
    for i, v in enumerate(self._screen.objects):
      if v == self:
        self._screen.objects.pop(i)
    del self.parent
    del self.animator.animation
    del self.animator

class player:
  def __init__(self, object: object, health: int):
    self.object = object
    self.health = health
    object.parent = self
  def hit(self, amount: int):
    self.health -= amount
    return self.health

class enemy:
  def __init__(self, object: object, health: int, damage: int):
    self.object = object
    self.health = health
    self.damage = damage
    object.parent = self

def ml(text):
  n = 75
  li = [f'{text[i:i+n]}-' for i in range(0, len(text), n)]
  li[-1] = li[-1][:-1]
  return '\n'.join(li)

def istouching(a: object, b: object):
  width1, height1, x1, y1 = a._width, a._height, a.x, a.y
  width2, height2, x2, y2 = b._width, b._height, b.x, b.y
  left1 = x1
  right1 = x1 + width1
  top1 = y1
  bottom1 = y1 + height1
  left2 = x2
  right2 = x2 + width2
  top2 = y2
  bottom2 = y2 + height2
  touching = True
  if bottom1 < top2 or top1 > bottom2 or right1 < left2 or left1 > right2:
      touching = False
  return touching

def FindFirstAncestorWhichIsA(object, objtype: str):
  if type(object).__name__ == objtype:
      return object
  elif hasattr(object, 'parent') and object.parent is not None:
      return FindFirstAncestorWhichIsA(object.parent, objtype)
  else:
      return None

def wrap(text, index):
  newtext = ''
  for i, v in enumerate(text):
    if i % index == 0:
      newtext = f'{newtext}\n{v}'
    else:
      newtext = f'{newtext}{v}'
  return newtext
