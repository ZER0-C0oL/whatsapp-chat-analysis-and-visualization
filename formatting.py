from helper_functions import *

def convert_to_structured_format(chat, date_format, messenger):
    senders = set()                         # To mark whether a message traversed is from a new sender or old
    messages = dict()                       # Store all messages in structured format
    dates = dict()                          # Store all dates in structures format
    time_stats = dict()                     # Store statistics based on time of messages
    time_stats['word_count'] = dict()
    time_stats['msg_count'] = dict()
    time_stats['reply'] = dict()

    # Helper variables
    last = None
    last_time = None
    sess_len = 1
    sess_date = None
    max_sess_len = 0
    max_sess_date = None
    
    for msg in chat:
        date_time, sender, content = extract_components(msg, date_format, messenger)

        # Checking corner cases
        if date_time == None:
            if last != None:
                messages[last][-1] += msg   # Newline in previous msg, must be appended to last message
                continue
            else:
                continue    # Description at beginning of chat(not important)

        # Adding data
        sender = sender.strip()
        content = content.strip()
        if "Your messages and calls are secured with 128-bit encryption" in content or "added you as a friend" in content:
            continue
        if sender not in senders:
            # Initializing all structures
            senders.add(sender)
            messages[sender] = [content]
            dates[sender] = dict()
            time_stats['word_count'][sender] = get_time_dict()
            time_stats['msg_count'][sender] = get_time_dict()
            time_stats['reply'][sender] = dict()
            time_stats['reply'][sender]['avg'] = 0
            time_stats['reply'][sender]['rep_count'] = 0
            time_stats['reply'][sender]['max_time'] = 0
        else:
            messages[sender].append(content)

        # Adding time stats    
        if last_time != None:
            difference = (date_time - last_time).total_seconds() // 60
            if difference <= 60:
                sess_len += 1
                sess_date = date_time.date()
            else:
                if sess_len > max_sess_len:
                    max_sess_len = sess_len
                    max_sess_date = sess_date
                sess_len = 1
            if last != sender:
                avg = time_stats['reply'][sender]['avg']
                total = time_stats['reply'][sender]['rep_count']
                curr = time_stats['reply'][sender]['max_time']
                time_stats['reply'][sender]['avg'] = ((avg * total) + difference) / (total+1)
                time_stats['reply'][sender]['rep_count'] += 1
                time_stats['reply'][sender]['max_time'] = max(curr, difference)
        last = sender
        last_time = date_time        
        
        date = date_time.date()
        if date in dates[sender]:
            dates[sender][date] += 1
        else:
            dates[sender][date] = 1
        time_stats['word_count'][sender][get_key(date_time.hour)] += content.count(' ') + 1
        time_stats['msg_count'][sender][get_key(date_time.hour)] += 1
                
        last = sender
    
    time_stats['longest_session'] = dict()
    time_stats['longest_session']['length'] = max_sess_len
    time_stats['longest_session']['date'] = max_sess_date

    return senders, messages, dates, time_stats