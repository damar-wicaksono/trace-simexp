"""Module to parse spacer grid data from the list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line: str) -> dict:
    r"""Parse spacer grid specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :returns: (list of dict) an updated params_dict with spacer specification
    """
    spacer_data = line.split()

    # Check the validity of the data
    check_spacer(spacer_data)

    spacer_dict = {
        "enum": int(spacer_data[0]),
        "data_type": "spacer",
        "var_num": int(spacer_data[2]),
        "var_name": spacer_data[3].lower(),
        "var_type": spacer_data[4].lower(),
        "var_mode": int(spacer_data[5]),
        "var_card": int(spacer_data[6]),
        "var_word": int(spacer_data[7]),
        "var_dist": spacer_data[8].lower(),
    }
    if spacer_dict["var_name"] == "spmatid":
        spacer_dict["var_par1"] = [int(_) for _ in spacer_data[9].split(",")]
        spacer_dict["var_par2"] = None
        spacer_dict["str_fmt"] = "14d"
    else:
        spacer_dict["var_par1"] = float(spacer_data[9])
        spacer_dict["var_par2"] = float(spacer_data[10])
        spacer_dict["str_fmt"] = spacer_data[11]

    # Add the message to be written in prepro.info
    spacer_dict["str_msg"] = create_msg(spacer_dict)

    return spacer_dict


def create_msg(spacer_dict: dict) -> str:
    """Create a string of parsed parameters

    :param spacer_dict: (dict) the parsed parameter specifications
    """
    from .common import var_type_str

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
    str_msg.append("Parameter distribution: *{}*"
                   .format(spacer_dict["var_dist"]))
    if spacer_dict["var_name"] == "spmatid":
        str_msg.append("1st distribution parameter: {}"
                       .format(spacer_dict["var_par1"]))
        str_msg.append("2nd distribution parameter: {}\n"
                       .format(spacer_dict["var_par2"]))
    else:
        str_msg.append("1st distribution parameter: {:.3f}"
                       .format(spacer_dict["var_par1"]))
        str_msg.append("2nd distribution parameter: {:.3f}\n"
                       .format(spacer_dict["var_par2"]))

    return "\n".join(str_msg)


def check_spacer(spacer_data):
    r"""Check the validity of the specified spacer grid data

    :param spacer_data: (list) list of specifications for spacer grid data
    """
    # Check the number of parameters in the data
    num_params = 12
    if spacer_data[3].lower() == "spmatid":
        if len(spacer_data) != num_params - 1:
            raise TypeError("The amount of information specified does not match."
                            "Required {}, supplied {}. check again!"
                            .format(num_params, len(spacer_data)))
    else:
        if len(spacer_data) != num_params:
            raise TypeError("The amount of information specified does not match."
                            "Required {}, supplied {}. check again!"
                            .format(num_params, len(spacer_data)))

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
    if int(spacer_data[6]) == 2:
        if not spacer_data[3].lower() in valid_names1:
            raise TypeError("the var_name *{}* is not a valid spacer "
                            "grid parameter names of card *{}*"
                            .format(spacer_data[3], spacer_data[5]))
        elif not int(spacer_data[7]) in [1, 2, 3, 4]:
            raise TypeError("The var_word *{}* is not a valid word "
                            "of grid parameters of card *{}*"
                            .format(spacer_data[6], spacer_data[5]))
        if spacer_data[3].lower() == "spbloc":
            if int(spacer_data[7]) != 1:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "vnbloc":
            if int(spacer_data[7]) != 2:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "phi":
            if int(spacer_data[7]) != 3:
                raise TypeError(err_msg)
        if spacer_data[4].lower() == "wetperm":
            if int(spacer_data[7]) != 4:
                raise TypeError(err_msg)

    elif int(spacer_data[6]) == 3:
        if not spacer_data[3].lower() in valid_names2:
            raise TypeError("the var_name *{}* is not a valid spacer "
                            "grid parameter names of card *{}*"
                            .format(spacer_data[3], spacer_data[5]))
        elif not int(spacer_data[7]) in [1, 2, 3]:
            raise TypeError("The var_word *{}* is not a valid word "
                            "of grid parameters of card *{}*"
                            .format(spacer_data[6], spacer_data[5]))
        if spacer_data[3].lower() == "height":
            if int(spacer_data[7]) != 1:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "strthick":
            if int(spacer_data[7]) != 2:
                raise TypeError(err_msg)
        if spacer_data[3].lower() == "spmatid":
            if int(spacer_data[7]) != 3:
                raise TypeError(err_msg)
            if spacer_data[8].lower() != "discunif":
                raise TypeError("Not appropriate distribution selected!")

    else:
        raise TypeError("Only 2 and 3 are valid choices!")

    # Check if the var_type is correct
    if not int(spacer_data[5]) in [1, 2, 3]:
        raise TypeError("The var_type *{}* is not supported"
                        .format(spacer_data[4]))