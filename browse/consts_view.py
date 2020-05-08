from browse.consts_db import TextPositions
import collections


class TextBox:
    def __init__(self, x, y, z, width, height, style_text='', background_color='#ffffff', background_opacity=0,
                 pos_type=TextPositions.OVER):
        Coordinate = collections.namedtuple('Coordinate', 'x y z')
        Shape = collections.namedtuple('Shape', 'width height')
        self.style_text = style_text

        self.background_color = background_color
        self.background_opacity = background_opacity

        self.pos_type = pos_type
        self.pos = Coordinate(x=x, y=y, z=z)
        self.len = Shape(width=width, height=height)
