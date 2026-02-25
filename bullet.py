import pygame
from typing import Callable
from circleshape import CircleShape
from constants import OBJ_LINE_WIDTH, BULLET_RADIUS, BULLET_LIFESPAN


class Bullet(CircleShape):
  bullet_died: Callable
  lifetime: float

  def __init__(self, x: float, y: float, bullet_died: Callable) -> None:
    super().__init__(x, y, BULLET_RADIUS)
    self.bullet_died = bullet_died
    self.lifetime = 0

  def draw(self, surface: pygame.Surface) -> None:
    pygame.draw.circle(surface, "white", self.position, self.radius, OBJ_LINE_WIDTH)

  def update(self, dt: float) -> None:
    self.position += self.velocity * dt
    self.lifetime += dt
    if self.lifetime >= BULLET_LIFESPAN:
      self.die()

  def die(self) -> None:
    self.bullet_died()
    self.kill()
