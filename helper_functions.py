def find_nth_occurence(string, substring, occurence):
    last = -1
    for _ in range(occurence):
        try:
            last = string.find(substring, last + 1)
            if last == -1:
                return -1
        except:
            return None
    return last

def get_time_dict():
    d = dict()
    for i in range(24):
        if i % 3 == 0:
            key = str(i) + ' - ' + str(i+3)
            d[key] = 0
    return d

def get_key(t):
    ts = (t//3) * 3
    key = str(ts) + ' - ' + str(ts+3)
    return key

def extract_components(msg, date_format, messenger):
    from dateutil import parser
    try:
        if messenger == "Hike":
            end = find_nth_occurence(msg, ":", 3)
            if end == -1:
                return (None,) * 3
            msg_start = msg.find("-", end+1)
            if msg_start == -1:
                return (None,) * 3
            sender = msg[end+1:msg_start]
            content = msg[msg_start+1:-1]
            if content == "":
                return (None,) * 3
            date_time = None
            if date_format == "dd/mm/yy":
                date_time = parser.parse(msg[:end], dayfirst = True)
            else:
                date_time = parser.parse(msg[:end])
            return date_time, sender, content
        elif messenger == "Whatsapp":
            end = msg.index("-")
            if end == -1:
                return (None,) * 3
            msg_start = msg.find(":", end+1)
            if msg_start == -1:
                return (None,) * 3
            sender = msg[end+1: msg_start]
            content = msg[msg_start+1:-1]
            if content == "":
                return (None,) * 3
            date_time = None
            if date_format == "dd/mm/yy":
                date_time = parser.parse(msg[:end].replace(",", ""), dayfirst = True)
            else:
                date_time = parser.parse(msg[:end].replace(",", ""))
            return date_time, sender, content
    except:
        return (None,) * 3