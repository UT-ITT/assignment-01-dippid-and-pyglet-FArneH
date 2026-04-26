from DIPPID import SensorUDP

PORT = 5700
sensor = SensorUDP(PORT)


def accel(data):
    print("ACCEL:", data)


def button(data):
    print("BUTTON:", data)


sensor.register_callback('accelerometer', accel)
sensor.register_callback('button_1', button)

print("Listening...")

while True:
    pass