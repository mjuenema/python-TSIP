#!/usr/bin/python

import struct

def main():

    with open('thunderbolt.tsip') as reader:
        for packet in GPS(reader):
            print Packet.unpack(packet)



if __name__ == '__main__':
    main()

