import logging

import serial

logger = logging.getLogger(__name__)


class MakelangoleRobot:
    IDLE_BYTES = b'> \n'

    def __init__(self, port: str, baudrate=57600):
        self._serial = serial.Serial()
        self._serial.port = port
        self._serial.baudrate = 57600

    def _wait_for_idle(self):
        return self._serial.read_until(self.IDLE_BYTES)

    def _wait_read(self):
        msg = b''
        while not msg:
            msg = self._serial.readline()
            # time.sleep(0.1)
        msg += self._serial.read_until(self.IDLE_BYTES)
        return msg.rstrip(self.IDLE_BYTES)

    def _send_gcode(self, bytes: bytes):
        if type(bytes) is str:
            bytes = bytes.encode()

        if not bytes.endswith(b'\n'):
            bytes += b'\n'

        logger.debug('Sending: {}'.format(bytes))
        self._serial.write(bytes)

    def init_connection(self):
        if not self._serial.is_open:
            self._serial.open()

        welcome_msg = self._wait_read()
        logger.info('Receive welcome message: {}'.format(welcome_msg.decode()))

        # Report current firmware version
        self._send_gcode('D5')
        logger.debug('Received: {}'.format(self._wait_read()))

        # Report all settings
        self._send_gcode('M503')
        logger.debug('Received: {}'.format(self._wait_read()))

        self._send_gcode('M17')
        logger.debug('Received: {}'.format(self._wait_read()))

        # Change axis A limits to max T and min B
        self._send_gcode('M101 A0 T242.5 B-242.5')
        self._send_gcode('M101 A1 T464 B-464')
        self._send_gcode('M101 A2 T170 B90')

        # Teleport
        self._send_gcode('G92 X0 Y-472')
        logger.debug('Received: {}'.format(self._wait_read()))

        # Set home
        self._send_gcode('D6 X0 Y-472')
        logger.debug('Received: {}'.format(self._wait_read()))

        self._send_gcode('M17')
        logger.debug('Received: {}'.format(self._wait_read()))

    def run_file(self, gcode_path: str):
        # Write GCODE
        with open(gcode_path) as f:
            for n, code in enumerate(f.readlines()):
                logger.debug('Processing line {}'.format(n))

                code = code.strip()
                if code.startswith(';') or code.startswith('('):
                    continue

                self._send_gcode(code)
                self._wait_for_idle()

        # Goto init position
        self._send_gcode('G00 X0 Y-472 F20')
