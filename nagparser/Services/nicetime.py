from datetime import datetime, timedelta


def getnicetimefromdatetime(datetimeinput, basedatetime=None):
    """Convert a datetime to a human-readable time difference string.
    
    Calculates the time difference between a given datetime and a base datetime
    (or current time if not specified) and returns it as a human-readable string
    like "2d 3h", "5h 30m", "45m 12s", or "30s".
    
    Args:
        datetimeinput (datetime): The datetime to convert to a nice time string
        basedatetime (datetime, optional): The base datetime to compare against. Defaults to datetime.now() if not provided.
    
    Returns:
        str: Human-readable time difference string formatted as "Xd Xh" if days > 0, "Xh Xm" if hours > 0 (and days == 0), "Xm Xs" if minutes > 0 (and hours == 0), or "Xs" if only seconds
    
    Example:
        >>> from datetime import datetime, timedelta
        >>> past_time = datetime.now() - timedelta(hours=2, minutes=30)
        >>> getnicetimefromdatetime(past_time)
        '2h 30m'
        >>> past_time = datetime.now() - timedelta(days=1, hours=5)
        >>> getnicetimefromdatetime(past_time)
        ' 1d  5h'
    """
    if basedatetime is None:
        base = datetime.now()
    else:
        base = basedatetime

    if (base > datetimeinput):
        delta = base - datetimeinput
    else:
        delta = datetimeinput - base

    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if delta.days > 0:
        result = ' %sd  %sh' % (delta.days, hours)
    elif hours > 0:
        result = '%sh %sm' % (hours, minutes)
    elif minutes > 0:
        result = '%sm %ss' % (minutes, seconds)
    else:
        result = '%ss' % (seconds)

    return result


def getdatetimefromnicetime(nicetime, basedatetime=None):
    """Convert a human-readable time string to a datetime object.
    
    Parses a string like "1d 2h 30m" or "5h:30m:15s" and adds that duration
    to a base datetime (or current time if not specified).
    
    Args:
        nicetime (str): Time string with units (d=days, h=hours, m=minutes, s=seconds).
                       Can be space-separated (e.g., "1d 2h") or colon-separated (e.g., "2:30:15").
        basedatetime (datetime, optional): The base datetime to add the duration to.
                                          Defaults to datetime.now() if not provided.
    
    Returns:
        datetime: The result of adding the parsed duration to the base datetime.
    
    Example:
        >>> from datetime import datetime
        >>> base = datetime(2023, 1, 1, 12, 0, 0)
        >>> result = getdatetimefromnicetime("1d 2h 30m", base)
        >>> print(result)
        2023-01-02 14:30:00
    """
    if basedatetime is None:
        base = datetime.now()
    else:
        base = basedatetime

    result = [0, 0, 0, 0]
    sections = nicetime.lower().split(':')
    if len(sections) == 1:
        sections = nicetime.split(' ')

    for section in sections:
        if section.find('d') > 0:
            result[0] = int(section.replace('d', ''))
        if section.find('h') > 0:
            result[1] = int(section.replace('h', ''))
        if section.find('m') > 0:
            result[2] = int(section.replace('m', ''))
        if section.find('s') > 0:
            result[3] = int(section.replace('s', ''))

    delta = timedelta(days=result[0], hours=result[1], minutes=result[2], seconds=result[3])

    return base + delta

if __name__ == "__main__":
    pass
