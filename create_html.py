from date_functions import convert_date

def create_html_page(senders, user_stats, overall_stats):
    from markdown import markdown as md

    html_file = open('analysis.html', mode = 'w', encoding = 'utf-8', errors = 'xmlcharrefreplace')

    html_file.write(md("## Overall Statistics"))
        
    html_file.write(md("#### Most active participants"))

    ctr = 1
    for s, c in overall_stats['users'][:min(10,len(overall_stats['users']))]:
        html_file.write(md("{}\. {}: {} messages ({}%)".format(ctr, s, c, int((c/overall_stats['total_msgs']) * 100))))
        ctr += 1
        
    html_file.write('\n\n')
    html_file.write(md("#### Most active days"))
    for day, count in overall_stats['dates'][:min(5, len(overall_stats['dates']))]:
        html_file.write(md("> - {}: {} messages".format(convert_date(day), count)))

    html_file.write('\n\n\n\n\n')

    html_file.write(md("## User Statistics"))
    for ctr, sender in enumerate(senders,1):
        html_file.write(md("#### {}. {}".format(ctr, sender)))
        html_file.write(md("* Total Messages: {}".format(user_stats[sender]['total_messages'])))
        html_file.write(md("* Media Sent: {}".format(user_stats[sender]['media'])))
        html_file.write(md("* Top most active days:-"))
        for day, count in user_stats[sender]['most_messages']:
            html_file.write(md("{}> {}: {} messages".format(' '*10,day, count)))
        c, s, e = user_stats[sender]['longest_streak']
        html_file.write(md("* Longest Streak: {} days (from {} to {})".format(c,s,e)))
        c, s, e = user_stats[sender]['biggest_date_difference']
        html_file.write(md("* Longest Span without messages: {} days (from {} to {})".format(c,s,e)))
    
    html_file.close()