"""Module to parse spacer grid data from the list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse_spacer(line, params_dict, verbose=True):
    r"""Parse spacer grid specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with spacer specification
    """
    spacer_data = line.split()
    check_parse(spacer_data)
    spacer_dict = {
        "data_type": "spacer",
        "num": spacer_data[2],
        "var_name": spacer_data[3].lower(),
        "var_type": spacer_data[4],
        "var_card": int(spacer_data[5]),
        "var_word": int(spacer_data[6]),
        "var_dist": spacer_data[7],
    }
    if spacer_dict["var_name"] == "spmatid":
        spacer_dict["var_par1"] = spacer_data[8].split(",")
        spacer_dict["var_par2"] = None
    else:
        spacer_dict["var_par1"] = float(spacer_data[8])
        spacer_dict["var_par2"] = float(spacer_data[9])

    params_dict.append(spacer_dict)

    if verbose:
        print("***{:2d}***" .format(int(spacer_data[0])))
        print("Spacer grid with Grid ID *{}*, parameter *{}* is specified"
              .format(spacer_dict["num"], spacer_dict["var_name"]))
        print("Parameter distribution is *{}*"
              .format(spacer_dict["var_dist"]))
        if spacer_dict["var_name"] == "spmatid":
            print("1st distribution parameter: {}"
                  .format(spacer_dict["var_par1"]))
            print("2nd distribution parameter: {}"
              .format(spacer_dict["var_par2"]))
        else:
            print("1st distribution parameter: {:.3f}"
                  .format(spacer_dict["var_par1"]))
            print("2nd distribution parameter: {:.3f}"
              .format(spacer_dict["var_par2"]))



def check_parse(spacer_data):
    r"""Check the validity of spacer grid data specified
    """
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
        elif not int(spacer_data[6]) in [1, 2, 3]:
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
                raise TypeError(err_msg)
            if spacer_data[7].lower() != "discunif":
                raise TypeError("Not appropriate distribution selected!")

    else:
        raise TypeError("Only 2 and 3 are valid choices!")