from gamestatemanager import GameState


class GameOverState(GameState):
  def __init__(self) -> None:
    super().__init__("game_over")
