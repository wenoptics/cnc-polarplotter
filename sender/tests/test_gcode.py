from gcode_robot.gcode import GCodeStatement, GCodeLine


def test_gcode_parser():
    ori = 'G01 X21.194500 Y-125.353000 Z160 F25'

    raw = GCodeLine.from_str(ori)
    g = GCodeStatement.from_str(ori)
    assert str(raw.statement) == str(g)

    assert str(g) == ori
    assert g.cmd.variable == 'G'
    assert g.cmd == 'G01'
    assert g.args['Z'] == 'Z160'
    assert g.args['Z'].value == '160'

    ori = 'G01 X21.194500 Y-125.353000 Z160 F25'
    g = GCodeLine.from_str(ori + ';comment()')
    assert str(g.statement) == ori

    ori = '; G01 X21.194500 Y-125.353000 Z160 F25'
    g = GCodeLine.from_str(ori)
    assert str(g) == ''
    assert g.statement is None
    assert g.comment is not None


def test_eq():
    p_x20 = GCodeStatement.GPart('X20')
    p_x30 = GCodeStatement.GPart('Y30')

    assert p_x20 == 'X20'
    assert p_x20 == GCodeStatement.GPart('X20')

    assert p_x20 != p_x30
    assert p_x20 != 'Y30'
