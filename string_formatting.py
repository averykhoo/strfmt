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

    # 1 or more seconds
    if num_seconds >= 1:
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
            return f'{minus}{num_seconds:,.2f} {unit}'
        else:
            return f'{minus}{num_seconds:,.0f} {unit}'

    # fractions of a second (ms, μs, ns)
    else:
        unit = 0
        while unit < 3 and num_seconds < 0.9:
            num_seconds *= 1000
            unit += 1
        unit = [u'seconds', u'milliseconds', u'microseconds', u'nanoseconds'][unit]

        # singular form
        if num_seconds == 1:
            unit = unit[:-1]

        # exact or float
        if num_seconds % 1 and num_seconds > 1:
            return f'{minus}{num_seconds:,.2f} {unit}'
        elif num_seconds % 1:
            # noinspection PyStringFormat
            num_seconds = f'{{N:,.{1 - int(math.floor(math.log10(abs(num_seconds))))}f}}'.format(N=num_seconds)
            return f'{minus}{num_seconds} {unit}'
        else:
            return f'{minus}{num_seconds:,.0f} {unit}'


def format_seconds_uncertainty(num_seconds, uncertainty=0, print_uncertainty=True):
    """
    string formatting
    note that the days in a month is kinda fuzzy
    kind of takes leap years into account, but as a result the years are fuzzy
    recommended uncertainty = 2 standard deviations ≈ 95%

    :type num_seconds: int | float
    :type uncertainty: int | float
    :type print_uncertainty: bool
    """

    def _format(_uncertainty, _minimum=0.000001):
        assert _uncertainty >= 0

        if not print_uncertainty:
            return ''

        if _uncertainty < _minimum:
            return ''
        elif _uncertainty % 1 == 0:
            return f'±{_uncertainty:,.0f}'
        elif _uncertainty < 1:
            # noinspection PyStringFormat
            return f'±{{N:,.{1 - int(math.floor(math.log10(_uncertainty)))}f}}'.format(N=_uncertainty)
        else:
            return f'±{_uncertainty:,.2f}'

    def _round(_num, _uncertainty):
        assert _uncertainty >= 0

        if _uncertainty == 0:
            return _num

        uncertainty_exponent = 10 ** math.floor(math.log10(_uncertainty))
        return math.ceil(_num / uncertainty_exponent) * uncertainty_exponent

    # handle negatives
    if num_seconds < 0:
        minus = '-'
    else:
        minus = ''
    num_seconds = abs(num_seconds)

    if print_uncertainty:
        tmp_seconds = _round(num_seconds, uncertainty)
    else:
        tmp_seconds = num_seconds

    # zero (not compatible with decimals below)
    if num_seconds == 0:
        if uncertainty > 0 and print_uncertainty:
            return f'0±{format_seconds(uncertainty)}'
        else:
            return f'0 seconds'

    # 1 or more seconds
    if tmp_seconds >= 1:
        unit = 0
        denominators = [60.0, 60.0, 24.0, 7.0, 365.25 / 84.0, 12.0]
        while unit < 6 and tmp_seconds > denominators[unit] * 0.9:
            num_seconds /= denominators[unit]
            tmp_seconds /= denominators[unit]
            uncertainty /= denominators[unit]
            unit += 1
        unit = [u'seconds', u'minutes', u'hours', u'days', u'weeks', u'months', u'years'][unit]
        num_seconds = _round(num_seconds, uncertainty / 10)

        # singular form
        if num_seconds == 1 and (uncertainty < 0.1 or not print_uncertainty):
            return f'{minus}1 {unit[:-1]}'

        # exact or float
        if num_seconds % 1:
            return f'{minus}{num_seconds:,.2f}{_format(uncertainty, 0.01)} {unit}'
        else:
            return f'{minus}{num_seconds:,.0f}{_format(uncertainty, 0.1)} {unit}'

    # fractions of a second (ms, μs, ns)
    else:
        unit = 0
        while unit < 3 and num_seconds < 0.9:
            tmp_seconds *= 1000
            num_seconds *= 1000
            uncertainty *= 1000
            unit += 1
        unit = [u'seconds', u'milliseconds', u'microseconds', u'nanoseconds'][unit]
        num_seconds = _round(num_seconds, uncertainty)

        # singular form
        if num_seconds == 1:
            return f'{minus}{num_seconds:,.0f}{_format(uncertainty, 0.1)} {unit[:-1]}'

        # exact or float
        if num_seconds % 1 and num_seconds > 1:
            return f'{minus}{num_seconds:,.2f}{_format(uncertainty, 0.01)} {unit}'
        elif num_seconds > 1:
            return f'{minus}{num_seconds:,.0f}{_format(uncertainty, 0.1)} {unit}'
        else:
            # noinspection PyStringFormat
            num_seconds = f'{{N:,.{1 - int(math.floor(math.log10(num_seconds)))}f}}'.format(N=num_seconds)
            return f'{minus}{num_seconds}{_format(uncertainty)} {unit}'
