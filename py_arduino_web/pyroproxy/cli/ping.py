# Licensed under the Apache License, Version 2.0
# Copyright (C) 2011-2015 - Horacio Guillermo de Oro <hgdeoro@gmail.com>

import sys
import time

from py_arduino_web.pyroproxy.utils import BasePyroMain


class Main(BasePyroMain):

    def run(self, options, args, arduino):
        while True:
            sys.stdout.write("Ping sent...")
            sys.stdout.flush()
            start = time.time()
            try:
                arduino.ping()
                end = time.time()
                sys.stdout.write(" OK - Time={0:.3f} ms\n".format((end - start) * 1000))
                sys.stdout.flush()
                time.sleep(1)
            except KeyboardInterrupt:
                raise
            except:  # CommandTimeout
                # TODO: check with PYRO if original exceptoin was CommandTimeout
                sys.stdout.write(" error\n")
                sys.stdout.flush()
                end = time.time()
                if (end - start) < 0.5:
                    time.sleep(0.5)

if __name__ == '__main__':
    Main().start()
