# Raspberry Pi USB Stick Destroyer

Use a Raspberry Pi to wipe a USB thumbdrive 

<img width="400px" src="https://raw.github.com/jarv/stick-destroyer/master/img/stick-destroyer.jpg" alt="stick-destroyer" />
<img width="400px" src="https://raw.github.com/jarv/stick-destroyer/master/img/led.jpg" alt="stick-destroyer" />

This is a quick hack to securely wipe a USB thumbdrive with a Raspberry Pi.

An LED attached to pins 11/12 will flash while the following is done:

* All of the data on the stick is shredded. _8GB takes 20-30 minutes_
* New partition table loaded from the SD card, creates new 100MB partition at /dev/sda1
* Pin 11 held high if when complete

If any of the commands fail pin LED will remain off.

All commands, output and errors logged to `/var/log/stick-destroyer.log`


## Installation

### Boot the Raspberry Pi and Install Dependencies:

```bash
 sudo apt-get install python-dev python-pip
 sudo pip install rpi.gpio
```

### Create udev rule, partition config, shell wrapper, and copy python script

* `/etc/udev/rules.d/99-stick-destroyer.rules`:
```bash
 KERNEL=="sda", ACTION=="add", RUN+="/usr/local/bin/stick-destroyer.sh"
```

* Shell wrapper that's called by udev

`/usr/local/bin/stick-destroyer.sh`:
```bash
 #!/bin/bash
 /usr/local/bin/stick-destroyer.py &
```
* Copy [stick-destroyer.py](https://raw.github.com/jarv/stick-destroyer/master/stick-destroyer.py) to `/usr/local/bin`.



