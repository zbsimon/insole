#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import ast
import time
import socket
import logging
import argparse


help_text = """

This program logs gyro/accel data from the IMU+GPS-Sensorstream
android application
(https://play.google.com/store/apps/details?id=de.lorenz_fenster.sensorstreamgps&hl=en)

"""


log_filename_template = "imu_sensorstream_log_{}.csv"
DEFAULT_PORT = 8190
PACKET_SIZE = 4096
argparse_formatter = argparse.ArgumentDefaultsHelpFormatter


def update_globals(samples):
    latest_sample = samples[-1]
    latest_sample_as_string = ""
    delim = ","
    for key, value in sorted(latest_sample.items()):
        if key in ['timestamp', 3, 81]:
            latest_sample_as_string += value + delim
    latest_sample_as_string.trim(delim)

    # may want to log this instead
    print(latest_sample_as_string)


def validate_data(raw_data_string):
    """
    attempts to parse raw_data_string as a csv line, raises if it fails
    """
    if raw_data_string is None:
        raise(Exception("invalid data: data is NULL"))

    values = [value.strip() for value in raw_data_string.strip().split(',')]
    if not (len(values) - 1) % 4 == 0:
        raise(Exception("invalid data: number of values"))

    # ensure every 4i+1 value is an int
    try:
        for i in range(1, len(values) - 1, 4):
            values[i] = int(values[i])
    except ValueError:
        raise(Exception("invalid data: index columns must be integers"))

    values = [value if type(value) is int else float(value) for value in values]
    return values


def format_values(values):
    """
    returns string representation of values that excel can understand
    """
    result = ', '.join([repr(value) for value in values])
    return result


def values_to_dict(values):
    results = {}
    results['timestamp'] = values[0]
    for i in range(1, len(values), 4):
        results[values[i]] = values[(i + 1):(i + 4)]
    return results


def main():

    parser = argparse.ArgumentParser(description=help_text,
                                     formatter_class=argparse_formatter)

    output_help = "the relative directory to place logged data in"
    parser.add_argument('--output', '--dst', dest='output_file',
                        help=output_help, default='./imu_data/')

    verbose_help = "if set, these flags force debug info to be sent to stderr"
    parser.add_argument('--debug', '--verbose', '-d', '-v', dest='verbose',
                        action="store_true", help=verbose_help)

    port_help = "the port number to open a UDP connection on"
    parser.add_argument('--port', '-p', dest='port', default=DEFAULT_PORT,
                        help=port_help, type=int)

    replay_help = "DON'T begin a server and INSTEAD proceed by reading samples from REPLAY_FILE"
    parser.add_argument('--replay', '-r', dest='replay_file', help=replay_help, default=None)

    args = parser.parse_args()

    output_dir = args.output_file
    verbose = args.verbose
    port = args.port
    replay_file = args.replay_file

    log = logging.getLogger('data_logger')
    log.setLevel(logging.INFO)
    timestamp = repr(time.time()).replace('.', '-')
    log_filename = os.path.join(output_dir,
                                log_filename_template.format(timestamp))

    if replay_file is not None:
        with open(replay_file, 'r') as f:
            data = []
            for line in f:
                data.append(ast.literal_eval(line))
                update_globals(data)
        return

    # ensure log file exists:
    if not os.path.exists(os.path.dirname(log_filename)):
        os.makedirs(os.path.dirname(log_filename))
    try:
        with open(log_filename, 'a'):
            pass
    except:
        print("Couldn't open log file {} ... exiting now".format(log_filename),
              file=sys.stderr)
        return

    log_file_handler = logging.FileHandler(log_filename, mode='w+')
    log.addHandler(log_file_handler)

    stderr = logging.getLogger('stderr')
    if verbose:
        stderr.setLevel(logging.DEBUG)
    else:
        stderr.setLevel(logging.ERROR)
    stderr.addHandler(logging.StreamHandler())

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("", port)

    # i'm just gonna put everything in here for a while so we can
    # have access to it later
    results = []

    sock.bind(addr)

    while True:
        try:
            data = sock.recv(PACKET_SIZE)
            values = validate_data(data)
            log.info(format_values(values))
            values_dict = values_to_dict(values)
            results.append(values_dict)
            stderr.debug(values_dict)
            update_globals(values_dict)
        except KeyboardInterrupt:
            break
        except Exception as e:
            stderr.error(e)
            pass

    sock.close()


if __name__ == '__main__':
    main()
