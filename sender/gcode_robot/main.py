from dataclasses import dataclass
import logging
from typing import Optional, Union
import time

import serial

from gcode_robot.common import Point
from gcode_robot.utils import gcode_reader
from gcode_robot.gcode import GCodeLine, GCodeStatement

logger = logging.getLogger(__name__)


class MakelangoleRobot:
    IDLE_BYTES = b'> \n'

    @dataclass
    class Settings:
        # General settings
        motor_width_mm: float = 500
        speed_idle: float = 30

        # Servo settings
        speed_draw: float = 20
        speed_pen_lift: float = 50

        angle_pen_up: float = 90
        angle_pen_down: float = 160

    def __init__(self, port: str, baudrate=57600,
                 settings: Optional['MakelangoleRobot.Settings'] = None):
        self._serial = serial.Serial()
        self._serial.port = port
        self._serial.baudrate = baudrate
        self._current_settings = settings
        self._home = Point(0, 0)

    def _wait_for_idle(self):
        _t = time.time()
        ret = self._serial.read_until(self.IDLE_BYTES)
        logger.debug('Spent {:.2f} ms waiting for idle'
                     .format(time.time() - _t))
        return ret

    def _wait_read(self):
        msg = b''
        while not msg:
            msg = self._serial.readline()
            # time.sleep(0.1)
        msg += self._serial.read_until(self.IDLE_BYTES)
        return msg.rstrip(self.IDLE_BYTES)

    def _send_gcode(self, line: Union[str, bytes, GCodeLine, GCodeStatement]):
        if isinstance(line, GCodeLine):
            line = line.statement
        if isinstance(line, GCodeStatement):
            line = str(line)
        if type(line) is str:
            line = line.encode()
        if line is None:
            return

        if not line.endswith(b'\n'):
            line += b'\n'

        logger.debug('Sending: {}'.format(line))
        self._serial.write(line)

    def init_connection(self):
        if not self._serial.is_open:
            self._serial.open()

        welcome_msg = self._wait_read()
        logger.info('Receive welcome message: {}'.format(welcome_msg.decode()))

        self.apply_settings()

    def apply_settings(self,
                       settings: Optional['MakelangoleRobot.Settings'] = None):
        if settings:
            self._current_settings = settings

        s = self._current_settings
        if s is None:
            raise

        # Report current firmware version
        self._send_gcode('D5')
        logger.debug('Received: {}'.format(self._wait_read()))

        # Report all settings
        self._send_gcode('M503')
        logger.debug('Received: {}'.format(self._wait_read()))

        self._send_gcode('M17')
        logger.debug('Received: {}'.format(self._wait_read()))

        # Change axis A limits to max T and min B
        half_width = self._current_settings.motor_width_mm / 2
        self._send_gcode(f'M101 A0 T{half_width} B{-half_width}')
        self._send_gcode('M101 A1 T464 B-464')
        self._send_gcode('M101 A2 T170 B90')

        # TODO Allow home to be configured
        self.make_home(Point(0, -472))

        self._send_gcode('M17')
        logger.debug('Received: {}'.format(self._wait_read()))

        # Set initial feed rate
        self._send_gcode(f'G00 X0 F{s.speed_idle}')
        logger.debug('Received: {}'.format(self._wait_read()))

    def set_home(self, p: Point):
        # Set home
        self._send_gcode(f'D6 {p.gcode}')
        self._home = p
        logger.debug('Received: {}'.format(self._wait_read()))

    def make_home(self, p: Point):
        # Teleport
        self._send_gcode(f'G92 {p.gcode}')
        logger.debug('Received: {}'.format(self._wait_read()))

        self.set_home(p)

    def go_home(self, speed=None):
        if speed is None:
            speed = self._current_settings.speed_idle

        # self._send_gcode(f'G28 F{speed}')
        self._send_gcode(f'G00 {str(self._home)} F{speed}')

    def run_code_block(self, raw: str):

        self._wait_for_idle()

        n = 0
        for line in gcode_reader(raw):
            n += 1

            if not line.statement:
                continue

            logger.debug('Processing line {}'.format(n))

            self._send_gcode(line)
            self._wait_for_idle()

    def run_file(self, gcode_path: str):
        # Make sure to lift pen
        self._send_gcode(f'G01 '
                         f'Z{self._current_settings.angle_pen_up} '
                         f'F{self._current_settings.speed_pen_lift}')

        # Write GCODE
        with open(gcode_path) as f:
            self.run_code_block(f)

        # Make sure to lift pen
        self._send_gcode(f'G01 '
                         f'Z{self._current_settings.angle_pen_up} '
                         f'F{self._current_settings.speed_pen_lift}')

        # Goto init position
        self.go_home()

    def show_init_diagram(self):
        diagram = r"""
                         W
             │◄───────────────────►│
             |                     |
        ┌──┬───┬─────────────────┬───┬──┐
        │  │ o │                 │ o │  │  ───
        │  └───┘                 └───┘  │    ▲
        │      \                 /      │    │
        │       \               /       │    │
        │        \             /        │    │
        │         \           /         │    │
        │          \         /          │    │ H
        │           \       /           │    │
        │            \     /            │    │
        │             ┌───┐             │    │
        │             │   │             │    ▼
        │             │ x │             │  ───
        │             └───┘             │
        │                               │
        │                               │
        │                               │
        └───────────────────────────────┘

        (All units are in millimeter(mm) )
        W: The distance between the two motors
        H: The vertical distance between the motor and the pen

        """
        print('Please confirm the following initialization:')
        print(f'W = {self._current_settings.motor_width_mm},\nH = {"?"}')
        print(diagram)
