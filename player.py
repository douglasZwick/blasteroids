import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, LINE_WIDTH


class Player(CircleShape):
  rotation: float

  def __init__(self, x, y):
    super().__init__(x, y, PLAYER_RADIUS)
    self.rotation = 0

  def get_forward(self):
    return pygame.Vector2(0, 1).rotate(self.rotation)

  def triangle(self):
    forward = self.get_forward()
    right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
    a = self.position + forward * self.radius
    b = self.position - forward * self.radius - right
    c = self.position - forward * self.radius + right
    return [a, b, c]
  
  def draw(self, screen):
    pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

  def rotate(self, dir, dt):
    d_rot = PLAYER_TURN_SPEED * dir * dt
    self.rotation += d_rot

  def update(self, dt):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
      self.rotate(+1, dt)
    if keys[pygame.K_a]:
      self.rotate(-1, dt)
    if keys[pygame.K_w]:
      self.move(+1, dt)
    if keys[pygame.K_s]:
      self.move(-1, dt)

  def move(self, dir, dt):
    forward = self.get_forward()
    velocity = forward * dir * PLAYER_SPEED
    self.position += velocity * dt
