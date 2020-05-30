from stat_functions import *

def run_statistics(senders, messages, dates, time_stats, messenger):
    user_stats = dict()
    total_msgs = 0

    # User stats
    for sender in senders:
        user_stats[sender] = dict()
        
        date_diff, st, en = biggest_date_difference(list(dates[sender].keys()))
        user_stats[sender]['biggest_date_difference'] = (date_diff, convert_date(st), convert_date(en))
        
        streak, st, en = longest_streak(list(dates[sender].keys()))
        user_stats[sender]['longest_streak'] = (streak, convert_date(st), convert_date(en))
        
        top_days = get_most_used(dates[sender], 10)[::-1]
        end = len(top_days)
        for i in range(len(top_days)):
            if top_days[i][0] == None:
                end = i
                break
            top_days[i] = (convert_date(top_days[i][0]), top_days[i][1])
        top_days = sorted(top_days[:end], key = lambda x: -x[1])
        user_stats[sender]['most_messages'] = top_days  
        
        count = sender_count(messages[sender])
        user_stats[sender]['total_messages'] = count
        total_msgs += count

    # Analyzing message contents

    ## Message, Word, Nudges Count
    total_nudges = 0
    for sender in senders:
        count = 0
        user_stats[sender]['word_count'] = 0
        if messenger == 'Hike':
            user_stats[sender]['nudges'] = 0
            audio = 0
            video = 0
        for m in messages[sender]:
            if messenger == "Whatsapp" and "<Media omitted>" in m:
                count += 1
            elif messenger == "Hike" and "File transfer of type" in m:
                if 'IMAGE' in m.split()[-1] :
                    count += 1
                elif 'AUDIO_RECORDING' in m.split()[-1]:
                    audio += 1
                elif 'VIDEO' in m.split()[-1]:
                    video += 1

            if messenger == 'Hike' and m.strip() == 'Nudge!':
                user_stats[sender]['nudges'] += 1
                total_nudges += 1
            user_stats[sender]['word_count'] += count_words(m)
        user_stats[sender]["media"] = count
        if messenger == "Hike":
            user_stats[sender]["audio"] = audio
            user_stats[sender]["video"] = video
    
    ## Emojis Count
    emoji_stats = get_emoji_stats(messages)
    for sender in emoji_stats:
        user_stats[sender]['fav_emojis'] = get_most_used(emoji_stats[sender], 5)

    ## Most used words
    for sender in messages:
        # print(sender, ":-")
        ans = get_most_used_words(messages[sender])
        # for word, count in ans:
        #     print(word, ":", count)
        # print()


    # Time Statistics
    for sender in time_stats['reply']:
        time_stats['reply'][sender]['avg'] = format_minutes(time_stats['reply'][sender]['avg'])
        time_stats['reply'][sender]['max_time'] = format_minutes(time_stats['reply'][sender]['max_time'])

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
    if messenger == 'Hike':
        overall_stats['total_nudges'] = total_nudges   
    return user_stats, overall_stats, time_stats