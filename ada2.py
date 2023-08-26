# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
`fingerprint_template_file_compare.py`
====================================================

This is an example program to demo storing fingerprint templates in a file. It also allows
comparing a newly obtained print with one stored in the file in previous step. This is helpful
when fingerprint templates are stored centrally (not on sensor's flash memory) and shared
between multiple sensors.

* Author(s): admiralmaggie

Implementation Notes
--------------------

**Hardware:**

* `Fingerprint sensor <https://www.adafruit.com/product/751>`_ (Product ID: 751)
* `Panel Mount Fingerprint sensor <https://www.adafruit.com/product/4651>`_ (Product ID: 4651)
"""

import time
import board
import busio
from digitalio import DigitalInOut, Direction


import serial
import adafruit_fingerprint


# import board (if you are using a micropython board)
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
uart = serial.Serial("/dev/ttyUSB1", baudrate=115200, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
# uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi 3 with pi3-disable-bte
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
finger._debug = True

##################################################


def sensor_reset():
    """Reset sensor"""
    print("Resetting sensor...")
    if finger.soft_reset() != adafruit_fingerprint.OK:
        print("Unable to reset sensor!")
    print("Sensor is reset.")

# pylint: disable=too-many-branches
def fingerprint_check_file():
    """Compares a new fingerprint template to an existing template stored in a file
    This is useful when templates are stored centrally (i.e. in a database)"""
    print("Waiting for finger print...")
    # set_led_local(color=3, mode=1)
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(2) != adafruit_fingerprint.OK:
        print("duh")
        return False

    data = []
    print("Loading file template...", end="")
    with open("template0.dat", "rb") as file:
        data = list(file.read())
    
    time.sleep(.25)
    finger.send_fpdata(data, "char", 1)
    time.sleep(.25)
    print("masih di sini")
    
    # print("Searching...")
    # if finger.finger_search() != adafruit_fingerprint.OK:
    #     return False
    # return True

    i = finger.compare_templates()

    print("masih di sini 2")

    if i == adafruit_fingerprint.OK:
        # set_led_local(color=2, speed=150, mode=6)
        print("Fingerprint match template in file.")
        return True
    if i == adafruit_fingerprint.NOMATCH:
        # set_led_local(color=1, mode=2, speed=20, cycles=10)
        print("Templates do not match!")
    else:
        print("Other error!")
    return False

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False

    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

# pylint: disable=too-many-statements
def enroll_save_to_file():
    """Take a 2 finger images and template it, then store it in a file"""
    # set_led_local(color=3, mode=1)
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                # set_led_local(color=1, mode=2, speed=20, cycles=10)
                print("Imaging error")
                return False
            else:
                # set_led_local(color=1, mode=2, speed=20, cycles=10)
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                # set_led_local(color=1, mode=2, speed=20, cycles=10)
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                # set_led_local(color=1, mode=2, speed=20, cycles=10)
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                # set_led_local(color=1, mode=2, speed=20, cycles=10)
                print("Image invalid")
            else:
                # set_led_local(color=1, mode=2, speed=20, cycles=10)
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            # set_led_local(color=1, mode=2, speed=20, cycles=10)
            print("Prints did not match")
        else:
            # set_led_local(color=1, mode=2, speed=20, cycles=10)
            print("Other error")
        return False

    print("Downloading template...")
    data = finger.get_fpdata("char", 1)
    with open("template0.dat", "wb") as file:
        file.write(bytearray(data))
    # set_led_local(color=2, speed=150, mode=6)
    print("Template is saved in template0.dat file.")

    return True

# pylint: disable=broad-except
def set_led_local(color=1, mode=3, speed=0x80, cycles=0):
    """this is to make sure LED doesn't interfer with example
    running on models without LED support - needs testing"""
    try:
        finger.set_led(color, mode, speed, cycles)
    except Exception as exc:
        print("INFO: Sensor les not support LED. Error:", str(exc))

# set_led_local(color=3, mode=2, speed=10, cycles=10)

while True:
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates: ", finger.templates)
    if finger.count_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Number of templates found: ", finger.template_count)
    time.sleep(.25)
    if finger.set_sysparam(6, 2) != adafruit_fingerprint.OK:
        raise RuntimeError("Unable to set package size to 128!")
    if finger.read_sysparam() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to get system parameters")
    print("Package size (x128):", finger.data_packet_size)
    print("Size of template library: ", finger.library_size)
    print("e) enroll print and save to file")
    print("c) compare print to file")
    print("f) find print")
    print("r) soft reset")
    print("x) quit")
    print("----------------")
    # c = input("> ")

    fingerprint_check_file()
    
    # enroll_save_to_file()
    
    # if get_fingerprint():
    # if fingerprint_check_file():
    #     print("Detected #", finger.finger_id, "with confidence", finger.confidence)
    # else:
    #     print("Finger not found")

    # if c in ("x", "q"):
    #     print("Exiting fingerprint example program")
    #     # turn off LED
    #     # set_led_local(mode=4)
    #     raise SystemExit
    # if c == "e":
    #     enroll_save_to_file()
    # elif c == "c":
    #     fingerprint_check_file()
    # elif c == "f":
    #     if get_fingerprint():
    #         print("Detected #", finger.finger_id, "with confidence", finger.confidence)
    #     else:
    #         print("Finger not found")
    # elif c == "r":
    #     sensor_reset()
    # else:
    #     print("Invalid choice: Try again")
