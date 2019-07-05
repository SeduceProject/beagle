from __future__ import absolute_import, unicode_literals

import time
import logging
import traceback

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian

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

        print("connecté!")

        # Essai de récupération des registres

        # Registre  R/W   Valeur  Type   Min   Max
        # 0         R     1       u16    -     -
        # 1         R     2       u16    -     -
        # 2         R     4       u16    -     -
        # 3         R     8       u16    -     -
        # 4         R     16      u16    -     -
        value = client.read_holding_registers(0, 5, unit=1)
        print(value.registers)

        # Registre  R/W   Valeur  Type   Min   Max
        # 1000      R     1234    u16    -     -
        # 1001      R     5678    u16    -     -
        value = client.read_holding_registers(1000, 2, unit=1)
        print(value.registers)
        
        # Registre  R/W   Valeur  Type    Min     Max
        # 2000      R/W   5678    u16     0       4923
        # 2000      R/W   5678    u16     0       4923
        # 2001      R/W   0       u16     -       -
        # 2002-2003 R/W   0       s32     -80000  70000
        # 2004-2005 R/W   0       float   -10.5   300.9
        # 2006-2007 R/W   0       float   0       70596
        # 2008      R/W   0       s16     -10000  10000
        # 2009      R/W   0       u16     -       -
        # 2010-2011 R/W   0       float   0       3000000000
        value = client.read_holding_registers(2000, 1, unit=1)
        print(value.registers)

        result  = client.read_holding_registers(2000, 12, unit=1)
        print(result.registers)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder='>', wordorder='>')
        decoded = {
            '1': decoder.decode_16bit_uint(),
            '2': decoder.skip_bytes(2),
            '3': decoder.decode_32bit_int(),
            '4': decoder.decode_32bit_float(),
            '5': decoder.decode_32bit_float(),
            '6': decoder.decode_16bit_int(),
            '7': decoder.skip_bytes(1),
            '8': decoder.decode_32bit_float(),
        }

        print("-" * 60)
        print("Decoded Data")
        print("-" * 60)
        for name, value in decoded.items():
            print ("%s\t" % name, value)

        # Try to write registers 2000

        builder = BinaryPayloadBuilder(byteorder='>', wordorder='>')
        
        builder.add_16bit_uint(1234)
        builder.add_16bit_uint(0) # Skip 1 byte        
        builder.add_32bit_int(-1234)
        builder.add_32bit_float(-1.234)
        builder.add_32bit_float(10)
        builder.add_16bit_int(-5678)
        builder.add_16bit_uint(0) # Skip 1 byte
        builder.add_32bit_float(1)
        
        payload = builder.to_registers()
        print("-" * 60)
        print("Writing Registers")
        print("-" * 60)
        print(payload)
        print("\n")
        payload = builder.build()
        # Can write registers
        registers = builder.to_registers()
        response = client.write_registers(2000, registers, unit=1)
        print(response)
    
    except:
        print("pas de connexion")
        traceback.print_exc()
