# -*- coding: utf-8 -*-
"""
    trace_simexp.paramfile.spacer
    *****************************

    Module to parse spacer grid related parameter specification from the list
    of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line: str) -> dict:
    r"""Parse spacer grid specification from a list of parameters file

    :param line: a line read from list of parameters file
    :returns: a dictionary of spacer grid parameter specification
    """
    from .common import parse_var_params

    spacer_data = line.split()

    # Check the validity of the data
    check_spacer(spacer_data)

    spacer_dict = {
        "enum": int(spacer_data[0]),
        "data_type": "spacer",
        "var_num": int(spacer_data[2]),
        "var_name": spacer_data[3].lower(),
        "var_type": spacer_data[4].lower(),
        "var_card": int(spacer_data[5]),
        "var_word": int(spacer_data[6]),
        "var_mode": int(spacer_data[7]),
        "var_dist": spacer_data[8].lower(),
        "var_pars": parse_var_params(line),
        "str_fmt": spacer_data[-1]
    }

    # Add the message to be written in prepro.info
    spacer_dict["str_msg"] = create_msg(spacer_dict)

    return spacer_dict


def create_msg(spacer_dict: dict) -> str:
    """Create a string of parsed parameters

    :param spacer_dict: (dict) the parsed parameter specifications
    """
    from .common import var_type_str
    from .common import print_var_params
    
    str_msg = list()

    str_msg.append("***{:2d}***" .format(spacer_dict["enum"]))
    str_msg.append("Spacer grid with Grid ID *{}*, parameter *{}* is "
                   "specified" .format(spacer_dict["var_num"],
                                       spacer_dict["var_name"]))
    str_msg.append("Parameter type: {}"
                   .format((spacer_dict["var_type"])))
    str_msg.append("Parameter perturbation mode: {} ({})"
                   .format(spacer_dict["var_mode"],
                           var_type_str(spacer_dict["var_mode"])))
    str_msg.append("Perturbation factor probability distribution:")
    str_msg.append(" - distribution: *{}*"
                   .format(spacer_dict["var_dist"]))
    str_msg.append("{}\n" .format(print_var_params(spacer_dict["var_pars"])))

    return "\n".join(str_msg)


def check_spacer(spacer_data: list):
    r"""Check the validity of the specified spacer grid data

    :param spacer_data: list of specifications for spacer grid parameter
    """
    # Check the variable type
    if spacer_data[4].lower() != "scalar":
        raise TypeError("Only scalar type is supported for spacer grid!")

    # Currently supported valid names of spacer grid parameters
    valid_names1 = ["spbloc", "vnbloc", "phi", "wetperm"]
    valid_names2 = ["height", "strthick", "spmatid"]

    # Make predefined error messages
    err_msg = "The var_name *{}* does not correspond to var_word *{}* in " \
              "spacer grid parameter of card *{}*"\
        .format(spacer_data[3], spacer_data[6], spacer_data[5])

    # Check the card choice and variable/parameter names
    if int(spacer_data[5]) == 2:
        if not spacer_data[3].lower() in valid_names1:
            raise TypeError("the var_name *{}* is not a valid spacer "
                            "grid parameter names of card *{}*"
                            .format(spacer_data[3], spacer_data[5]))
        elif not int(spacer_data[6]) in [1, 2, 3, 4]:
            raise TypeError("The var_word *{}* is not a valid word "
                            "of grid parameters of card *{}*"
                            .format(spacer_data[6], spacer_data[5]))
        if spacer_data[3].lower() == "spbloc":
            if int(spacer_data[6]) != 1:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "vnbloc":
            if int(spacer_data[6]) != 2:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "phi":
            if int(spacer_data[6]) != 3:
                raise TypeError(err_msg)
        if spacer_data[4].lower() == "wetperm":
            if int(spacer_data[6]) != 4:
                raise TypeError(err_msg)

    elif int(spacer_data[5]) == 3:
        if not spacer_data[3].lower() in valid_names2:
            raise TypeError("the var_name *{}* is not a valid spacer "
                            "grid parameter names of card *{}*"
                            .format(spacer_data[3], spacer_data[5]))
        elif not int(spacer_data[7]) in [1, 2, 3]:
            raise TypeError("The var_word *{}* is not a valid word "
                            "of grid parameters of card *{}*"
                            .format(spacer_data[6], spacer_data[5]))
        if spacer_data[3].lower() == "height":
            if int(spacer_data[6]) != 1:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "strthick":
            if int(spacer_data[6]) != 2:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "spmatid":
            if int(spacer_data[6]) != 3:
                print(spacer_data)
                raise TypeError(err_msg)
            if spacer_data[8].lower() != "discrete":
                raise TypeError("Not appropriate distribution selected!")

    else:
        raise TypeError("Only 2 and 3 are valid choices!")

    # Check if the var_type is correct
    if not int(spacer_data[5]) in [1, 2, 3]:
        raise TypeError("The var_type *{}* is not supported"
                        .format(spacer_data[4]))
