def format_bytes(num):
    """
    string formatting
    :type num: int
    :rtype: str
    """
    num = abs(num)
    if num == 0:
        return '0 Bytes'
    elif num == 1:
        return '1 Byte'
    unit = 0
    while num >= 1024 and unit < 8:
        num /= 1024.0
        unit += 1
    unit = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'][unit]
    return ('%.2f %s' if num % 1 else '%d %s') % (num, unit)


def format_seconds(num):
    """
    string formatting
    note that the days in a month is kinda fuzzy
    :type num: int | float
    """
    num = abs(num)
    if num == 0:
        return u'0 seconds'
    elif num == 1:
        return u'1 second'

    if num < 1:
        # display 2 significant figures worth of decimals
        return (u'%%0.%df seconds' % (1 - int(math.floor(math.log10(abs(num)))))) % num

    unit = 0
    denominators = [60.0, 60.0, 24.0, 7.0, 365.25 / 84.0, 12.0]
    while unit < 6 and num > denominators[unit] * 0.9:
        num /= denominators[unit]
        unit += 1
    unit = [u'seconds', u'minutes', u'hours', u'days', u'weeks', u'months', u'years'][unit]
    return (u'%.2f %s' if num % 1 else u'%d %s') % (num, unit[:-1] if num == 1 else unit)
