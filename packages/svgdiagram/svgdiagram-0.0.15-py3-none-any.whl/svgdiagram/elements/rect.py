from .svg_element import SvgElement


class Rect(SvgElement):
    def __init__(
        self,
        x, y,
        width, height,
        rx=None, ry=None,
        stroke="black", stroke_width_px=1,
        fill="white",
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rx = rx
        self.ry = ry

        self.stroke = stroke
        self.stroke_width_px = stroke_width_px
        self.fill = fill

        super().__init__('rect')

    @property
    def bounds(self):
        return [
            self.x-self.stroke_width_px/2.0,
            self.x+self.stroke_width_px/2.0+self.width,
            self.y-self.stroke_width_px/2.0,
            self.y+self.stroke_width_px/2.0+self.height,
        ]

    def _render(self, doc, tag, text, debug):
        self.attributes.update({
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "stroke": self.stroke,
            "stroke-width": f"{self.stroke_width_px}px",
            "fill": self.fill,
        })

        if self.rx:
            self.attributes["rx"] = self.rx
        if self.ry:
            self.attributes["ry"] = self.ry

        return super()._render(doc, tag, text, debug)

    @classmethod
    def midpoint_round_rect(
        cls,
        mid_x, mid_y,
        width, height,
        radius,
        stroke="black", stroke_width_px=1,
        fill="white",
    ):
        return Rect(
            x=mid_x - width/2,
            y=mid_y - height/2,
            width=width,
            height=height,
            rx=radius,
            ry=radius,
            stroke=stroke,
            stroke_width_px=stroke_width_px,
            fill=fill,
        )
