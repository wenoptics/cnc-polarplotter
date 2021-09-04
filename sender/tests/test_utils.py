from pathlib import Path

from gcode_robot import utils

data = Path(__file__).absolute().parent / 'data'


def test_bounding():
    with open(data / 't0_simple_oval.ngc') as f:
        p1, p2 = utils.calc_bounding_area(
            f.read(),
            is_pen_down=lambda g: g.args.get('Z') and 160 == float(g.args['Z'].value),
            is_pen_up=lambda g: g.args.get('Z') and 90 == float(g.args['Z'].value)
        )

    assert p1
    assert p2
