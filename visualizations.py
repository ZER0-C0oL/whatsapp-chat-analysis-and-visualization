import matplotlib.pyplot as plt

def msgs_by_time(msg_stats):
    fig = plt.figure()
    plot = fig.add_subplot(111)
    ax = fig.add_axes([0,0,2,1])
    colors = ['b', 'g', 'r', 'm']
    ctr = 0
    time_val = [(ts + 3/2.0) + 0.25 * ctr for ts in range(24) if ts % 3 == 0]
    for sender in msg_stats:
        time_ranges = list(msg_stats[sender].keys())
        time_count = [msg_stats[sender][t] for t in time_ranges]
        ticks = time_val
        ax.bar(time_val,time_count, color = colors[ctr], width = 0.50, label = sender)
        if ctr == 0:
            ax.set_xticklabels(list(msg_stats[sender].keys()))
        ctr += 1
    plt.xticks(time_val)
    plt.xlabel("Time (24 hours)")
    plt.ylabel("Messages Sent")
    if len(msg_stats.keys()) > 1:
        plt.legend()
    plt.savefig("time_msg_viz.png")
    # plt.show()

def words_by_time(word_stats):
    fig = plt.figure()
    plot = fig.add_subplot(111)
    ax = fig.add_axes([0,0,2,1])
    colors = ['b', 'g', 'r', 'm']
    ctr = 0
    time_val = [(ts + 3/2.0) + 0.25 * ctr for ts in range(24) if ts % 3 == 0]
    for sender in word_stats:
        time_ranges = list(word_stats[sender].keys())
        time_count = [word_stats[sender][t] for t in time_ranges]
        ticks = time_val
        ax.bar(time_val,time_count, color = colors[ctr], width = 0.50, label = sender)
        if ctr == 0:
            ax.set_xticklabels(list(word_stats[sender].keys()))
        ctr += 1
    plt.xticks(time_val)
    plt.xlabel("Time (24 hours)")
    plt.ylabel("Words Sent")
    plt.legend()
    plt.savefig("time_words_viz.png")

def msg_chart(overall_stats):
    labels = []
    sizes = []
    for l, s in overall_stats['users']:
        sizes.append(s)
        labels.append(l + " (" + str(sizes[-1]) + ")")
    explode = [0.0] * len(labels)
    explode[sizes.index(max(sizes))] = 0.1
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode = explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig("msg_chart.png")

def word_chart(user_stats):
    labels = []
    sizes = []
    for sender in user_stats:
        sizes.append(user_stats[sender]['word_count'])
        labels.append(sender + " (" + str(sizes[-1]) + ")")
    explode = [0.0] * len(labels)
    explode[sizes.index(max(sizes))] = 0.1
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode = explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig("word_chart.png")


def create_visualizations(user_stats, overall_stats, time_stats):

    # Create Time-based Visualizations
    if len(time_stats['word_count'].keys()) <= 4:
        msgs_by_time(time_stats['word_count'])
        words_by_time(time_stats['msg_count'])
    
    # Create Count-based Visualizations
    msg_chart(overall_stats)
    word_chart(user_stats)

