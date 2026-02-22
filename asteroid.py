import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH


class Asteroid(CircleShape):
  def __init__(self, x: float, y: float, radius: float):
    super().__init__(x, y, radius)

  def draw(self, surface: pygame.Surface):
    pygame.draw.circle(surface, "white", self.position, self.radius, LINE_WIDTH)

  def update(self, dt):
    self.position += self.velocity * dt
