from svgdiagram.elements.path import Path


class Milestone(Path):
    def __init__(self, x, y, size=30, stroke="black", stroke_width_px=1, fill="white") -> None:
        super().__init__(
            points=[
                (x-size/2.0, y),
                (x, y-size/2.0),
                (x+size/2.0, y),
                (x, y+size/2.0),
            ],
            stroke=stroke,
            stroke_width_px=stroke_width_px,
            fill=fill,
            close=True
        )
