import pygame
from typing import ClassVar


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
  containers: ClassVar[tuple] = ()
  position: pygame.Vector2
  velocity: pygame.Vector2
  radius: float

  def __init__(self, x: float, y: float, radius: float):
    # we will be using this later
    if hasattr(self, "containers"):
      super().__init__(self.containers) # type: ignore[arg-type]
    else:
      super().__init__()

    self.position = pygame.Vector2(x, y)
    self.velocity = pygame.Vector2(0, 0)
    self.radius = radius

  def draw(self, surface: pygame.Surface):
    # must override
    pass

  def update(self, dt: float):
    # must override
    pass

  def collides_with(self, other: "CircleShape") -> bool:
    r_sum = self.radius + other.radius
    distance_squared = self.position.distance_squared_to(other.position)
    return distance_squared <= r_sum * r_sum
