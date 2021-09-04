from gcode_robot.gcode import GCodeStatement, clean_line


def test_gcode_parser():
    ori = 'G01 X21.194500 Y-125.353000 Z160 F25'
    raw = clean_line(ori)
    g = GCodeStatement.from_str(raw)
    assert str(g) == ori
    assert g.cmd.variable == 'G'
    assert g.cmd == 'G01'
    assert g.args['Z'] == 'Z160'
    assert g.args['Z'].value == '160'

    ori = 'G01 X21.194500 Y-125.353000 Z160 F25'
    raw = clean_line(ori + ';comment()')
    g = GCodeStatement.from_str(raw)
    assert str(g) == ori

    ori = '; G01 X21.194500 Y-125.353000 Z160 F25'
    assert clean_line(ori) == ''


def test_eq():
    p_x20 = GCodeStatement.GPart('X20')
    p_x30 = GCodeStatement.GPart('Y30')

    assert p_x20 == 'X20'
    assert p_x20 == GCodeStatement.GPart('X20')

    assert p_x20 != p_x30
    assert p_x20 != 'Y30'
