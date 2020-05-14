def convert_date(date):
    # Convert date from dd/mm/yy format to day-mon-YY format
    res = str(date.day)
    if date.day in (1,21,31):
        res += 'st'
    elif date.day in (2,22):
        res += 'nd'
    elif date.day in (3,23):
        res += 'rd'
    else:
        res += 'th'
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    res += " " + months[int(date.month)]
    res += " " + str(date.year) 
    return res

def biggest_date_difference(dates):       # Input: list[key list of dates dictionary]
    dates.sort()
    if len(dates) == 1:
        return 0, dates[0], dates[0]
    max_diff = abs((dates[1] - dates[0]).days)
    date1 = dates[0]
    date2 = dates[1]
    for i in range(1, len(dates)):
        diff = abs((dates[i] - dates[i-1]).days)
        if diff > max_diff:
            max_diff = diff
            date1 = dates[i-1]
            date2 = dates[i]
    
    return max_diff, date1, date2

def longest_streak(dates):                # Input: list[key list of dates dictionary]
    dates.sort()
    streak = 1
    max_streak = 1
    st, max_st = dates[0], dates[0]
    en, max_en = dates[0], dates[0]
    for i in range(1,len(dates)):
        if abs((dates[i] - dates[i-1]).days) == 1:
            streak += 1
            en = dates[i]
        else:
            if streak > max_streak:
                max_streak = streak
                max_st = st
                max_en = en
            streak = 1
            st = dates[i]
    if streak > max_streak:
        max_streak = streak
        max_st = st
        max_en = en
    return max_streak, max_st, max_en

def most_messages_per_day(dates):              # Input: dictionary[dates dictionary]
    top3 = [[None, 0], [None, 0], [None, 0]]       # [0]: 3rd rank, [1]: 2nd rank [2]: 3rd rank
    for i in dates:
        if top3[0][1] < dates[i]:
            top3[0][0] = i
            top3[0][1] = dates[i]
        top3.sort(key = lambda x: x[1])
    return top3

def sender_count(sender_msg):
    return len(sender_msg)

def count_words(msg):
    if msg == '<Media Omitted>':
        return 0
    return msg.count(' ') + 1