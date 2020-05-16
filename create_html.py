from stat_functions import convert_date
import random

def extract_name(path):
    e = path.rfind('.')
    s = path.rfind('/')
    return path[s+1:e]

def create_html_page(user_stats, overall_stats, time_stats, file_path):
    from markdown import markdown as md
    name = './output/analysis_of_' + extract_name(file_path) + str(random.randint(0,1000)) + '.html'
    print(name)
    html_file = open(name, mode = 'w', encoding = 'utf-8', errors = 'xmlcharrefreplace')
    # html_file.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">')
    # html_file.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>')
    # html_file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>')
    # html_file.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>')
    # html_file.write("<div style='padding=40px;'>")
    html_file.write(md("## Overall Statistics"))

    html_file.write(md("#### Total Messages: {}".format(overall_stats['total_msgs'])))
    if 'total_nudges' in overall_stats:
        html_file.write(md("#### Total Nudges: {}".format(overall_stats['total_nudges'])))

        
    html_file.write(md("#### Most active participants"))

    ctr = 1
    for s, c in overall_stats['users'][:min(10,len(overall_stats['users']))]:
        html_file.write(md("{}\. {}: {} messages ({}%)".format(ctr, s, c, int((c/overall_stats['total_msgs']) * 100))))
        ctr += 1
    html_file.write('<br>')
    html_file.write(md("#### Most active days"))
    for day, count in overall_stats['dates'][:min(5, len(overall_stats['dates']))]:
        html_file.write(md("> - {}: {} messages".format(convert_date(day), count)))
    
    html_file.write(md("#### Longest Session: {} messages in one session on {}".format(time_stats['longest_session']['length'], convert_date(time_stats['longest_session']['date']))))

    # Encoding images into base64 to crate self-maintained webpage
    import base64
    html_file.write(md("#### Message Distribution"))
    with open("output/images/msg_chart.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode('ascii')
        html_file.write("<img src = 'data:image/png;base64,{0}'><br>".format(encoded))
    html_file.write(md("#### Words Distribution"))
    with open("output/images/word_chart.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode('ascii')
        html_file.write("<img src = 'data:image/png;base64,{0}'><br>".format(encoded))

    if len(user_stats.keys()) <= 4:
        html_file.write(md("#### Message Activity"))
        with open("output/images/time_msg_viz.png", "rb") as img:
            encoded = base64.b64encode(img.read()).decode('ascii')
            html_file.write("<img src = 'data:image/png;base64,{0}'><br>".format(encoded))
        html_file.write(md("#### Words Activity"))
        with open("output/images/time_words_viz.png", "rb") as img:
            encoded = base64.b64encode(img.read()).decode('ascii')
            html_file.write("<img src = 'data:image/png;base64,{0}'><br>".format(encoded))


    html_file.write("<br><br><br>")

    html_file.write(md("## User Statistics"))
    for ctr, sender in enumerate(list(user_stats.keys()),1):
        html_file.write(md("<details><summary> {}. {} </summary>".format(ctr, sender)))
        html_file.write(md("* Total Messages: {}".format(user_stats[sender]['total_messages'])))
        if 'nudges' in user_stats[sender]:
            html_file.write(md("* Total Nudges: {}".format(user_stats[sender]['nudges'])))
        html_file.write(md("* Media Sent: {}".format(user_stats[sender]['media'])))
        if 'audio' in user_stats[sender]:
            html_file.write(md("* Voice Notes: {}".format(user_stats[sender]['audio'])))
            html_file.write(md("* Videos Sent: {}".format(user_stats[sender]['video'])))
        html_file.write(md("* Total Words: {}".format(user_stats[sender]['word_count'])))
        html_file.write(md("* Top most active days:-"))
        for day, count in user_stats[sender]['most_messages']:
            html_file.write(md("{}> {}: {} messages".format(' '*10,day, count)))
        html_file.write(md("* Favorite emojis:-"))
        for emoji, count in user_stats[sender]['fav_emojis']:
            html_file.write(md("{}> {}: Used {} times".format(' '*10, emoji, count)))
        html_file.write(md("* Average Reply Time : {}".format(time_stats['reply'][sender]['avg'])))
        html_file.write(md("* Maximum Reply Time : {}".format(time_stats['reply'][sender]['max_time'])))
        # html_file.write(md("Total Replies : {}".format(time_stats['reply'][sender]['rep_count'])))
        c, s, e = user_stats[sender]['longest_streak']
        html_file.write(md("* Longest Streak: {} days (from {} to {})".format(c,s,e)))
        c, s, e = user_stats[sender]['biggest_date_difference']
        html_file.write(md("* Longest Span without messages: {} days (from {} to {})".format(c,s,e)))
        html_file.write(md("</details>"))
    html_file.write("<br><br><br>")
    # html_file.write("</div>")
    html_file.close()
