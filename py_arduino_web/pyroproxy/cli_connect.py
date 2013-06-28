##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    py-arduino - Access your Arduino from Python
##    Copyright (C) 2011-2013 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of py-arduino.
##
##    py-arduino is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    py-arduino is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with py-arduino; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import sys

from py_arduino.proxy import DEVICE_FOR_EMULATOR

from .utils import get_arduino_pyro


def main():
    arduino = get_arduino_pyro()
    if len(sys.argv) > 1:
        device = sys.argv[1]
    else:
        device = DEVICE_FOR_EMULATOR
    print "Calling proxy.connect() - Connecting to {0}".format(device)
    arduino.connect(device)
    print "Calling proxy.ping() to check the connection"
    ret = arduino.ping()
    print "Ping returned: '{0}'. End.".format(ret)

if __name__ == '__main__':
    main()
