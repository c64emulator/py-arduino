#!/usr/bin/env python
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

from . import setup_pythonpath

setup_pythonpath()

from py_arduino import InvalidCommand, CommandTimeout, InvalidResponse
from py_arduino.main_utils import default_main
from py_arduino import NotConnected, HIGH, OUTPUT, LSBFIRST


def main():  # pylint: disable=R0915
    _, _, arduino = default_main()  # pylint: disable=W0612
    try:
        print "getFreeMemory() -> %s" % str(arduino.getFreeMemory())
        print "enableDebug() -> %s" % str(arduino.enableDebug())
        print "disableDebug() -> %s" % str(arduino.disableDebug())
        print "validateConnection() -> %s" % str(arduino.validateConnection())
        print "ping() -> %s" % str(arduino.ping())
        print "pinMode() -> %s" % str(arduino.pinMode(13, OUTPUT))
        print "analogRead() -> %s" % str(arduino.analogRead(0))
        print "analogWrite() -> %s" % str(arduino.analogWrite(0, 128))
        print "digitalRead() -> %s" % str(arduino.digitalRead(0))
        print "digitalWrite() -> %s" % str(arduino.digitalWrite(0, HIGH))
        print "digitalRead() -> %s" % str(arduino.digitalRead(0))
        print "delay() -> %s" % str(arduino.delay(1))
        print "delayMicroseconds() -> %s" % str(arduino.delayMicroseconds(1))
        print "millis() -> %s " % str(arduino.millis())
        print "micros() -> %s" % str(arduino.micros())
        print "shiftOut() -> %s" % str(arduino.shiftOut(10, 11, LSBFIRST, 255,
            set_pin_mode=True))
        print "getArduinoTypeStruct() -> %s" % str(arduino.getArduinoTypeStruct())
        print "enhanceArduinoTypeStruct() -> %s" % str(arduino.enhanceArduinoTypeStruct(
            arduino.getArduinoTypeStruct()))

        #define RETURN_OK 0
        #define READ_ONE_PARAM_NEW_LINE_FOUND 7
        #define READ_ONE_PARAM_EMPTY_RESPONSE 1
        #define READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE 2
        #define READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS 3
        #define UNEXPECTED_RESPONSE_FROM_READ_ONE_PARAM 4
        #define UNEXPECTED_RESPONSE_FROM_READ_PARAMETERS 5
        #define FUNCTION_NOT_FOUND 6

        try:
            print "Check for READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE"
            arduino.send_cmd("laaaarge_meeeethod_" * 10)
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, exception:
            # READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE == 2
            print " +", exception
            assert exception.error_code == "2"

        try:
            print "Check for FUNCTION_NOT_FOUND"
            arduino.send_cmd("_nonexisting\tp1\tp2\tp3\tp4\tp5\tp6\tp7\tp8\tp9")
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, exception:
            # FUNCTION_NOT_FOUND == 6
            print " +", exception
            assert exception.error_code == "6"

        try:
            print "Check for READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS"
            arduino.send_cmd("cmd\tp1\tp2\tp3\tp4\tp5\tp6\tp7\tp8\tp9\tp10")
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, exception:
            # READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS == 3
            print " +", exception
            assert exception.error_code == "3"

        arduino.setTimeout(1)
        print "delay(500)"
        arduino.delay(500)

        print "delay(2000)"
        arduino.delay(2000)

        print "low level delay(500)"
        ret = arduino.send_cmd("%s\t500" % (arduino.delay.arduino_function_name))
        assert ret == "D_OK"

        print "low level delay(1500)"
        try:
            arduino.send_cmd("%s\t1500" % (arduino.delay.arduino_function_name))
            assert False, "The previous line should raise an exception!"
        except CommandTimeout, exception:
            print " +", exception.__class__

        try:
            # The INPUT buffer has the response from the timed-out delay()
            # Anything before a validateConnection() should fail.
            print "ping() -> %s" % str(arduino.ping())
            assert False, "The previous line should raise an exception!"
        except InvalidResponse, exception:
            pass

        print "Re-connecting after timeout. validateConnection() -> %s" % \
            str(arduino.validateConnection())

        # Now, the connection is valid again, ping() should work...
        print "ping() -> %s" % str(arduino.ping())

        print "getFreeMemory() -> %s" % str(arduino.getFreeMemory())

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Test streaming
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Test streaming of analog values
        for val in arduino.streamingAnalogRead(0, 10):
            print "streamingAnalogRead() -> %s" % str(val)

        # Test streaming of analog values
        for val in arduino.streamingDigitalRead(0, 10):
            print "streamingDigitalRead() -> %s" % str(val)

        print "validateConnection() -> %s" % str(arduino.validateConnection())
        print "millis() -> %s " % str(arduino.millis())
        # Finished!

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Test NotConnected/close()/re-connect()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print "Test close() and re-connect()"
        assert arduino.is_connected()
        arduino.close()
        assert not arduino.is_connected()

        try:
            arduino.ping()
        except NotConnected:
            pass

        arduino.connect()
        arduino.ping()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Test autoconnect()
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print "Test autoconnect()"
        arduino.close()
        assert arduino.autoconnect()
        arduino.ping()

    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        if arduino.is_connected():
            arduino.close()


if __name__ == '__main__':
    main()
