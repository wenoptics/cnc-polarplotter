import logging

from main import MakelangoleRobot


if __name__ == '__main__':

    logging.basicConfig(format='[%(levelname)s][%(asctime)-15s][%(module)s] %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    mr = MakelangoleRobot('COM5')
    mr.init_connection()
    mr.run_file('../test_data/t3_modified.ngc')
