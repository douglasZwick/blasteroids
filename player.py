import pygame
from circleshape import CircleShape
from shot import Shot
from constants import (
  PLAYER_RADIUS,
  PLAYER_TURN_SPEED,
  PLAYER_SPEED,
  PLAYER_SHOOT_SPEED,
  SHOT_COOLDOWN_SECONDS,
  LINE_WIDTH,
)


class Player(CircleShape):
  rotation: float
  shot_cooldown_timer: float

  def __init__(self, x: float, y: float):
    super().__init__(x, y, PLAYER_RADIUS)
    self.rotation = 0
    self.shot_cooldown_timer = 0

  def get_forward(self) -> pygame.Vector2:
    return pygame.Vector2(0, 1).rotate(self.rotation)

  def triangle(self) -> list[pygame.Vector2]:
    forward = self.get_forward()
    right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
    a = self.position + forward * self.radius
    b = self.position - forward * self.radius - right
    c = self.position - forward * self.radius + right
    return [a, b, c]
  
  def draw(self, surface: pygame.Surface):
    pygame.draw.polygon(surface, "white", self.triangle(), LINE_WIDTH)

  def rotate(self, dir: float, dt: float):
    d_rot = PLAYER_TURN_SPEED * dir * dt
    self.rotation += d_rot

  def update(self, dt: float):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      self.rotate(+1, dt)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      self.rotate(-1, dt)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      self.move(+1, dt)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      self.move(-1, dt)
    if keys[pygame.K_SPACE]:
      self.attempt_shoot()

    if self.shot_cooling_down():
      self.shot_cooldown_timer -= dt

  def move(self, dir: float, dt: float):
    forward = self.get_forward()
    velocity = forward * dir * PLAYER_SPEED
    self.position += velocity * dt

  def shot_cooling_down(self) -> bool:
    return self.shot_cooldown_timer > 0.0

  def attempt_shoot(self):
    if not self.shot_cooling_down():
      self.shoot()

  def shoot(self):
    shot = Shot(self.position.x, self.position.y)
    shot_speed = PLAYER_SHOOT_SPEED

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      shot_speed += PLAYER_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      shot_speed -= PLAYER_SPEED

    shot.velocity = self.get_forward() * shot_speed

    self.shot_cooldown_timer = SHOT_COOLDOWN_SECONDS
