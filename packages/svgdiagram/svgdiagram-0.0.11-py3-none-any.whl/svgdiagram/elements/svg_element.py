INF_CON = float('inf')


class SvgElement:
    def __init__(self, tag_name, attributes=None, children=None) -> None:
        self.tag_name = tag_name
        self.attributes = attributes if attributes else {}

        if not isinstance(children, list) and children:
            children = [children]

        self.children = children if children else []

    @property
    def bounds(self):
        """Bounds provided by [xmin, xmax, ymin, ymax]"""
        raise NotImplementedError

    def _render(self, doc, tag, text, debug):
        kv_attribs = [(k, v) for k, v in self.attributes.items()]

        with tag(self.tag_name, *kv_attribs):
            for child in self.children:
                if isinstance(child, str):
                    text(child)
                else:
                    child._render(doc, tag, text, debug)

    def _layout(self, x_con_min, x_con_max, y_con_min, y_con_max):
        """layout before writing svg file

        By default
        - layouting is unconstraint
        - every element layouts itself

        Elements may
        - set position child elements
        - request width and height of the child elements
        - apply constraints to the with and height of child elements
        """
        assert x_con_min == -INF_CON
        assert x_con_max == INF_CON
        assert y_con_min == -INF_CON
        assert y_con_max == INF_CON

        for child in self.children:
            if not isinstance(child, str):
                child._layout(x_con_min, x_con_max, y_con_min, y_con_max)

    def append_child(self, child):
        self.children.append(child)
