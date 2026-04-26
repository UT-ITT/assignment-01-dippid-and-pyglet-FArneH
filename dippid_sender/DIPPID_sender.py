import socket
import numpy as np
import time
import json
import random


class DIPPIDSender:
    def __init__(self, ip="127.0.0.1", port=5700):
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.t = 0

        self.button_state = 0
        self.button_timer = 0

    def send(self, data):
        msg = json.dumps(data).encode("utf-8")
        self.sock.sendto(msg, self.addr)

    def update_button(self):

        if self.button_state == 0:
            if random.random() < 0.02:
                self.button_state = 1
                self.button_timer = random.randint(5, 15)

        else:
            self.button_timer -= 1
            if self.button_timer <= 0:
                self.button_state = 0

        return self.button_state

    def run(self):
        while True:
            self.t += 0.05

            accelerometer = {
                "x": np.sin(self.t) + np.random.normal(0, 0.03),
                "y": np.sin(self.t * 1.2 + 1) + np.random.normal(0, 0.03),
                "z": np.cos(self.t * 0.8 + 2) + np.random.normal(0, 0.03),
            }

            # 🎯 realistische Button Simulation
            button_1 = self.update_button()

            packet = {
                "accelerometer": accelerometer,
                "button_1": button_1
            }

            self.send(packet)

            time.sleep(0.05)


if __name__ == "__main__":
    sender = DIPPIDSender()
    sender.run()