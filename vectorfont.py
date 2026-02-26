import pygame
import pygame.gfxdraw
import json
from typing import Callable, TypedDict, cast
from pathlib import Path
from constants import TEXT_LINE_WIDTH

Point = list[float]
VectorPath = list[Point]

class JsonGlyph(TypedDict, total=False):
  open: list[VectorPath]
  closed: list[VectorPath]
  point: list[Point]

JsonFont = dict[str, JsonGlyph]

VectorStroke = tuple[pygame.Vector2, pygame.Vector2]
VectorGlyph = list[VectorStroke]

DEFAULT_SPACING = pygame.Vector2(8, 8)
DEFAULT_TEXT_COLOR = pygame.Color(255, 255, 255)


class TextStyle:
  size: float   # height in pixels
  aspect: float
  weight: int
  oblique: float
  spacing: pygame.Vector2
  color: pygame.Color

  def __init__(self, size: float, aspect: float, weight: int, oblique: float,
               spacing: pygame.Vector2, color: pygame.Color) -> None:
    self.size = size
    self.aspect = aspect
    self.weight = weight
    self.oblique = oblique
    self.spacing = spacing
    self.color = color

  def get_size_vector(self) -> pygame.Vector2:
    return pygame.Vector2(self.size * self.aspect, self.size)

  def oblique_shift(self, y: float) -> float:
    return (self.oblique * self.aspect) * (1.0 - y)


class VectorFont:
  surface: pygame.Surface
  name: str
  glyphs: dict[str, VectorGlyph]
  default_style: TextStyle

  def __init__(self, surface: pygame.Surface, name: str, path: str) -> None:
    self.surface = surface
    self.name = name
    self.glyphs = {}
    self.default_style = TextStyle(size=80, aspect=1, weight=TEXT_LINE_WIDTH, oblique=1,
                                   spacing=DEFAULT_SPACING,
                                   color=DEFAULT_TEXT_COLOR)

    print(f"Creating font {name} from path {path}...")
    data_path = Path(__file__).with_name(path)
    # Intentionally not using a try-catch here. If something fails with loading,
    # then the UI will be broken one way or another, so let's just let the exception go uncaught
    with open(data_path, "r") as font_file:
      json_data = cast(JsonFont, json.load(font_file))
      count = self.create_glyphs(json_data)
      print(f"  Successfully created {count} glyphs")

  def add(self, key: str, value: VectorGlyph) -> None:
    self.glyphs[key] = value
  
  def create_glyphs(self, data: JsonFont) -> int:
    count = 0

    for key, json_glyph in data.items():
      vector_glyph = self.create_glyph(json_glyph)
      self.add(key, vector_glyph)
      count += 1

    return count

  def create_glyph(self, data: JsonGlyph) -> VectorGlyph:
    glyph: VectorGlyph = []
    open_paths = data.get("open", [])
    closed_paths = data.get("closed", [])
    points = data.get("point", [])

    y_flip: Callable[[Point], pygame.Vector2] = lambda p: pygame.Vector2(p[0], 1.0 - p[1])

    for path in open_paths:
      for i in range(0, len(path) - 1):
        stroke = y_flip(path[i]), y_flip(path[i + 1])
        glyph.append(stroke)
    for path in closed_paths:
      for i in range(0, len(path) - 1):
        stroke = y_flip(path[i]), y_flip(path[i + 1])
        glyph.append(stroke)
      stroke = y_flip(path[-1]), y_flip(path[0])
      glyph.append(stroke)
    for point in points:
      point = y_flip(point)
      glyph.append((point, point))
    
    return glyph
  
  def draw_char(self, char: str, pos: pygame.Vector2,
                _style: TextStyle | None = None) -> None:
    self.draw_glyph(self.glyphs[char], pos, _style)
  
  def draw_glyph(self, glyph: VectorGlyph, pos: pygame.Vector2,
                 _style: TextStyle | None = None) -> None:
    style: TextStyle = self.default_style if _style is None else _style
    size = style.get_size_vector()
    for stroke in glyph:
      p0, p1 = stroke[0].copy(), stroke[1].copy()
      p0.x += style.oblique_shift(p0.y)
      p1.x += style.oblique_shift(p1.y)
      p0, p1 = p0.elementwise() * size, p1.elementwise() * size
      p0, p1 = p0 + pos, p1 + pos
      if p0 == p1:
        pygame.draw.circle(self.surface, style.color, p0, style.weight)
      else:
        pygame.draw.line(self.surface, style.color, p0, p1, style.weight)
        # pygame.draw.circle(self.surface, style.color, p0, style.weight)
        # pygame.draw.circle(self.surface, style.color, p1, style.weight)

  def text(self, text: str, pos: pygame.Vector2,
           _style: TextStyle | None = None) -> None:
    style: TextStyle = self.default_style if _style is None else _style
    spacing = style.get_size_vector().x + style.spacing.x
    for i, char in enumerate(text):
      if char == " " or not char.isprintable():
        continue
      glyph_pos = pos + pygame.Vector2(i * spacing, 0)
      self.draw_char(char, glyph_pos, _style)

  def demo(self, _style: TextStyle | None = None) -> None:
    style: TextStyle = self.default_style if _style is None else _style
    origin = pygame.Vector2(30, 30)
    line_height = style.get_size_vector().y + style.spacing.y
    start = 32
    end = 128
    step = 16
    strings = []
    for i in range(start, end, step):
      line = []
      for code in range(i, i + step):
        line.append(chr(code))
      strings.append("".join(line))
    for i, string in enumerate(strings):
      pos = origin + pygame.Vector2(0, i * line_height)
      self.text(string, pos)
