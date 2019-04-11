from datetime import datetime
from time import sleep
import json


def log_1(message, when=datetime.now()):
    print('%s %s' % (when, message))


print('example 1')
log_1('Hi there!')
sleep(0.1)
log_1('Hi there!')
print('\n')


def log_2(message, when=None):
    """
    Log a message with a timestamp.

    :param message: Message to print
    :param when: datetime of when the message ocurred. Defaults to the present time.
    :return: None
    """
    when = datetime.now() if when is None else when
    print('%s %s' % (when, message))


print('example 2')
log_2('Hi there!')
sleep(0.1)
log_2('Hi there!')
print('\n')


def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)


def decode_2(data, default=None):
    """
    Load JSON data from a string.

    :param data: JSON data to decode
    :param default: Value to return if decoding fails. Defaults to an empty dictionary
    :return: str
    """
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default


foo_2 = decode_2('bad data')
foo_2['stuff'] = 5
bar_2 = decode_2('also bad')
bar_2['meep'] = 1
print('Foo 2:', foo_2)
print('Bar 2:', bar_2)
print()