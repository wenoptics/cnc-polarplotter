import serial

IDLE_BYTES = b'> \n'

def wait_for_idle(s):
    return s.read_until(IDLE_BYTES)

def wait_read(s):
    msg = b''
    while not msg:
        msg = s.readline()
        # time.sleep(0.1)
    msg += s.read_until(IDLE_BYTES)
    return msg.rstrip(IDLE_BYTES)

def send_code(s, bytes: bytes):
    if type(bytes) is str:
        bytes = bytes.encode()

    if not bytes.endswith(b'\n'):
        bytes += b'\n'

    print('[Debug] sending: {}'.format(bytes))
    s.write(bytes)


# with serial.Serial("COM5", 57600) as s:
s = serial.Serial()
s.port = 'COM5'
s.baudrate = 57600
s.open()

welcome_msg = wait_read(s)
print(welcome_msg)

# Report current firmware version
send_code(s, b'D5')
print(wait_read(s))

# Report all settings
send_code(s, b'M503')
print(wait_read(s))

send_code(s, b'M17')
print(wait_read(s))

# Change axis A limits to max T and min B
send_code(s, b'M101 A0 T242.5 B-242.5')
send_code(s, b'M101 A1 T464 B-464')
send_code(s, b'M101 A2 T170 B90')

# Teleport
send_code(s, b'G92 X0 Y-472')
print(wait_read(s))

# Set home
send_code(s, b'D6 X0 Y-472')
print(wait_read(s))

send_code(s, b'M17')
print(wait_read(s))

# Write GCODE
with open('../test_data/t3_modified.ngc') as f:
    for n, l in enumerate(f.readlines()):
        l = l.strip()
        if l.startswith(';') or l.startswith('('):
            continue
        
        print(f'Processing line {n}')
        send_code(s, l)
        wait_for_idle(s)


send_code(s, 'G00 X0 Y-472 F20')
