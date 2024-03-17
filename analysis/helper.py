def cut_off_step(data, helper_parameters):
    (
        remove_from_start,
        remove_from_end,
        custom_range,
        custom_start,
        custom_num_cycles,
    ) = (
        helper_parameters["remove_from_start"],
        helper_parameters["remove_from_end"],
        helper_parameters["custom_range"],
        helper_parameters["custom_start"],
        helper_parameters["custom_num_cycles"],
    )

    # Viewing N cycles
    if custom_range:
        start = remove_from_start * 2 + custom_start * 2
        end = start + custom_num_cycles * 2
        data = data[start:end, :]

    # Cut off cycles
    else:
        data = data[(remove_from_start * 2) : (len(data) - remove_from_end * 2), :]

    return data


def cut_off_record(data, helper_parameters):
    (
        remove_from_start,
        remove_from_end,
        custom_range,
        custom_start,
        custom_num_cycles,
    ) = (
        helper_parameters["remove_from_start"],
        helper_parameters["remove_from_end"],
        helper_parameters["custom_range"],
        helper_parameters["custom_start"],
        helper_parameters["custom_num_cycles"],
    )

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
            elif data[i, 0] == (custom_start + custom_num_cycles):
                end = i
                break

    else:
        for i in range(len(data[:, 0])):
            if data[i, 0] <= remove_from_start:
                start = i
            if data[i, 0] > (max_cycle - remove_from_end):
                end = i - 1
                break

    return data[start:end, :]


def cut_off_cycle(data, helper_parameters):
    (
        remove_from_start,
        remove_from_end,
        custom_range,
        custom_start,
        custom_num_cycles,
    ) = (
        helper_parameters["remove_from_start"],
        helper_parameters["remove_from_end"],
        helper_parameters["custom_range"],
        helper_parameters["custom_start"],
        helper_parameters["custom_num_cycles"],
    )

    # Viewing N cycles
    if custom_range:
        start = remove_from_start + custom_start
        end = start + custom_num_cycles
        data = data[start:end, :]

    # Cut off cycles
    else:
        data = data[remove_from_start : (len(data) - remove_from_end), :]

    return data
