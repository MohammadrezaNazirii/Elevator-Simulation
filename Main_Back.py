import copy
import math
from Gantt import *

algorithm = ''
inputs = []
time_quantum = 0
speed = 1
floor_distance = 1
floors = 0


def initialize(alg, floors_n, tq=0):
    global algorithm
    global time_quantum
    global floors

    algorithm = alg
    floors = floors_n
    time_quantum = tq


def get_inputs(input_arr):
    global inputs

    print(input_arr)

    for i in input_arr:
        inputs.append(i)


def get_output(sorted_arr, mode='non-preemptive', n=0):
    elapsed_time = (sorted_arr[0][0])

    current_floor = 0

    output = [(-elapsed_time if elapsed_time != 0 else 0)]

    times = []

    if mode == 'preemptive':
        waits = [0 for i in range(n)]
    else:
        waits = []

    for i in range(len(sorted_arr)):

        if elapsed_time < sorted_arr[i][0] and i != 0:
            wait_time = elapsed_time - sorted_arr[i][0]
            elapsed_time += -wait_time
            output.append(wait_time)

        output.append(sorted_arr[i][1])
        # time to wait in a floor
        output.append(sorted_arr[i][2])

        elapsed_time += abs((sorted_arr[i][1] - current_floor)) / speed

        times.append([elapsed_time])
        # adds elapsed_time (here means start of process) to wait times
        if mode == 'preemptive':
            waits[sorted_arr[i][3]] += elapsed_time - sorted_arr[i][0]
        else:
            waits.append(elapsed_time - sorted_arr[i][0])

        current_floor = sorted_arr[i][1]

        elapsed_time += abs((sorted_arr[i][2] - current_floor)) / speed

        times[i].append(elapsed_time)
        times[i].append(sorted_arr[i][3])

        current_floor = sorted_arr[i][2]

    return output, elapsed_time, waits, times


def sort_sjf(sorted_arr):
    burst = []
    time = 0
    travel = []
    i = 0
    waiting = []
    curent = 0

    res = []

    while sorted_arr:

        mini = 10000
        index = 0
        flag = 0
        for j in range(len(sorted_arr)):
            if sorted_arr[j][0] > time:
                break
            if sorted_arr[j][2] - sorted_arr[j][1] < mini:
                mini = sorted_arr[j][2] - sorted_arr[j][1]
                index = j
                flag = 1

        if flag == 0:
            index = 0

        temp = 0
        burst += [abs(sorted_arr[index][2] - sorted_arr[index][1])]
        travel += [sorted_arr[index][1]]
        travel += [sorted_arr[index][2]]

        if i == 0:
            waiting += [abs(curent - sorted_arr[0][1])]
            # time+= waiting[0]
        else:
            if sorted_arr[index][0] > time:
                # idle += sorted_arr[index][0] - time
                time = sorted_arr[index][0]
            else:
                temp = time - sorted_arr[index][0]

            waiting += [abs(curent - sorted_arr[index][1]) + temp]  # 3

        time += burst[i] + waiting[i] - temp
        curent = sorted_arr[index][2]
        # end += [time]
        res.append(sorted_arr[index])
        sorted_arr.pop(index)
        i += 1

    return res


def run():
    global inputs
    global algorithm

    output = []

    if algorithm == 'FCFS':

        sorted_arr = sorted(inputs, key=lambda _: _[0])

        # Give id to each process
        for i in range(len(sorted_arr)):
            sorted_arr[i].append(i)

        output, elapsed_time, waits, times = get_output(sorted_arr)

        draw_chart(times)

        return output

    elif algorithm == 'SJF':

        sorted_arr = inputs

        sorted_arr = sorted(inputs, key=lambda _: _[0])

        sort_sjf(sorted_arr)

        # Give id to each process
        for i in range(len(sorted_arr)):
            sorted_arr[i].append(i)

        output, elapsed_time, waits, times = get_output(sorted_arr)

        draw_chart(times)

        return output

    elif algorithm == "RR":

        sorted_arr = sorted(inputs, key=lambda _: _[0])

        n = len(sorted_arr)

        res = []

        # Give id to each process
        for i in range(len(sorted_arr)):
            sorted_arr[i].append(i)

        for entry in sorted_arr:

            checking = entry

            current_floor = 0

            while checking[2] - checking[1] > time_quantum:
                temp = [checking[0], checking[1], checking[1] + time_quantum, entry[3]]

                res.append(temp)

                checking[1] = temp[2]
                checking[0] += (temp[2] - current_floor) / speed

                current_floor = temp[2]

            res.append([checking[0], checking[1], entry[2], entry[3]])

        sorted_arr = sorted(res, key=lambda _: _[0])

        output, elapsed_time, waits, times = get_output(sorted_arr, 'preemptive', n)

        print(waits)

        draw_chart(times)

        return output

    elif algorithm == 'SRTF':

        sorted_arr = inputs

        # Give id to each process
        for i in range(len(sorted_arr)):
            sorted_arr[i].append(i)

        n = len(sorted_arr)

        sort_sjf(sorted_arr)

        res = []

        remaining_process = len(sorted_arr)

        floor_time = floor_distance / speed

        elapsed_time = sorted_arr[0][0]

        current_floor = 0

        while remaining_process > 0:

            running = sorted_arr[0]

            elapsed_time += abs(running[1] - current_floor) / speed

            start_range = elapsed_time

            run_direction = 'up' if running[2] - running[1] > 0 else 'down'

            # elapsed_time = running[0]

            end_range = (abs(running[2] - running[1]) / speed) + start_range

            preempted = False

            # end_range = (abs(running[2]-running[1]) / speed)+running[0]
            # run_range = (running[0], (running[2]-running[1])+running[0])

            for check_in in range(1, len(sorted_arr)):

                arr_time = sorted_arr[check_in][0]

                if start_range < arr_time < end_range:

                    elapsed_floor = math.ceil((arr_time - start_range) / floor_time)

                    elapsed_time = start_range + (elapsed_floor / speed)

                    remaining = abs(running[2] - running[1]) - elapsed_floor

                    next_process = sorted_arr[check_in]

                    if next_process[2] - next_process[1] < remaining:
                        sorted_arr.pop(0)

                        res.append([running[0], running[1], running[1] + elapsed_floor, running[3]])

                        current_floor = running[1] + (+elapsed_floor if run_direction == 'up' else -elapsed_floor)

                        sorted_arr.append([arr_time, current_floor, running[2], running[3]])

                        sort_sjf(sorted_arr)

                        preempted = True

                        break

            if not preempted:
                res.append(sorted_arr[0])

                sorted_arr.pop(0)

                remaining_process -= 1

        output, elapsed_time, waits, times = get_output(res, 'preemptive', n)

        print(waits)

        draw_chart(times)

        return output
