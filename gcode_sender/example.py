import logging

from main import MakelangoleRobot


if __name__ == '__main__':

    logging.basicConfig(format='[%(levelname)s][%(asctime)-15s][%(module)s] %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    s = MakelangoleRobot.Settings(
        motor_width_mm=485,
        speed_idle=30,
        speed_draw=20,
        speed_pen_lift=100,
        angle_pen_up=160,
        angle_pen_down=90,
    )

    mr = MakelangoleRobot('COM5', settings=s)
    mr.init_connection()

    mr.run_file('../test_data/t0_simple_oval.ngc')
