import logging
from pathlib import Path

from gcode_robot.main import MakelangoleRobot
from gcode_robot import utils

CUR_DIR = Path(__file__).parent


if __name__ == '__main__':

    logging.basicConfig(format='[%(levelname)s][%(asctime)-15s][%(module)s] %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    s = MakelangoleRobot.Settings(
        motor_width_mm=485,
        speed_idle=60,
        speed_draw=30,
        speed_pen_lift=100,
        angle_pen_up=90,
        angle_pen_down=160,
    )

    mr = MakelangoleRobot('COM5', settings=s)
    mr.init_connection()

    ngc = CUR_DIR / '../test_data/t0_simple_oval.ngc'

    # Draw a bounding box
    with open(ngc) as f:
        p1, p2 = utils.calc_bounding_area(f.read())

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

    input('ANY KEY TO CONTINUE...')
    mr.run_file(ngc)
