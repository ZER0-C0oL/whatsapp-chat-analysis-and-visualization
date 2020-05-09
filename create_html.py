def create_html(senders, messages, dates):
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