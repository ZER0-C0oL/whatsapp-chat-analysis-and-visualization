import sys
from create_statistics import run_statistics
from formatting import convert_to_structured_format
from create_html import create_html_page
from visualizations import create_visualizations

file_path = sys.argv[1]
if len(sys.argv) > 2:
    date_format = sys.argv[2]
    messenger = sys.argv[3]
else:
    date_format = "dd/mm/yy"
    messenger = "Whatsapp"

chat = []
with open(file_path, mode = 'r', encoding = 'utf-8') as f:
    chat.extend(f.readlines())

senders, messages, dates, time_stats = convert_to_structured_format(chat, date_format, messenger)
user_stats, overall_stats, time_stats = run_statistics(senders, messages, dates, time_stats, messenger)
create_visualizations(user_stats, overall_stats, time_stats)
create_html_page(user_stats, overall_stats, time_stats, file_path)