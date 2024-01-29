# Variables
num_pre_cycles = 4
num_lifetime_cycles = 1000
include_pre_cycles = True
remove_from_end = 1

custom_range = True
custom_start = 0  # Starting at cycle N
custom_num_cycles = 6  # Number of cycles to include


def cut_off_step(data):
    # Cut off pre-cycles
    start = 0
    if not include_pre_cycles:
        start = num_pre_cycles * 2
        data = data[start:-remove_from_end, :]

    # Viewing N cycles
    if custom_range:
        if not include_pre_cycles:
            start += num_pre_cycles * 2
        start += custom_start * 2
        end = start + custom_num_cycles * 2
        data = data[start:end, :]

    return data


def cut_off_record(data):
    # Cut off pre-cycles
    if not include_pre_cycles:
        start = 0
        end = 0
        # Find index of first cycle count of pre_cycles + 1
        # Last index is just the cycle before the last cycle. For example, 1003 if there are 1000 lifetime cycles and 4 pre-cycles
        # Cycle count is last column
        for i in range(len(data[:, -1])):
            if start == 0 and data[i, -1] == (num_pre_cycles + 1):
                start = i
            elif data[i, -1] == (num_pre_cycles + num_lifetime_cycles):
                end = i
                break
        data = data[start:end, :]

    # Viewing N cycles
    if custom_range:
        # Find first index of first cycle count of custom_start + 1
        # Find last index of first cycle count of custom_start + custom_num_cycles + 1
        # Cycle count is last column
        start = 0
        end = 0
        for i in range(len(data[:, -1])):
            if start == 0 and data[i, -1] == (custom_start + 1):
                start = i
            elif data[i, -1] == (custom_start + custom_num_cycles + 1):
                end = i
                break
        data = data[start:end, :]

    return data


def cut_off_cycle(data):
    # Cut off pre-cycles
    start = 0
    if not include_pre_cycles:
        start = num_pre_cycles
        data = data[start:-remove_from_end, :]

    # Viewing N cycles
    if custom_range:
        if not include_pre_cycles:
            start += num_pre_cycles + 1
        start += custom_start
        end = start + custom_num_cycles
        data = data[start:end, :]

    return data
