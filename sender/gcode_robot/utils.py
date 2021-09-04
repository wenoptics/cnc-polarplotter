import math
from typing import Mapping

from gcode_robot.common import Point

DEFAULT_PEN_DOWN = lambda cmd, args: 'Z160' in [p.raw for p in args.values()]


class GCodeStatement:

    class GPart:
        """A part is like "X-10.25". """
        raw: str
        variable: str
        value: str

        def __init__(self, raw: str):
            self.raw = raw
            if raw:
                self.variable = raw[0]
                self.value = raw[1:]

        def __str__(self):
            return self.raw

        def __repr__(self):
            return '{}<Var="{}" Value="{}">'.format(
                self.__class__.__name__,
                self.variable,
                self.value
            )

    def __init__(self, cmd: GPart, args: Mapping[str, GPart]):
        self.cmd = cmd
        self.args = args

    def __str__(self):
        parts = [p.raw for p in self.args.values()]
        return f'{self.cmd.raw} {" ".join(parts)}'

    @classmethod
    def from_str(cls, raw: str):

        # Remove comments, i.e. ; and (
        raw = raw.split(';', 1)[0]
        raw = raw.split('(', 1)[0]
        raw = raw.strip()

        s = raw.split()
        first, parts = s[0], s[1:]
        cmd = GCodeStatement.GPart(first)

        args = {}
        for part in parts:
            p = GCodeStatement.GPart(part)
            args[p.variable] = p

        return cls(cmd, args)


def parse_cmd(gcode_cmd: str) -> GCodeStatement:
    return GCodeStatement.from_str(gcode_cmd)


def calc_bounding_area(gcode: str, is_pen_down=DEFAULT_PEN_DOWN):
    min_x, max_x = math.inf, -math.inf
    min_y, max_y = math.inf, -math.inf

    is_writing = False
    for li in gcode.splitlines():
        c = parse_cmd(li)
        is_writing = is_pen_down()
        

if __name__ == '__main__':
    # Some quick inline tests
    cmd = parse_cmd('G01 X21.194500 Y-125.353000 Z160 F25')
    print(str(cmd))
