import serial
import glob
import time

BTN_A = 1
BTN_B = 2
BTN_UP = 3
BTN_DOWN = 4
BTN_LEFT = 5
BTN_RIGHT = 6
BTN_START = 7
BTN_SELECT = 8

buttons = ["A", "B", "UP", "DOWN", "LEFT", "RIGHT", "START", "SELECT"]


def get_ports():
    return glob.glob("/dev/ttyUSB*")


def is_pressed(status, button):
    return (status >> button) & 1


def run():
    ports = get_ports()

    if len(ports) != 1:
        print("Es wurden " + str(len(ports)) + " gefunden. Bitte schließen ein Gerät an.")
        return

    ser = serial.Serial(ports[0], 9600)

    while True:
        if ser.inWaiting() < 3:
            time.sleep(0.05)
            continue

        data = ser.read(3)

        if data[0] ^ data[1] != data[2]:
            print("Error detected")
            ser.read(ser.inWaiting())
            continue

        out = data[0] | (data[1] << 8)
        print("Raw: " + "{0:b}".format(out))
        print("\nPlayer: " + str(out & 1))
        for x in range(len(buttons)):
            print(buttons[x] + ": " + str(is_pressed(out, x + 1)))
        print("\n\n")


run()
