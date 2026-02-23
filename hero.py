import pygame
from circleshape import CircleShape
from bullet import Bullet
from constants import (
  HERO_RADIUS,
  HERO_TURN_SPEED,
  HERO_SPEED,
  HERO_SHOOT_SPEED,
  MAX_BULLETS,
  LINE_WIDTH,
)


class Hero(CircleShape):
  rotation: float
  bullet_count: int
  shot_requested: bool

  def __init__(self, x: float, y: float) -> None:
    super().__init__(x, y, HERO_RADIUS)
    self.rotation = 0
    self.bullet_count = 0
    self.shot_requested = False

  def get_forward(self) -> pygame.Vector2:
    return pygame.Vector2(0, 1).rotate(self.rotation)

  def get_mesh_points(self) -> list[pygame.Vector2]:
    forward = self.get_forward()
    right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
    a = self.position + forward * self.radius
    b = self.position - forward * self.radius - right
    c = self.position - forward * self.radius + right
    return [a, b, c]
  
  def draw(self, surface: pygame.Surface) -> None:
    pygame.draw.polygon(surface, "white", self.get_mesh_points(), LINE_WIDTH)

  def rotate(self, dir: float, dt: float) -> None:
    d_rot = HERO_TURN_SPEED * dir * dt
    self.rotation += d_rot

  def shoot_key_pressed(self) -> None:
    self.shot_requested = True

  def update(self, dt: float) -> None:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      self.rotate(+1, dt)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      self.rotate(-1, dt)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      self.move(+1, dt)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      self.move(-1, dt)

    if self.shot_requested:
      self.attempt_shoot()
    self.shot_requested = False

  def move(self, dir: float, dt: float) -> None:
    forward = self.get_forward()
    velocity = forward * dir * HERO_SPEED
    self.position += velocity * dt

  def can_shoot(self) -> bool:
    return self.bullet_count < MAX_BULLETS

  def attempt_shoot(self) -> None:
    if self.can_shoot():
      self.shoot()

  def shoot(self) -> None:
    bullet = Bullet(self.position.x, self.position.y, self.bullet_died)
    self.bullet_created()

    bullet_speed = HERO_SHOOT_SPEED

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      bullet_speed += HERO_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
      bullet_speed -= HERO_SPEED

    bullet.velocity = self.get_forward() * bullet_speed

  def bullet_created(self) -> None:
    self.bullet_count += 1

  def bullet_died(self) -> None:
    self.bullet_count -= 1
