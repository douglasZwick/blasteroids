import pygame
import json
from pathlib import Path
from constants import VECTOR_FONT_POINT_WIDTH

VectorPath = list[list[float]]
GlyphData = dict[str, list[VectorPath]]
VectorStroke = tuple[pygame.Vector2, pygame.Vector2]
VectorGlyph = list[VectorStroke]


class VectorFont:
  name: str
  glyphs: dict[str, VectorGlyph]

  def __init__(self, name: str, path: str) -> None:
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
