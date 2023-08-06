from .svg_element import SvgElement


class Transform:
    """basic transformation class"""

    @property
    def transform_text(self):
        raise NotImplementedError()

    def apply_transform_to_bounds(self, xmin, xmax, ymin, ymax):
        raise NotImplementedError


class TranslateTransform(Transform):
    def __init__(self, dx, dy):
        super().__init__()

        self.dx = dx
        self.dy = dy

    @property
    def transform_text(self):
        return f"translate({self.dx}, {self.dy})"

    def apply_transform_to_bounds(self, xmin, xmax, ymin, ymax):
        return [
            xmin + self.dx,
            xmax + self.dx,
            ymin + self.dy,
            ymax + self.dy,
        ]


class Group(SvgElement):
    def __init__(self, children=None, transforms=None) -> None:
        super().__init__('g', children=children)

        if isinstance(transforms, Transform):
            transforms = [transforms]

        self.transforms = transforms if transforms else []

    @property
    def bounds(self):
        if not self.children:
            return None

        all_bounds = list(map(lambda x: x.bounds, self.children))
        all_bounds = list(filter(lambda x: x, all_bounds))

        if not all_bounds:
            return None

        [xmin, xmax, ymin, ymax] = zip(*all_bounds)

        xmin = min(xmin)
        xmax = max(xmax)
        ymin = min(ymin)
        ymax = max(ymax)

        for transform in self.transforms:
            [xmin, xmax, ymin, ymax] = transform.apply_transform_to_bounds(
                xmin, xmax, ymin, ymax,
            )

        return [xmin, xmax, ymin, ymax]

    def _render(self, doc, tag, text, debug):
        if self.transforms:
            self.attributes["transform"] = " ".join(
                map(lambda x: x.transform_text, self.transforms))
        return super()._render(doc, tag, text, debug)
