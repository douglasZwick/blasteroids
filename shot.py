import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS


class Shot(CircleShape):
  def __init__(self, x: float, y: float):
    super().__init__(x, y, SHOT_RADIUS)

  def draw(self, surface: pygame.Surface):
    pygame.draw.circle(surface, "white", self.position, self.radius, LINE_WIDTH)

  def update(self, dt: float):
    self.position += self.velocity * dt
