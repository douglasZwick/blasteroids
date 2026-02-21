import pygame
from typing import ClassVar


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
  containers: ClassVar[tuple] = ()
  position: pygame.Vector2
  velocity: pygame.Vector2
  radius: float

  def __init__(self, x, y, radius):
    # we will be using this later
    if hasattr(self, "containers"):
      super().__init__(self.containers) # type: ignore[arg-type]
    else:
      super().__init__()

    self.position = pygame.Vector2(x, y)
    self.velocity = pygame.Vector2(0, 0)
    self.radius = radius

  def draw(self, screen):
    # must override
    pass

  def update(self, dt):
    # must override
    pass
