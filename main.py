import sys
import pygame
import string
from logger import log_state, log_event

from player import Player
from asteroid import Asteroid
from bullet import Bullet
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS
from vectorfont import VectorFont


def main():
  print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
  print(f"Screen width: {SCREEN_WIDTH}")
  print(f"Screen height: {SCREEN_HEIGHT}")

  pygame.init()

  clock = pygame.time.Clock()
  dt = 0

  surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  bounds = surface.get_rect()

  font = VectorFont(surface, "main", "mainfont.json")
  
  updatables = pygame.sprite.Group()
  drawables = pygame.sprite.Group()
  asteroids = pygame.sprite.Group()
  bullets = pygame.sprite.Group()

  Player.containers = (updatables, drawables)
  Asteroid.containers = (updatables, drawables, asteroids)
  AsteroidField.containers = (updatables, )
  Bullet.containers = (updatables, drawables, bullets)
  
  _ = AsteroidField() # Curiously, we don't need to use this object...!

  center_x, center_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
  player = Player(center_x, center_y)

  while True:
    log_state()

    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          return
        case pygame.KEYDOWN:
          match event.key:
            case pygame.K_ESCAPE:
              return
            case pygame.K_SPACE:
              player.shoot_key_pressed()
    
    updatables.update(dt)

    for asteroid in asteroids:
      player_collision_check(asteroid, player)
      
      for bullet in bullets:
        bullet_collision_check(asteroid, bullet)

    for bullet in bullets:
      bullet_bounds_check(bounds, bullet)
      
    surface.fill("black")

    for item in drawables:
      item.draw(surface)

    font.text(string.ascii_uppercase, pygame.Vector2(15, 100))

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) / 1000.0

def player_collision_check(asteroid: Asteroid, player: Player):
  if asteroid.collides_with(player):
    player_collision_detected()

def player_collision_detected():
  return
  log_event("player_hit")
  print("Game over!")
  sys.exit()

def bullet_collision_check(asteroid: Asteroid, bullet: Bullet):
  if asteroid.collides_with(bullet):
    bullet_collision_detected(asteroid, bullet)

def bullet_collision_detected(asteroid: Asteroid, bullet: Bullet):
  log_event("asteroid_shot")
  asteroid.take_damage()
  bullet.die()

def bullet_bounds_check(bounds: pygame.Rect, bullet: Bullet) -> None:
  if not bounds.collidepoint(bullet.position):
    bullet.die()


if __name__ == "__main__":
  main()
