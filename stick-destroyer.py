#!/usr/bin/python
import os
import subprocess
import logging
import sys
import time
import RPi.GPIO as gpio

# set up logging
formatter = logging.Formatter('%(asctime)s %(process)d %(message)s')
logger = logging.getLogger(__name__)
f_hdlr = logging.FileHandler('/var/log/stick-destroyer.log')
f_hdlr.setFormatter(formatter)
logger.addHandler(f_hdlr)
stdout_hdlr = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_hdlr)
logger.setLevel(logging.DEBUG)

def run(cmd, valid_ret=0):
    """
    cmd - Command to run
    valid_ret - return code to check

    Runs a command, raises an exception
    if return doesn't match valid_ret.
    """

    logger.info('running: {}'.format(cmd))
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True)
    for line in iter(process.stdout.readline, ""):
        logger.debug(line.rstrip())
        # on every line of status blink the LED
        blink()

    ret = None
    while ret is None:
        ret = process.poll()

    if ret != valid_ret:
        raise Exception("`{0}` returned {1}, expected {2}".format(cmd, ret, valid_ret))

def blink():
    """
    Blinks pin 11.
    """
    gpio.output(11, gpio.HIGH)
    time.sleep(.20)
    gpio.output(11, gpio.LOW)
    time.sleep(.20)
    return

def destroyer():
    """
    Destroys the device /dev/sda, which in the
    raspberry pi case will (hopefully) be a USB
    stick.
    """

    # use raspberry pi board pin numbers
    gpio.setmode(gpio.BOARD)
    # set 11 and 12 as output pins
    gpio.setup(11, gpio.OUT)
    gpio.setup(12, gpio.OUT)
    # set 12 low
    gpio.output(12, gpio.LOW)
    run('shred --iterations 1 --verbose --size 200M /dev/sda 2>&1')
    run('cat /usr/local/etc/100M.partition |  sfdisk /dev/sda 2>&1')
    run('mkfs.vfat /dev/sda1 2>&1')
    # turn on the LED when done
    gpio.output(11, gpio.HIGH)

if __name__ == '__main__':
    try:
        destroyer()
    except Exception as e:
        # global exception handler will
        # log the exception info and
        # turn off the LED to indicate
        # a problem
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error_reason = '{0}: {1}'.format(exc_type, e)
        logger.critical('USB destroyer ended in error: ' + error_reason)
        gpio.cleanup()
        raise
