import sys
file_path = sys.argv[0]

chat = ''
with open(file_path, mode = 'r', encoding = 'utf-8') as f:
    chat = f.readlines() 

senders, messages, dates = convert_to_structured_format(chat)
user_stats, overall_stats = run_statistics(senders, messages, dates)
analyze_and_create_html(user_stats, overall_stats)