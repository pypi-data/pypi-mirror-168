from dataclasses import dataclass
from svgdiagram.elements.rect import Rect
from svgdiagram.elements.text import Text
from svgdiagram.elements.group import Group


@dataclass
class TextLine:
    text: str
    font_size: float = 16.0
    font_family: str = "arial"
    font_weight: str = 'normal'


class MultiLineRect(Group):
    def __init__(
        self,
        x, y,
        width,
        padding=5, line_gap=2,
        radius=None,
        text_lines=None,
        stroke="black", stroke_width_px=1,
        fill="white",
    ):
        height = padding
        children = []

        for line in text_lines:

            children.append(Text(
                x + width / 2, y+height + line.font_size/2, line.text,
                horizontal_alignment="center",
                vertical_alignment="center",
                font_family=line.font_family,
                font_size=line.font_size,
                font_weight=line.font_weight
            ))
            height += line.font_size + line_gap

        height += padding

        super().__init__(
            children=[Rect(
                x, y,
                width, height,
                radius, radius,
                stroke=stroke,
                stroke_width_px=stroke_width_px,
                fill=fill,
            )] + children)
