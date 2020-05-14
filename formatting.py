from helper_functions import *

def convert_to_structured_format(chat, date_format, messenger):
    senders = set()      # To mark whether a message traversed is from a new sender or old
    messages = dict()    # Store all messages in structured format
    dates = dict()       # Store all dates in structures format
    time_stats = dict()
    time_stats['word_count'] = dict()
    time_stats['msg_count'] = dict()
    last = None
    
    for msg in chat:
        date_time, sender, content = extract_components(msg, date_format, messenger)
        if date_time == None:
            if last != None:
                messages[last][-1] += msg   # Newline in previous msg, must be appended to last message
                continue
            else:
                continue    # Description at beginning of chat(not important)
        last = sender
        sender = sender.strip()
        content = content.strip()
        # Adding data
        if sender not in senders:
            senders.add(sender)
            messages[sender] = [content]
            dates[sender] = dict()
            time_stats['word_count'][sender] = get_time_dict()
            time_stats['msg_count'][sender] = get_time_dict()
        else:
            messages[sender].append(content)
        
        date = date_time.date()
        if date in dates[sender]:
            dates[sender][date] += 1
        else:
            dates[sender][date] = 1
        time_stats['word_count'][sender][get_key(date_time.hour)] += content.count(' ') + 1
        time_stats['msg_count'][sender][get_key(date_time.hour)] += 1
                
        last = sender

    return senders, messages, dates, time_stats