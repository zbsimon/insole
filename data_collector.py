#!/usr/bin/env python

from __future__ import print_function
import socket
import sys

filename = "output.csv"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    PORT_NUM = 8190
    addr = ("", PORT_NUM)
    sock.bind(addr)

    with open(filename, "w") as f:
        while True:
            try:
                data = sock.recv(4096)
                vals = data.split(',')
                vals = [val.strip() for val in vals]
                if not len(vals) % 4 == 1:
                    print("couln't understand data", file=sys.stderr)
                timestamp = vals[0]

                """
                note we have to take care of the index (i.e. 3, 4)
                """

                # samples = [vals[i:i + 4] for i in range(1, (len(vals) - 1) / 4, 4)]
                # samples = [vals[(1 + 3 * i):min(3 + 3 * i, len(vals) + 1)] for i in range((len(vals) - 1) / 3)]
                # samples = [{samples[i][0]: samples[i][1:]}]
                print(data, file=f)
                # print(data)
                # print(samples)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e, file=sys.stderr)
                pass
    sock.close()


if __name__ == '__main__':
    main()
