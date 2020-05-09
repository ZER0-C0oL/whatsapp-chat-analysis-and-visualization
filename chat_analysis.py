chat = ''
# Enter the path where the chat is stored
file_name = './chat1.txt'
with open(file_name, mode = 'r', encoding = 'utf-8') as f:
    chat = f.readlines()

senders = set()      # To mark whether a message traversed is from a new sender or old
messages = dict()    # Store all messages in structured format
dates = dict()       # Store all dates in structures format
last = None

for msg in chat:
    if not (len(msg) > 12 and msg[2] == '/' and msg[5] == '/' and msg[8] == ',' and (msg[11] == ':' or msg[12] == ':')):
        # This means there was a newline in chat and is a part of previous message
        messages[last][-1] += ' ' + content
        continue
            
    # Extract different components of raw data
    try:
        d, t = msg.index(','), msg.index('-')
        s = t + msg[t:].index(':')
        date = msg[:d]
        tim = msg[d+2:t]
        sender = msg[t+2:s]
        content = msg[s+2:-1]
    except:
        # Irrevelant stuff such as changed group's icon, left group, joined group, etc.
        continue
        
    # Adding data
    if sender not in senders:
        senders.add(sender)
        messages[sender] = [content]
        dates[sender] = dict()
    else:
        messages[sender].append(content)
            
    if date in dates[sender]:
        dates[sender][date] += 1
    else:
        dates[sender][date] = 1
            
    last = sender

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

# Date statistics

def biggest_date_difference(dates):       # Input: list[key list of dates dictionary]
    dates = sort_dates(dates)
    if len(dates) == 1:
        return 0
    max_diff = get_date_difference(dates[0], dates[1])
    date1 = dates[0]
    date2 = dates[1]
    for i in range(1, len(dates)):
        diff = get_date_difference(dates[i-1], dates[i])
        if diff > max_diff:
            max_diff = diff
            date1 = dates[i-1]
            date2 = dates[i]
    
    return max_diff, date1, date2

def longest_streak(dates):                # Input: list[key list of dates dictionary]
    dates = sort_dates(dates)
    streak = 1
    max_streak = 1
    st, max_st = dates[0], dates[0]
    en, max_en = dates[0], dates[0]
    for i in range(1,len(dates)):
        if get_date_difference(dates[i], dates[i-1]) == 1:
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

# Message Counts

def sender_count(sender_msg):
    return len(sender_msg)

stat_sender = dict()
total_msgs = 0
for sender in senders:
    stat_sender[sender] = dict()
    
    date_diff, st, en = biggest_date_difference(list(dates[sender].keys()))
    stat_sender[sender]['biggest_date_difference'] = (date_diff, convert_date(st), convert_date(en))
    
    streak, st, en = longest_streak(list(dates[sender].keys()))
    stat_sender[sender]['longest_streak'] = (streak, convert_date(st), convert_date(en))
    
    top3 = most_messages_per_day(dates[sender])[::-1]
    for i in range(len(top3)):
        top3[i][0] = convert_date(top3[i][0])
    stat_sender[sender]['most_messages'] = top3
    
    count = sender_count(messages[sender])
    stat_sender[sender]['total_messages'] = count
    total_msgs += count

# Content Statistics
for sender in senders:
    count = 0
    for m in messages[sender]:
        if "<Media omitted>" in m:
            count += 1
    stat_sender[sender]["media"] = count

# Group Statistics
participants = []
for sender in senders:
    participants.append([sender, stat_sender[sender]['total_messages']])
participants.sort(key = lambda x: -x[1])

date_count = dict()
for sender in senders:
    for date in dates[sender]:
        if date in date_count:
            date_count[date] += dates[sender][date]
        else:
            date_count[date] = dates[sender][date]
date_count = list(date_count.items())
date_count.sort(key = lambda x: -x[1])

from markdown import markdown as md

html_file = open('analysis.html', mode = 'w', encoding = 'utf-8', errors = 'xmlcharrefreplace')

html_file.write(md("## User Statistics"))
for ctr, sender in enumerate(senders,1):
    html_file.write(md("#### {}. {}".format(ctr, sender)))
    html_file.write(md("* Total Messages: {}".format(stat_sender[sender]['total_messages'])))
    html_file.write(md("* Media Sent: {}".format(stat_sender[sender]['media'])))
    html_file.write(md("* Top most active days:-"))
    for day, count in stat_sender[sender]['most_messages']:
        html_file.write(md("{}> {}: {} messages".format(' '*10,day, count)))
    c, s, e = stat_sender[sender]['longest_streak']
    html_file.write(md("* Longest Streak: {} days (from {} to {})".format(c,s,e)))
    c, s, e = stat_sender[sender]['biggest_date_difference']
    html_file.write(md("* Longest Span without messages: {} days (from {} to {})".format(c,s,e)))

html_file.write(md("## Overall Statistics"))
    
html_file.write(md("#### Most active participants"))

ctr = 1
for s, c in participants[:min(10,len(participants))]:
    html_file.write(md("{}\. {}: {} messages ({}%)".format(ctr, s, c, int((c/total_msgs) * 100))))
    ctr += 1
    
html_file.write('\n'*2)
html_file.write(md("#### Most active days"))
for day, count in date_count[:min(5, len(date_count))]:
    html_file.write(md(" {}: {} messages".format(convert_date(day), count)))

# Visualizations

import matplotlib.pyplot as plt
labels = []
sizes = []
for l, s in participants:
   labels.append(l)
   sizes.append(s)
explode = [0.0] * len(labels)
explode[sizes.index(max(sizes))] = 0.1
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode = explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

html_file.close()

