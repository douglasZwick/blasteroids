import pygame
from logger import log_state

from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS


def main():
  print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
  print(f"Screen width: {SCREEN_WIDTH}")
  print(f"Screen height: {SCREEN_HEIGHT}")

  pygame.init()

  clock = pygame.time.Clock()
  dt = 0
  
  updatable = pygame.sprite.Group()
  drawable = pygame.sprite.Group()
  Player.containers = (updatable, drawable)
  
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  center_x, center_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
  player = Player(center_x, center_y)

  while True:
    log_state()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
    
    updatable.update(dt)
      
    screen.fill("black")

    for item in drawable:
      item.draw(screen)

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) / 1000.0


if __name__ == "__main__":
  main()
