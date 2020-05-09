import sys
from create_statistics import run_statistics
from formatting import convert_to_structured_format
from create_html import create_html_page
file_path = sys.argv[1]

chat = []
with open(file_path, mode = 'r', encoding = 'utf-8') as f:
    chat.extend(f.readlines())

senders, messages, dates = convert_to_structured_format(chat)
user_stats, overall_stats = run_statistics(senders, messages, dates)
create_html_page(senders, user_stats, overall_stats)