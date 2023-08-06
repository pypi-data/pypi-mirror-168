from svgdiagram.elements.group import Group
from svgdiagram.elements.rect import Rect
from svgdiagram.elements.text import Text


class Task(Group):
    def __init__(
        self,
        x_start, x_end, y, height,
        text="", text_horizontal_align="center", text_padding=10,
        text_font_family="arial", text_font_size=16.0, text_font_weight="normal", text_color="black",
        progess=0,
        radius=3,
        stroke="black", stroke_width_px=1,
        fill="white", fill_progress="grey",
    ):
        width = x_end - x_start

        children = []

        if progess < 1:
            background_rect = Rect(
                x_start, y - height/2.0, width, height,
                radius, radius,
                stroke="transparent", stroke_width_px=1, fill=fill,
            )
            children.append(background_rect)

        if progess > 0:
            progress_rect = Rect(
                x_start, y - height/2.0, width * progess, height,
                radius, radius,
                stroke="transparent", stroke_width_px=1, fill=fill_progress,
            )
            children.append(progress_rect)

        if stroke != "transparent" and stroke_width_px > 0:
            outline_rect = Rect(
                x_start, y - height/2.0, width, height,
                radius, radius,
                stroke=stroke, stroke_width_px=stroke_width_px, fill="transparent",
            )
            children.append(outline_rect)

        if text:
            if text_horizontal_align == "left":
                x = x_start + text_padding
            elif text_horizontal_align == "right":
                x = x_end - text_padding
            elif text_horizontal_align == "center":
                x = (x_start + x_end) / 2.0

            children.append(Text(
                x=x, y=y, text=text,
                horizontal_alignment=text_horizontal_align,
                font_family=text_font_family,
                font_size=text_font_size,
                font_weight=text_font_weight,
                fill=text_color,
            ))

        super().__init__(children)
