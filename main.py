import sys
import pygame
import logger

from gamestatemanager import GameStateManager
from hero import Hero
from asteroid import Asteroid
from bullet import Bullet
from asteroidfield import AsteroidField
from vectorfont import VectorFont
from constants import (
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  TARGET_FPS,
  LOGGING_ENABLED,
  INITIAL_DT,
)


class Game:
  gsm: GameStateManager

  clock: pygame.time.Clock
  surface: pygame.Surface
  bounds: pygame.Rect
  font: VectorFont

  updatables: pygame.sprite.Group
  drawables: pygame.sprite.Group
  asteroids: pygame.sprite.Group
  bullets: pygame.sprite.Group

  hero: Hero

  logging_enabled: bool

  def __init__(self) -> None:
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    self.clock = pygame.time.Clock()
    self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # TODO: research how to use pygame.OPENGL
    self.bounds = self.surface.get_rect()

    self.gsm = GameStateManager("title")
    self.font = VectorFont(self.surface, "Main", "mainfont.json")
    
    self.updatables = pygame.sprite.Group()
    self.drawables = pygame.sprite.Group()
    self.asteroids = pygame.sprite.Group()
    self.bullets = pygame.sprite.Group()

    Hero.containers = (self.updatables, self.drawables)
    Asteroid.containers = (self.updatables, self.drawables, self.asteroids)
    AsteroidField.containers = (self.updatables, )
    Bullet.containers = (self.updatables, self.drawables, self.bullets)

    _ = AsteroidField()

    c_x, c_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    self.hero = Hero(c_x, c_y)

    self.logging_enabled = LOGGING_ENABLED

  def run(self) -> None:
    dt = INITIAL_DT
    quit_requested = False

    self.surface.fill("black")

    while not quit_requested:
      self.log_state()

      for event in pygame.event.get():
        match event.type:
          case pygame.QUIT:
            quit_requested = True
          case pygame.KEYDOWN:
            match event.key:
              case pygame.K_ESCAPE:
                quit_requested = True
              case pygame.K_SPACE:
                self.hero.shoot_key_pressed()
      
      self.update_game_state(dt)

      # self.font.demo()

      pygame.display.flip()
      dt = self.clock.tick(TARGET_FPS) / 1000.0

    self.shut_down()

  def update_game_state(self, dt: float):
    self.updatables.update(dt)

    for asteroid in self.asteroids:
      self.hero_collision_check(asteroid, self.hero)
      
      for bullet in self.bullets:
        self.bullet_collision_check(asteroid, bullet)

    for bullet in self.bullets:
      self.bullet_bounds_check(self.bounds, bullet)
      
    self.surface.fill("black")

    for item in self.drawables:
      item.draw(self.surface)

  def game_over(self) -> None:
    pass

  def shut_down(self) -> None:
    print("Thank you for playing Wing Commander!")

  def hero_collision_check(self, asteroid: Asteroid, hero: Hero) -> None:
    if asteroid.collides_with(hero):
      self.hero_collision_detected()

  def hero_collision_detected(self) -> None:
    self.log_event("player_hit")
    print("Game over!")
    sys.exit()

  def bullet_collision_check(self, asteroid: Asteroid, bullet: Bullet) -> None:
    if asteroid.collides_with(bullet):
      self.bullet_collision_detected(asteroid, bullet)

  def bullet_collision_detected(self, asteroid: Asteroid, bullet: Bullet) -> None:
    self.log_event("asteroid_shot")
    asteroid.take_damage()
    bullet.die()

  def bullet_bounds_check(self, bounds: pygame.Rect, bullet: Bullet) -> None:
    if not bounds.collidepoint(bullet.position):
      bullet.die()

  def log_state(self) -> None:
    if not self.logging_enabled:
      return
    logger.log_state()

  def log_event(self, event_type: str) -> None:
    if not self.logging_enabled:
      return
    logger.log_event(event_type)


def main():
  game = Game()
  game.run()


if __name__ == "__main__":
  main()
