from .svg_element import SvgElement


class Path(SvgElement):
    def __init__(self, points, close=False, stroke='black', stroke_width_px=1, fill='transparent'):

        self.points = points
        self.close = close

        self.stroke = stroke
        self.stroke_width_px = stroke_width_px
        self.fill = fill

        super().__init__('path')

    @property
    def bounds(self):
        [x, y] = zip(*self.points)

        xmin = min(x)-self.stroke_width_px
        xmax = max(x)+self.stroke_width_px
        ymin = min(y)-self.stroke_width_px
        ymax = max(y)+self.stroke_width_px

        return [xmin, xmax, ymin, ymax]

    def _calc_poly_text_d(self):
        d = f'M {self.points[0][0]} {self.points[0][1]}'

        for p in self.points[1:]:
            d += f' L {p[0]} {p[1]}'

        if self.close:
            d += " Z"

        return d

    def _render(self, doc, tag, text, debug):
        self.attributes.update({
            "d": self._calc_poly_text_d(),
            "stroke": self.stroke,
            "stroke-width": f"{self.stroke_width_px}px",
            "fill": self.fill,
        })

        return super()._render(doc, tag, text, debug)
