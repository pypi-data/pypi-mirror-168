from .svg_element import SvgElement, INF_CON
from yattag import Doc, indent
import cairosvg


class Svg(SvgElement):
    def __init__(self, children=None) -> None:
        super().__init__(
            'svg',
            attributes={
                "xmlns": "http://www.w3.org/2000/svg",
            },
            children=children,
        )

    @property
    def bounds(self):
        if not self.children:
            return [0, 0, 0, 0]

        all_bounds = list(map(lambda x: x.bounds, self.children))
        all_bounds = list(filter(lambda x: x, all_bounds))

        if not all_bounds:
            return [0, 0, 0, 0]

        [xmin, xmax, ymin, ymax] = zip(*all_bounds)

        xmin = min(xmin)
        xmax = max(xmax)
        ymin = min(ymin)
        ymax = max(ymax)

        return [xmin, xmax, ymin, ymax]

    def _render(self, doc, tag, text, debug):
        [xmin, xmax, ymin, ymax] = self.bounds
        width = xmax-xmin
        height = ymax-ymin

        self.attributes.update({
            "width": width,
            "height": height,
            "viewBox": f"{xmin} {ymin} {width} {height}",
        })

        return super()._render(doc, tag, text, debug)

    def create_svg_text(self, debug=False, indent_count=None):
        doc, tag, text = Doc().tagtext()

        self._layout(-INF_CON, INF_CON, -INF_CON, INF_CON)
        self._render(doc, tag, text, debug)

        svg_text = doc.getvalue()
        if indent_count:
            svg_text = indent(svg_text, ' '*indent_count)
        return svg_text

    def write_svg(self, filename, debug=False, indent_count=None):
        svg_text = self.create_svg_text(
            debug=debug,
            indent_count=indent_count,
        )

        with open(filename, 'w') as f:
            f.write(svg_text)

    def write_png(self, filename):
        svg_text = self.create_svg_text()
        cairosvg.svg2png(svg_text, write_to=filename)

    def write_eps(self, filename):
        svg_text = self.create_svg_text()
        cairosvg.svg2eps(svg_text, write_to=filename)

    def write_ps(self, filename):
        svg_text = self.create_svg_text()
        cairosvg.svg2ps(svg_text, write_to=filename)
