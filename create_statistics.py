from stat_functions import biggest_date_difference, longest_streak, most_messages_per_day, sender_count
from date_functions import convert_date

def run_statistics(senders, messages, dates):
    user_stats = dict()
    total_msgs = 0

    # General stats
    for sender in senders:
        user_stats[sender] = dict()
        
        date_diff, st, en = biggest_date_difference(list(dates[sender].keys()))
        user_stats[sender]['biggest_date_difference'] = (date_diff, convert_date(st), convert_date(en))
        
        streak, st, en = longest_streak(list(dates[sender].keys()))
        user_stats[sender]['longest_streak'] = (streak, convert_date(st), convert_date(en))
        
        top3 = most_messages_per_day(dates[sender])[::-1]
        for i in range(len(top3)):
            top3[i][0] = convert_date(top3[i][0])
        user_stats[sender]['most_messages'] = top3
        
        count = sender_count(messages[sender])
        user_stats[sender]['total_messages'] = count
        total_msgs += count

    # Analyzing message contents
    for sender in senders:
        count = 0
        for m in messages[sender]:
            if "<Media omitted>" in m:
                count += 1
        user_stats[sender]["media"] = count

    # Overall Statistics
    participants = []
    for sender in senders:
        participants.append([sender, user_stats[sender]['total_messages']])
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

    overall_stats = dict()
    overall_stats['users'] = participants
    overall_stats['dates'] = date_count
    overall_stats['total_msgs'] = total_msgs

    return user_stats, overall_stats