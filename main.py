import sys
import pygame
from logger import log_state, log_event

from player import Player
from asteroid import Asteroid
from shot import Shot
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

  font = VectorFont("main", "mainfont.json")
  
  updatables = pygame.sprite.Group()
  drawables = pygame.sprite.Group()
  asteroids = pygame.sprite.Group()
  shots = pygame.sprite.Group()

  Player.containers = (updatables, drawables)
  Asteroid.containers = (updatables, drawables, asteroids)
  AsteroidField.containers = (updatables, )
  Shot.containers = (updatables, drawables, shots)
  
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  _ = AsteroidField() # Curiously, we don't need to use this object...!

  center_x, center_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
  player = Player(center_x, center_y)

  while True:
    log_state()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
      return
    
    updatables.update(dt)

    for asteroid in asteroids:
      player_collision_check(asteroid, player)
      
      for shot in shots:
        shot_collision_check(asteroid, shot)
      
    screen.fill("black")

    for item in drawables:
      item.draw(screen)

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) / 1000.0

def player_collision_check(asteroid: Asteroid, player: Player):
  if asteroid.collides_with(player):
    player_collision_detected()

def player_collision_detected():
  log_event("player_hit")
  print("Game over!")
  sys.exit()

def shot_collision_check(asteroid: Asteroid, shot: Shot):
  if asteroid.collides_with(shot):
    shot_collision_detected(asteroid, shot)

def shot_collision_detected(asteroid: Asteroid, shot: Shot):
  log_event("asteroid_shot")
  asteroid.take_damage()
  shot.kill()


if __name__ == "__main__":
  main()
