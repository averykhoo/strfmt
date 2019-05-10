import math


def format_bytes(num_bytes):
    """
    string formatting
    :type num_bytes: int
    :rtype: str
    """

    # handle negatives
    if num_bytes < 0:
        minus = '-'
    else:
        minus = ''
    num_bytes = abs(num_bytes)

    # ±1 byte (singular form)
    if num_bytes == 1:
        return f'{minus}1 Byte'

    # determine unit
    unit = 0
    while unit < 8 and num_bytes > 999:
        num_bytes /= 1024.0
        unit += 1
    unit = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'][unit]

    # exact or float
    if num_bytes % 1:
        return f'{minus}{num_bytes:,.2f} {unit}'
    else:
        return f'{minus}{num_bytes:,.0f} {unit}'


def format_seconds(num_seconds):
    """
    string formatting
    note that the days in a month is kinda fuzzy
    kind of takes leap years into account, but as a result the years are fuzzy
    :type num_seconds: int | float
    """

    # handle negatives
    if num_seconds < 0:
        minus = '-'
    else:
        minus = ''
    num_seconds = abs(num_seconds)

    # zero (not compatible with decimals below)
    if num_seconds == 0:
        return '0 seconds'

    # fractions of a second (should be improved with ms, μs, ns)
    if num_seconds < 1:
        # display 2 significant figures worth of decimals
        return (f'{minus}%%0.%df seconds' % (1 - int(math.floor(math.log10(abs(num_seconds)))))) % num_seconds

    # determine unit
    unit = 0
    denominators = [60.0, 60.0, 24.0, 7.0, 365.25 / 84.0, 12.0]
    while unit < 6 and num_seconds > denominators[unit] * 0.9:
        num_seconds /= denominators[unit]
        unit += 1
    unit = [u'seconds', u'minutes', u'hours', u'days', u'weeks', u'months', u'years'][unit]

    # singular form
    if num_seconds == 1:
        unit = unit[:-1]

    # exact or float
    if num_seconds % 1:
        return f'{num_seconds:,.2f} {unit}'
    else:
        return f'{num_seconds:,.0f} {unit}'
