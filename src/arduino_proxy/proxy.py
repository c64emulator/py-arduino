# TODO: _unindent() could be a annotation

import serial

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def _unindent(spaces, the_string):
    lines = []
    start = ' '*spaces
    for a_line in the_string.splitlines():
        if a_line.startswith(start):
            lines.append(a_line[spaces:])
        else:
            lines.append(a_line)
    return '\n'.join(lines)

class ArduinoProxy(object):
    
    INPUT = "I"
    OUTPUT = "O"
    
    def __init__(self, tty, speed=9600):
        # For communicating with the computer, use one of these rates: 300, 1200, 2400, 4800,
        #    9600, 14400, 19200, 28800, 38400, 57600, or 115200.        
        self.tty = tty
        self.speed = speed
        self.serial_port = None
        if tty:
            self.serial_port = serial.Serial(port=tty, baudrate=speed, bytesize=8, parity='N',
                stopbits=1, timeout=5)
    
    def _setup(self):
        # FIXME: implementar!
        return _unindent(8, """
        char lastCmd[128]; // buffer size of Serial
        
        void setup() {
            Serial.begin(%(speed)d);
        }
        
        void readCmd() {
            int incomingByte = 0xff;
            int pos = 0;
            lastCmd[0] = 0;
            
            while (Serial.available() > 0 && pos < 128) {
                // read the incoming byte:
                lastCmd[pos] = Serial.read();
                if(lastCmd[pos] == 0) {
                    break;
                }
                pos++;
            }
        }

        void sendOkResponse() {
            Serial.print("OK");
            Serial.write((uint8_t)0);
        }
        
        int stringToInt(String str) {
            char buff[str.length() + 1];
            str.toCharArray(buff, (str.length() + 1));
            return atoi(buff); 
        }
        
        void sendIntResponse(int value) {
            Serial.print(value, DEC);
            Serial.write((uint8_t)0);
        }
        """ % {
            'speed': self.speed, 
        })
    
    _setup.include_in_pde = True
    _setup.proxy_function = False
    
    def sendCmd(self, cmd):
        """
        Sends a command to the arduino. The command is terminated with a 0x00.
        Returns the response as a string.
        """
        self.serial_port.write(cmd)
        self.serial_port.write(0x00)
        self.serial_port.flush()
        
        response_buffer = StringIO()
        while True:
            byte = self.serial_port.read()
            if byte == 0x00:
                break
            else:
                response_buffer.write(byte)
        
        return response_buffer.getvalue()
    
    # Digital I/O
    def _pinMode(self):
        return _unindent(12, """
            void _pinMode(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                int index_of_mode = cmd.indexOf(' ', index_of_pin+1);
                String pin = cmd.substring(index_of_pin, index_of_mode);
                String mode = cmd.substring(index_of_mode);
                if(mode.equals("%(INPUT)s")) {
                    pinMode(stringToInt(pin), INPUT);
                    sendOkResponse();
                    return;
                }
                if(mode.equals("%(OUTPUT)s")) {
                    pinMode(stringToInt(pin), OUTPUT);
                    sendOkResponse();
                    return;
                }
            }
        """ % {
        'method': 'pinMode', 
        'INPUT': ArduinoProxy.INPUT, 
        'OUTPUT': ArduinoProxy.OUTPUT, 
    })
    
    _pinMode.include_in_pde = True
    _pinMode.proxy_function = True
    
    def pinMode(self, pin, mode):
        """
        * ...vast majority of Arduino (Atmega) analog pins, may be configured, and used,
        in exactly the same manner as digital pins.
        * Arduino (Atmega) pins default to inputs: high-impedance state (extremely small demands
        on the circuit)
        * NOTE: Digital pin 13 is harder to use as a digital input than the other digital pins
        because it has an LED and resistor attached to it that's soldered to the board
        * it is a good idea to connect OUTPUT pins to other devices with 470omh or 1k resistors
        
        TODO: The analog input pins can be used as digital pins, referred to as A0, A1, etc.
        """
        cmd = "_pinMode %d %s" % (pin, mode)
        ret = self.sendCmd(cmd)
        return ret

    def digitalWrite(self):
        pass
    
    def digitalRead(self):
        pass

    #Analog I/O
    def analogReference(self):
        pass
    
    def _analogRead(self):
        return _unindent(12, """
            void _analogRead(String cmd) {
                if(!cmd.startsWith("%(method)s")) {
                    return;
                }
                int index_of_pin = cmd.indexOf(' ');
                String pin = cmd.substring(index_of_pin);
                int value = analogRead(stringToInt(pin));
                sendIntResponse(value);
                return;
            }
        """ % {
        'method': 'analogRead', 
    })
    
    _analogRead.include_in_pde = True
    _analogRead.proxy_function = True
    
    def analogRead(self, pin):
        """
        * map input voltages between 0 and 5 volts into integer values between 0 and 1023.
        """
        cmd = "_analogRead %d" % (pin)
        ret = self.sendCmd(cmd)
        return ret
    
    def analogWrite(self):
        pass

if __name__ == '__main__':
    proxy = ArduinoProxy('')

    print _unindent(8, """
        /*
         * THIS FILE IS GENERATED AUTOMATICALLI WITH generate-pde.sh
         * WHICH IS PART OF THE PROYECT "PyArduinoProxy"
         */
    """)
    
    # All this functions have 'include_in_pde' == True
    pde_functions = [getattr(proxy, a_function) for a_function in dir(proxy)
        if getattr(getattr(proxy, a_function), 'include_in_pde', None) is True]
    
    # First functions that have 'proxy_function' == False
    for a_function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is False]:
        print a_function()
    
    # Now the real, interesting functions...
    for a_function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is True]:
        print a_function()
    
    # Now, generate the loop()
    print "void loop() {"
    print "    readCmd();"
    
    for a_function in [a_function for a_function in pde_functions
            if getattr(a_function, 'proxy_function', None) is True]:
        print "    " + a_function.__name__ + "(String(lastCmd));"
    print "}"
