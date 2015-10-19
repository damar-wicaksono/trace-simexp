"""Module to write info file from parsing the command line
"""

__author__ = "Damar Wicaksono"


def make_filename(inputs_dict):
    r"""

    :param inputs_dict:
    :return:
    """

    if len(inputs_dict["samples"]) > 1:
        info_file = "info-{}-{}-{}-{}-{}.txt" \
            .format(inputs_dict["case_name"],
                    inputs_dict["params_list_name"],
                    inputs_dict["dm_name"],
                    inputs_dict["samples"][0],
                    inputs_dict["samples"][-1])
    else:
        info_file = "info-{}-{}-{}-{}" \
            .format(inputs_dict["case_name"],
                    inputs_dict["params_list_name"],
                    inputs_dict["dm_name"],
                    inputs_dict["samples"][0])

    return info_file
