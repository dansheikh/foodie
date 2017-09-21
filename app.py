#!/usr/bin/env python

import argparse
import collections
import datetime
import requests


def _getchar():
    import tty
    import termios
    import sys

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


def _display_info(info_list, info_dict, batch_size=10):
    limit = len(info_list)
    idx = 0
    count = 0
    more = True
    batch = collections.deque()

    if limit == 0:
        print('\nNo Food Trucks are currently available.')
        return

    while (idx < limit and more):
        print("\n{:66s}{}".format('Name', 'Address'))

        # Append name-adress strings to the batch so that the number of elements in the batch is at least equal to batch-size.
        while len(batch) < batch_size and idx < limit:
            vendor_id = info_list[idx]

            for location in info_dict[vendor_id]:
                batch.append("{name:66s}{location}".format(name=vendor_id, location=location))

            idx += 1

        # Print batch-size number of name-address strings.
        while count < batch_size and len(batch) > 0:
            entry = batch.popleft()
            print(entry)
            count += 1

        if len(batch) > 0 or idx < limit:
            print('\nPress any key to continue or "q" to quit.')

            if _getchar() == 'q':
                more = False
            else:
                count = 0  # Reset counter.


def _parse_data(data):
    print("Parsing {count} data elements...".format(count=len(data)))
    info_list = list()
    info_dict = dict()

    for datum in data:
        applicant = datum['applicant']

        if applicant not in info_dict:
            info_list.append(applicant)
            info_dict[applicant] = [datum['location']]
        else:
            info_dict[applicant].append(datum['location'])

    info_list.sort()

    return (info_list, info_dict)


def _gather_data(url, params):
    query = ''

    for idx, key in enumerate(params.keys()):
        if idx == 0:
            query += "{key}={val}".format(key=key, val=params[key])
        else:
            query += "&{key}={val}".format(key=key, val=params[key])

        res = requests.get(url, params=query)

    print("Fetching data from {source}".format(source=res.url))

    if res.status_code >= 400:
        msg = res.json()['error_message']
        raise Exception(msg)

    return res.json()


def _main(args):
    target = None
    day = None
    time = None
    params = dict()
    url = "{url}.{format}".format(url=args.url, format=args.format)
    data = None

    if args.datetime is None:
        target = datetime.datetime.today()
        day = target.strftime("%A")
        time = "{hours:02d}:{minutes:02d}".format(hours=target.hour, minutes=target.minute)
    else:
        target = datetime.datetime.strptime(args.datetime, "%Y-%m-%d %H:%M")
        day = target.strftime("%A")
        time = "{hours:02d}:{minutes:02d}".format(hours=target.hour, minutes=target.minute)

    params['dayofweekstr'] = day
    params['start24'] = time

    try:
        data = _gather_data(url, params)
        (info_list, info_dict) = _parse_data(data)
        _display_info(info_list, info_dict, args.batch_size)

    except Exception as error:
        print(error)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='foodie')
    parser.add_argument('-u', '--url', action='store', default='https://data.sfgov.org/resource/bbb8-hzi6', type=str)
    parser.add_argument('-b', '--batch_size', action='store', default=10, help='Display batch size. Default is 10.', type=int)
    parser.add_argument('-f', '--format', action='store', default='json', help='Format options: json | xml | csv', type=str)
    parser.add_argument('-d', '--datetime', action='store', help='Datetime Format: Y-m-d H:M', type=str)

    args = parser.parse_args()

    _main(args)
