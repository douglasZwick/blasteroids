class GameState:
  name: str

  def __init__(self, name: str) -> None:
    self.name = name

  def enter(self) -> None:
    raise NotImplementedError()
  
  def update(self, dt: float) -> None:
    raise NotImplementedError()
  
  def exit(self) -> None:
    raise NotImplementedError()


class GameStateManager:
  states: dict[str, GameState]
  curr_state: GameState

  def __init__(self, starting_state_name: str) -> None:
    self.switch(starting_state_name)

  def add_state(self, state_name: str, state: GameState) -> None:
    self.states[state_name] = state

  def get_state(self, state_name: str) -> GameState:
    return self.states[state_name]
  
  def switch(self, state_name: str) -> None:
    self.curr_state.exit()
    self.curr_state = self.get_state(state_name)
    self.curr_state.enter()
