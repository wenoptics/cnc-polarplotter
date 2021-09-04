from gcode_robot.utils import GCodeStatement


def test_gcode_parser():
    ori = 'G01 X21.194500 Y-125.353000 Z160 F25'
    g = GCodeStatement.from_str(ori)
    assert str(g) == ori

    ori = 'G01 X21.194500 Y-125.353000 Z160 F25'
    g = GCodeStatement.from_str(ori + ';comment()')
    assert str(g) == ori
