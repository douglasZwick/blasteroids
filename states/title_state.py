from gamestatemanager import GameState


class TitleState(GameState):
  def __init__(self) -> None:
    super().__init__("title")
