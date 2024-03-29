import logging
from pathlib import Path

from gcode_robot.main import MakelangoleRobot
from gcode_robot import utils

CUR_DIR = Path(__file__).parent


if __name__ == '__main__':

    logging.basicConfig(format='[%(levelname)s][%(asctime)-15s][%(module)s] %(message)s')  # noqa: E501
    logging.getLogger().setLevel(logging.DEBUG)

    s = MakelangoleRobot.Settings(
        motor_width_mm=485,
        speed_idle=60,
        speed_draw=30,
        speed_pen_lift=100,
        angle_pen_up=90,
        angle_pen_down=150,
    )

    mr = MakelangoleRobot('COM3', settings=s)
    mr.init_connection()

    mr.show_init_diagram()
    input('ANY KEY TO CONFIRM...')

    ngc = CUR_DIR / '../test_data/cat-hang_0002.ngc'

    # Draw a bounding box
    with open(ngc) as f:
        p1, p2 = utils.calc_bounding_area(
            f.read(),
            is_pen_down=lambda g: g.args.get('Z') and s.angle_pen_down == float(g.args['Z'].value),  # noqa: E501
            is_pen_up=lambda g: g.args.get('Z') and s.angle_pen_up == float(g.args['Z'].value)  # noqa: E501
        )

    input(f'Bounding box: ({p1}, {p2}). ANY KEY TO CONTINUE...')
    mr.run_code_block(f"""
        G00 X{p1.x} Y{p1.y} F{s.speed_idle}
        G01 Z{s.angle_pen_down} F{s.speed_pen_lift}
        G01 X{p1.x} Y{p2.y} F{s.speed_draw}
        G01 X{p2.x} Y{p2.y} F{s.speed_draw}
        G01 X{p2.x} Y{p1.y} F{s.speed_draw}
        G01 X{p1.x} Y{p1.y} F{s.speed_draw}
        G01 Z{s.angle_pen_up} F{s.speed_pen_lift}
    """)
    mr.go_home()

    input('ANY KEY TO START...')
    mr.run_file(ngc)
