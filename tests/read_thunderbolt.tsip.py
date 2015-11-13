#!/usr/bin/python

import binascii


def main():

    with open('thunderbolt.tsip') as fp:

        while True:
            dle_count = 0

            p = ''

            while True:
                b = fp.read(1)

                p += b

                if ord(b) == 0x10:
                    dle_count += 1
                elif ord(b) == 0x03 and (dle_count % 2) == 1:
                    break
                else:
                    pass

            print binascii.hexlify(p[:2])


if __name__ == '__main__':
    main()

