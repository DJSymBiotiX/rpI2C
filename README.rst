rpI2C
=====

rpI2C is a Raspberry-Pi I2C Library

Setup
=====

-  Install the smbus and i2c tools onto the Pi

   ::

           $ sudo apt-get install python-smbus
           $ sudo apt-get install i2c-tools

-  Install kernel support with raspi-config

   ::

           $ sudo raspi-config

-  Go to "Advanced Options"
-  Enable I2C
-  Reboot
-  You can also follow this guide:
   https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

How to use
==========

Installing rpI2C
----------------

Installing from pip
~~~~~~~~~~~~~~~~~~~

::

        $ pip install rpI2C

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

::

        $ python setup.py install

Example Script
~~~~~~~~~~~~~~

::

        import rpI2C

        address = 0x18
        bus = rpI2C.I2C(address)
        data = bus.read_raw_byte()
        bus.write_raw_byte(0x00)
        bus.clean_up()

Bus Value
~~~~~~~~~

On different versions of the Raspberry-Pi you will need to use a
different bus value for the I2C bus. On some it's '0' and others it's
'1'. This library tries to connect to bus '0' first and if that fails,
it will connect to bus '1'. You can specify a bus manually in the
initializer.

::

        bus = rpI2C.I2C(address, bus=0)

Contributing
============

Send ideas through github issues.

Send patches through pull requests.

Code should ideally:

- Follow PEP8
- Generate no pyflakes warnings

License
=======

Written by Fernando Chorney Released under the MIT License:
http://www.opensource.org/licenses/mit-license.php
