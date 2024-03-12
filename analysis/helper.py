# Variables
remove_from_start = 1
remove_from_end = 1
num_lifetime_cycles = 1000

custom_range = False
custom_start = 1  # Starting at cycle N
custom_num_cycles = 1  # Number of cycles to include


def cut_off_step(data):
    # Viewing N cycles
    if custom_range:
        start = remove_from_start * 2 + custom_start * 2
        end = start + custom_num_cycles * 2
        data = data[start:end, :]

    # Cut off cycles
    else:
        data = data[(remove_from_start * 2) : (len(data) - remove_from_end * 2), :]

    return data


def cut_off_record(data):
    # Cut off cycles
    # - Use the column "Cycle Count" (column 0), remove the first and last N cycles
    # - For first n, if "Cycle Count" value <= remove_from_start, remove it
    # - For last n, if "Cycle Count" value > (max - remove_from_end), remove it
    max_cycle = data[-1, 0]

    # Viewing N cycles
    if custom_range:
        start = 0
        end = 0
        for i in range(len(data[:, 0])):
            if start == 0 and data[i, 0] == custom_start:
                start = i
            elif data[i, 0] == (custom_start + custom_num_cycles + 1):
                end = i - 1
                break

    else:
        for i in range(len(data[:, 0])):
            if data[i, 0] <= remove_from_start:
                start = i
            if data[i, 0] > (max_cycle - remove_from_end):
                end = i - 1
                break

    return data[start:end, :]


def cut_off_cycle(data):
    # Viewing N cycles
    if custom_range:
        start = remove_from_start + custom_start
        end = start + custom_num_cycles
        data = data[start:end, :]

    # Cut off cycles
    else:
        data = data[remove_from_start : (len(data) - remove_from_end), :]

    return data
