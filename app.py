from __future__ import absolute_import, unicode_literals

import time
import logging

from pymodbus.client.sync import ModbusTcpClient

DEBUG = True

logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s')
log = logging.getLogger()

if DEBUG:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

if __name__ == "__main__":
    try:
        client = ModbusTcpClient('192.168.7.2', port=502)
        client.connect()
    except:
        time.sleep(2)
        print("reconnect")
