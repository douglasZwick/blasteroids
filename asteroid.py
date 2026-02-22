import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_SPEED_SCALE_FACTOR


class Asteroid(CircleShape):
  size: int

  def __init__(self, x: float, y: float, size: int):
    super().__init__(x, y, size * ASTEROID_MIN_RADIUS)
    self.size = size

  def draw(self, surface: pygame.Surface):
    pygame.draw.circle(surface, "white", self.position, self.radius, LINE_WIDTH)

  def update(self, dt):
    self.position += self.velocity * dt

  def take_damage(self):
    if self.size > 1:
      self.split()
    else:
      self.die()

  def die(self):
    log_event("asteroid_died")
    self.kill()

  def split(self):
    log_event("asteroid_split")
    self.kill()

    x, y = self.position
    angle = random.uniform(20, 50)
    l_vel = self.velocity.rotate(angle) * ASTEROID_SPEED_SCALE_FACTOR
    r_vel = self.velocity.rotate(-angle) * ASTEROID_SPEED_SCALE_FACTOR
    size = self.size - 1
    l_child = Asteroid(x, y, size)
    r_child = Asteroid(x, y, size)
    l_child.velocity = l_vel
    r_child.velocity = r_vel
