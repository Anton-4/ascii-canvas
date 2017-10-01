"""Items can be placed on the Canvas."""
from __future__ import print_function


class Item(object):
    """Defined by an arbitrary text and a position on the Canvas."""

    def __init__(self, text, position=[0, 0]):
        """Hold a text and a position."""
        self.text = text
        self.position = position

    @property
    def bbox(self):
        """Make the bbox encompass the text."""
        lines = self.text.split('\n')
        return [0, 0, max([len(l) for l in lines]), len(lines)]


class Line(Item):
    """A line between two points.

    It is drawn like this:

        START ---+
                 |
                 |
                 +--- END
    """

    def __init__(self, start, end):
        """Define the line by a start and an end point."""
        self.start = start
        self.end = end

    @property
    def bbox(self):
        """Make the bbox encompass the entire line."""
        return [0, 0,
                abs(self.end[0] - self.start[0]) + 1,
                abs(self.end[1] - self.start[1]) + 1]

    @property
    def text(self):
        """Create a string representing the line.

        1. Go half way horizontally
        2. Go straight down to the end of y
        3. Continue rest horizontally
        """
        text = ''
        first_y = self.bbox[1]
        half_x = int((self.bbox[2] - self.bbox[0]) * 0.5)
        last_y = self.bbox[3] - 1
        for row in range(self.bbox[1], self.bbox[3]):
            for column in range(self.bbox[0], self.bbox[2]):
                if row == first_y and column < half_x:
                    text += '-'
                elif row == last_y and column > half_x:
                    text += '-'
                elif row == first_y and column == half_x:
                    if self.bbox[3] - self.bbox[1] > 1:
                        text += '+'
                    else:
                        text += '-'
                elif row == last_y and column == half_x:
                    text += '+'
                elif row != first_y and row != last_y and column == half_x:
                    text += '|'
                else:
                    text += ' '
            text += '\n'
        if self.start[1] > self.end[1]:
            text = '\n'.join(text.split('\n')[::-1])
        return text

    @property
    def position(self):
        """Offset the position if the start is left of the end."""
        if self.start[1] <= self.end[1]:
            return self.start
        else:
            return [self.start[0], self.start[1] - self.bbox[3]]
