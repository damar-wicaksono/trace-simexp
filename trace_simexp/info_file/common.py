"""Common module for info_file package
"""

__author__ = "Damar Wicaksono"


def make_filename(inputs: dict, flag: str) -> str:
    """Create a string of filename for the info file

    The function is called by default, if no custom filename is specified

    :param inputs: (dict) the required inputs for execute phase in a dictionary
    :param flag: (str) the info file flag: prepro, exec, or postpro
    :return: (str) the filename as string
    """

    if len(inputs["samples"]) > 1:
        info_file = "{}-{}-{}-{}-{}-{}" \
            .format(flag,
                    inputs["case_name"],
                    inputs["params_list_name"],
                    inputs["dm_name"],
                    inputs["samples"][0],
                    inputs["samples"][-1])
    else:
        info_file = "{}-{}-{}-{}-{}" \
            .format(flag,
                    inputs["case_name"],
                    inputs["params_list_name"],
                    inputs["dm_name"],
                    inputs["samples"][0])

    # if postpro.info, additional id for list of graphic variable names
    if flag == "postpro":
        info_file = "{}-{}.info" .format(info_file, inputs["xtv_vars_name"])
    else:
        info_file = "{}.info" .format(info_file)

    return info_file

