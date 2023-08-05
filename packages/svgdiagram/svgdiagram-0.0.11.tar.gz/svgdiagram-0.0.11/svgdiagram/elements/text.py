from .svg_element import SvgElement


_HORIZONTAL_ALIGNMENT_MAP = {
    "left": "start",
    "center": "middle",
    "right": "end",
}

_VERTICAL_ALIGNMENT_MAP = {
    "top": "hanging",
    "center": "central",
    "bottom": "text-top"
}


class Text(SvgElement):
    def __init__(
        self,
        x, y, text,
        horizontal_alignment="center",
        vertical_alignment="center",
        font_family="arial",
        font_size=16.0,
        font_weight="normal",
        fill=None
    ) -> None:
        self.x = x
        self.y = y

        assert horizontal_alignment in _HORIZONTAL_ALIGNMENT_MAP
        self.horizontal_alignment = horizontal_alignment
        assert vertical_alignment in _VERTICAL_ALIGNMENT_MAP
        self.vertical_alignment = vertical_alignment

        self.font_family = font_family
        self.font_size = font_size
        self.font_weight = font_weight

        self.fill = fill

        super().__init__('text', children=text)

    @property
    def text(self):
        return self.children[0]

    @property
    def bounds(self):
        height = self.font_size
        approximated_width = self.font_size * len(self.text) * 0.6

        if self.horizontal_alignment == "left":
            xmin = self.x
        elif self.horizontal_alignment == "right":
            xmin = self.x - approximated_width
        else:
            xmin = self.x - approximated_width / 2.0
        xmax = xmin + approximated_width

        if self.vertical_alignment == "bottom":
            ymin = self.y - height
        elif self.vertical_alignment == "top":
            ymin = self.y
        else:
            ymin = self.y - height/2
        ymax = ymin + height

        return [xmin, xmax, ymin, ymax]

    def _render(self, doc, tag, text, debug):
        self.attributes.update({
            "x": self.x,
            "y": self.y,
            "text-anchor": _HORIZONTAL_ALIGNMENT_MAP[self.horizontal_alignment],
            "dominant-baseline": _VERTICAL_ALIGNMENT_MAP[self.vertical_alignment],
            "font-family": self.font_family,
            "font-size": self.font_size,
            "font-weight": self.font_weight,
        })
        if self.fill:
            self.attributes["fill"] = self.fill

        return super()._render(doc, tag, text, debug)
