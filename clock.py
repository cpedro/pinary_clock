#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""
File: clock.py
Description: Displays a binary clock of the current time via lighting up LEDs.
    Meant to be run from a Raspberry Pi.

    Pinouts:
    Hour:
        '16': WiringPi pin 0  - GPIO 17 - Pi pin 11
        '8':  WiringPi pin 1  - GPIO 18 - Pi pin 12
        '4':  WiringPi pin 2  - GPIO 27 - Pi pin 13
        '2':  WiringPi pin 3  - GPIO 22 - Pi pin 15
        '1':  WiringPi pin 4  - GPIO 23 - Pi pin 16
    Minute:
        '32': WiringPi pin 5  - GPIO 24 - Pi pin 18
        '16': WiringPi pin 6  - GPIO 25 - Pi pin 22
        '8':  WiringPi pin 7  - GPIO 4  - Pi pin 7
        '4':  WiringPi pin 8  - GPIO 2  - Pi pin 3
        '2':  WiringPi pin 9  - GPIO 3  - Pi pin 5
        '1':  WiringPi pin 10 - GPIO 8  - Pi pin 24

usage: clock.py [-h] [-t] [-d]

Pinary Clock

optional arguments:
  -h, --help   show this help message and exit
  -t, --test   Test pins mode
  -d, --debug  Debug output, flashes all used pins in sequence from hour to
               minute
"""


__author__ = 'Chris Pedro'
__copyright__ = '(c) Chris Pedro 2021'
__licence__ = 'MIT'


import argparse
import sys
import time
import wiringpi

from datetime import datetime
from signal import *


# Change to define output pins.
hour_pins = {
    '16': 0,
    '8': 1,
    '4': 2,
    '2': 3,
    '1': 4
}
min_pins = {
    '32': 5,
    '16': 6,
    '8': 7,
    '4': 8,
    '2': 9,
    '1': 10
}

# Value used for all sleep commands.  Adjust as needed.
t_delay = 0.25

p_args = []


def parse_args(args):
    """Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Pinary Clock')
    parser.add_argument(
        '-t', '--test', action='store_true', help='Test pins mode')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug output, flashes all used pins in sequence from hour to '
        'minute')
    return parser.parse_args(args)


def main(args):
    """Main method.
    """
    global p_args
    p_args = parse_args(args)
    setup()
    while True:
        loop()


def setup():
    """Setup method, preps GPIO pins.
    """
    wiringpi.wiringPiSetup()
    for pin in hour_pins.values():
        wiringpi.pinMode(pin, wiringpi.OUTPUT)
    for pin in min_pins.values():
        wiringpi.pinMode(pin, wiringpi.OUTPUT)
    clear_all_pins()


def cleanup(signal_received, frame):
    """Cleanup method, clears all pins.
    """
    clear_all_pins()
    sys.exit(0)


def loop():
    """Main execution loop.
    """
    global p_args
    if p_args.test:
        test_all_pins()
        test_time()
        return

    now = datetime.now().time()
    if p_args.debug:
        print('-----------------------------')
        print('Time = {:02d}:{:02d}'.format(now.hour, now.minute))
        print('-----------------------------')
        print('Hour Pins:')
        print('-----------------------------')
    set_pins(hour_pins, now.hour)
    if p_args.debug:
        print('-----------------------------')
        print('Minute Pins:')
        print('-----------------------------')
    set_pins(min_pins, now.minute)
    time.sleep(t_delay)


def clear_all_pins():
    """Method for 'clearing' all pins, turns all LEDs off.
    """
    for pin in hour_pins.values():
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    for pin in min_pins.values():
        wiringpi.digitalWrite(pin, wiringpi.LOW)


def test_all_pins():
    """Method for testing pins, sequentially lights up all LEDs.
    """
    for pin in hour_pins.values():
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        time.sleep(t_delay)
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    for pin in min_pins.values():
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        time.sleep(t_delay)
        wiringpi.digitalWrite(pin, wiringpi.LOW)


def test_time():
    for hour in range(24):
        for minute in range(60):
            set_pins(hour_pins, hour)
            set_pins(min_pins, minute)
            time.sleep(0.2)


def set_pins(pins, hour):
    """Method for setting all hour pins that are needed.
    """
    global p_args
    # Clear all pins by default
    clear_bits = pins.copy()
    set_bits = {}

    # If a bit needs to be set add it to set_bits and remove it from clear_bits
    for bit in bits(hour):
        clear_bits.pop(str(bit))
        set_bits[str(bit)] = pins[str(bit)]

    # Clear bits
    for bit in clear_bits:
        if p_args.debug:
            print('\t{}\tClear'.format(bit))
        wiringpi.digitalWrite(pins[str(bit)], wiringpi.LOW)

    # Set bits
    for bit in set_bits:
        if p_args.debug:
            print('\t{}\tSet'.format(bit))
        wiringpi.digitalWrite(pins[str(bit)], wiringpi.HIGH)


def bits(int_type):
    """Method to get list of bits that are set or cleared in an integer.
    """
    bit = 1
    while int_type >= bit:
        if int_type & bit:
            yield bit
        bit <<= 1


if __name__ == '__main__':
    for sig in (SIGABRT, SIGINT, SIGTERM):
        signal(sig, cleanup)
    sys.exit(main(sys.argv[1:]))

