import pygame
import json
import string
from pathlib import Path
from constants import VECTOR_FONT_POINT_WIDTH, LINE_WIDTH

VectorPath = list[list[float]]
GlyphData = dict[str, list[VectorPath]]
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
        json_data: dict[str, GlyphData] = json.load(font_file)
        print(f"Creating glyphs from font file {path}:")
        count = self.create_glyphs(json_data)
        print(f"Successfully created {count} glyphs")
    except Exception as ex:
      print(f"Error reading font file {path}: {ex}")

    # for _, glyph in self.glyphs.items():

  def add(self, key: str, value: VectorGlyph) -> None:
    self.glyphs[key] = value
  
  def create_glyphs(self, data: dict[str, GlyphData]) -> int:
    count = 0

    for key, glyph_data in data.items():
      print(f"  Creating glyph '{key}'...")
      glyph = self.create_glyph(glyph_data)
      self.add(key, glyph)
      count += 1

    return count

  def create_glyph(self, data: GlyphData) -> VectorGlyph:
    glyph: VectorGlyph = []
    open_paths = data.get("open", [])
    closed_paths = data.get("closed", [])
    points = data.get("point", [])

    for path in open_paths:
      for i in range(0, len(path) - 1):
        stroke = (pygame.Vector2(path[i]), pygame.Vector2(path[i + 1]))
        glyph.append(stroke)
    for path in closed_paths:
      for i in range(0, len(path) - 1):
        stroke = (pygame.Vector2(path[i]), pygame.Vector2(path[i + 1]))
        glyph.append(stroke)
      closing_stroke = (pygame.Vector2(path[-1]), pygame.Vector2(path[0]))
      glyph.append(closing_stroke)
    for point in points:
      for pair in point:
        center = pygame.Vector2(pair)
        l, r = center.copy(), center.copy()
        l.x -= VECTOR_FONT_POINT_WIDTH
        r.x += VECTOR_FONT_POINT_WIDTH
        glyph.append((l, r))
    
    return glyph
  
  def draw_char(self, char: str, pos: pygame.Vector2) -> None:
    self.draw_glyph(self.glyphs[char], pos)
  
  def draw_glyph(self, glyph: VectorGlyph, pos: pygame.Vector2) -> None:
    size = pygame.Vector2(44, -88)
    for stroke in glyph:
      p0, p1 = stroke
      start = p0.elementwise() * size + pos
      end = p1.elementwise() * size + pos
      pygame.draw.line(self.surface, "white", start, end, LINE_WIDTH)

  def text(self, text: str, pos: pygame.Vector2) -> None:
    spacing = 48
    for i, char in enumerate(text):
      if char not in string.ascii_uppercase:
        continue
      glyph_pos = pos + pygame.Vector2(i * spacing, 0)
      self.draw_char(char, glyph_pos)
