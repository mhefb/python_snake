import serial
import glob
import time

import Config
from errors.InputError import InputError

# Serial connection
__ser = None

# Callback for when something changes with the players
__on_change = None


# Returns all usb-ports with connected devices
def __get_ports():
    return glob.glob("/dev/ttyUSB*")


# Opens the port
def __open_port():
    global __ser

    # Gets all connected ports
    ports = __get_ports()

    # Ensures only one device got detected
    if len(ports) != 1:
        raise InputError("Es wurden " + str(len(ports)) + " gefunden. Bitte schließe mindestens bzw. nur ein Gerät an.")

    # Opens the serial-connection
    __ser = serial.Serial(ports[0], Config.ESP_BAUD)


# Inits the controller-input
def init(on_change):
    global __on_change
    __on_change = on_change


# Updates the controller-input
def update():
    global __ser, __on_change
    try:

        # Ensures an open connection to the esp
        if __ser is None:
            __open_port()

        # Waits until data got found
        while __ser.inWaiting() >= 3:
            # Gets next data
            data = __ser.read(3)

            # Performs checksum-check using XOR
            if data[0] ^ data[1] != data[2]:
                print("Error detected")
                # Kills remaining bytes to prevent out-of-sync
                __ser.read(__ser.inWaiting())
                return

            # Reads in the packet and executes the callback
            __on_change(data[0] | (data[1] << 8))

    except serial.serialutil.SerialException:
        print("Serial-port error. Retrying...")
        time.sleep(1)
