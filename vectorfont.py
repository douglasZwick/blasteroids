import pygame
import json
from typing import Callable, TypedDict, cast
from pathlib import Path
from constants import VECTOR_FONT_POINT_WIDTH, LINE_WIDTH

Point = list[float]
VectorPath = list[Point]

class JsonGlyph(TypedDict, total=False):
  open: list[VectorPath]
  closed: list[VectorPath]
  point: list[Point]

JsonFont = dict[str, JsonGlyph]

VectorStroke = tuple[pygame.Vector2, pygame.Vector2]
VectorGlyph = list[VectorStroke]


class VectorFont:
  surface: pygame.Surface
  name: str
  glyphs: dict[str, VectorGlyph]

  def __init__(self, surface: pygame.Surface, name: str, path: str) -> None:
    self.surface = surface
    self.name = name
    self.glyphs = {}

    data_path = Path(__file__).with_name("mainfont.json")
    try:
      with open(data_path, "r") as font_file:
        json_data = cast(JsonFont, json.load(font_file))
        print(f"Creating glyphs from font file {path}:")
        count = self.create_glyphs(json_data)
        print(f"Successfully created {count} glyphs")
    except Exception as ex:
      print(f"Error reading font file {path}: {ex}")
      raise ex

    # for _, glyph in self.glyphs.items():

  def add(self, key: str, value: VectorGlyph) -> None:
    self.glyphs[key] = value
  
  def create_glyphs(self, data: JsonFont) -> int:
    count = 0

    for key, json_glyph in data.items():
      print(f"  Creating glyph '{key}'...")
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
      center = y_flip(point)
      l, r = center.copy(), center.copy()
      l.x -= VECTOR_FONT_POINT_WIDTH
      r.x += VECTOR_FONT_POINT_WIDTH
      glyph.append((l, r))
    
    return glyph
  
  def draw_char(self, char: str, pos: pygame.Vector2) -> None:
    self.draw_glyph(self.glyphs[char], pos)
  
  def draw_glyph(self, glyph: VectorGlyph, pos: pygame.Vector2) -> None:
    size = pygame.Vector2(44, 88)
    for stroke in glyph:
      p0, p1 = stroke
      start, end = p0.elementwise() * size, p1.elementwise() * size
      pygame.draw.line(self.surface, "white", p0, p1, LINE_WIDTH)

  def text(self, text: str, pos: pygame.Vector2) -> None:
    spacing = 48
    for i, char in enumerate(text):
      if char == " " or not char.isprintable():
        continue
      glyph_pos = pos + pygame.Vector2(i * spacing, 0)
      self.draw_char(char, glyph_pos)

  def demo(self) -> None:
    origin = pygame.Vector2(30, 30)
    line_height = 96
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
