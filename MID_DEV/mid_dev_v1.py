# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#!/usr/bin/env python
from digi.xbee.devices import XBeeDevice
import http.client
import json
from os import stat

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600


def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    
    device = XBeeDevice(PORT, BAUD_RATE)

     
    headers = {"Content-type": "application/json"}
    conn = http.client.HTTPConnection("192.168.1.107:5000")
    try:
        device.open()
        def data_receive_callback(xbee_message):
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))
            MAC = xbee_message.remote_device.get_64bit_addr() 
            stat = xbee_message.data.decode()
            conn.request("GET", "/v1/parking/0")
            resp = conn.getresponse()
            data = json.loads(resp.read())
            floor = data["floor"]
            params = json.dumps({"place":str(MAC),"status":int(stat)})
            if MAC in floor.keys():
                conn.request("POST","/v1/parking/0", params, headers)
            else:
                conn.request("POST","/v1/parking/0/"+str(MAC), params, headers)
            response = conn.getresponse()
        device.add_data_received_callback(data_receive_callback)
        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
