def sort_dates(dates):
    dates.sort(key = lambda date: list(map(int, date.split('/')))[::-1])
    return dates

def get_date_difference(date1, date2):
    from datetime import date
    d1, m1, y1 = map(int, date1.split('/'))
    d2, m2, y2 = map(int, date2.split('/'))
    diff = date(y2, m2, d2) - date(y1, m1, d1)
    return abs(diff.days)

def convert_date(date):
    # Convert date from dd/mm/yy format to day-mon-YY format
    day, month, year = map(int, date.split('/'))
    res = ''
    res += str(day)
    if day in [1,21,31]:
        res += 'st '
    elif day in [2, 22]:
        res += 'nd '
    elif day in [3, 23]:
        res += 'rd '
    else:
        res += 'th '
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    res += months[month]
    res += " 20" + str(year)    
    return res