# Importing the matplotlib.pyplot
import random

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def draw_chart(items):
    gantt_by_id = {}

    for item in items:
        if item[2] not in gantt_by_id:
            gantt_by_id[item[2]] = [(item[0], item[1])]
        else:
            gantt_by_id[item[2]].append((item[0], item[1]))

    fig, ax = plt.subplots(figsize=(10, 4))  # Adjust the figure size as needed

    y_coordinate = 0.25  # Fixed y-coordinate for all tasks

    for key, intervals in gantt_by_id.items():
        for interval in intervals:
            start, end = interval
            ax.barh(y_coordinate, width=end - start, left=start, color=f'C{key}', edgecolor='black', height=0.1)

    ax.set_xlabel('Time')
    ax.set_title('Gantt Chart')
    ax.set_ylim(0, 0.5)  # Adjust the y-axis limit
    ax.invert_yaxis()  # Invert y-axis to have task 0 at the top
    ax.set_xticks(range(0 - 4, int(max(end for intervals in gantt_by_id.values() for _, end in intervals) + 4), 2))
    ax.grid(True)

    plt.savefig("gantt1.png")
    # plt.show()
