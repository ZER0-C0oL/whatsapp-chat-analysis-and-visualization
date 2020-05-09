def convert_to_structured_format(chat):
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
    
    return senders, messages, dates