import math
import io
from typing import TextIO, Union

from gcode_robot.common import Point
from gcode_robot.gcode import GCodeStatement, clean_line

DEFAULT_PEN_DOWN = lambda g: g.args.get('Z') and 160 == float(g.args['Z'].value)
DEFAULT_PEN_UP = lambda g: g.args.get('Z') and 90 == float(g.args['Z'].value)


def gcode_reader(raw: Union[str, TextIO], clean_comment=True):
    if isinstance(raw, str):
        raw = io.StringIO(raw)

    for li in raw.readlines():
        if clean_comment:
            li = clean_line(li)
            if not li:
                continue

        yield li


def calc_bounding_area(
    gcode: str, is_pen_down=DEFAULT_PEN_DOWN, is_pen_up=DEFAULT_PEN_UP
):
    min_x, max_x = math.inf, -math.inf
    min_y, max_y = math.inf, -math.inf

    _writing = False
    for li in gcode_reader(gcode):
        g = GCodeStatement.from_str(li)
        if is_pen_down(g):
            _writing = True
        elif is_pen_up(g):
            _writing = False

        if _writing:
            if g.cmd not in ['G01', 'G00']:
                continue

            x, y = g.args.get('X'), g.args.get('Y')
            if x:
                min_x = min(min_x, float(x.value))
                max_x = max(max_x, float(x.value))
            if y:
                min_y = min(min_y, float(y.value))
                max_y = max(max_y, float(y.value))

    assert math.inf not in (min_x, min_y, max_x, max_y)
    assert -math.inf not in (min_x, min_y, max_x, max_y)

    return Point(min_x, min_y), Point(max_x, max_y)


if __name__ == '__main__':
    # Some quick inline tests
    pass
