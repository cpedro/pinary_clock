# Pinary Clock

Python program to display binary clock via LEDs connected to Raspberry Pi.

### Pinouts

* Hour Pins:
  * '16': WiringPi pin 0 (GPIO 17, Pi pin 11)
  * '8': WiringPi pin 1 (GPIO 18, Pi pin 12)
  * '4': WiringPi pin 2 (GPIO 27, Pi pin 13)
  * '2': WiringPi pin 3 (GPIO 22, Pi pin 15)
  * '1': WiringPi pin 4 (GPIO 23, Pi pin 16)
* Minute Pins:
  * '32': WiringPi pin 5 (GPIO 24, Pi pin 18)
  * '16': WiringPi pin 6 (GPIO 24, Pi pin 18)
  * '8': WiringPi pin 7 (GPIO 25, Pi pin 22)
  * '4': WiringPi pin 8 (GPIO 2, Pi pin 3)
  * '2': WiringPi pin 9 (GPIO 3, Pi pin 5)
  * '1': WiringPi pin 10 (GPIO 8, Pi pin 24)

### Usage
```shell
usage: clock.py [-h] [-t] [-d]

Pinary Clock

optional arguments:
  -h, --help   show this help message and exit
  -t, --test   Test pins mode
  -d, --debug  Debug output, flashes all used pins in sequence from hour to
               minute
```

