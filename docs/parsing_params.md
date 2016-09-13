# `trace_simexp` - Parsing Input Specifications for Simulation Experiment 

## General formats

The *list of parameters file* contains the specification of perturbed parameters
of a TRACE model specified by the user.
In general, for each line, it contains the following information:

 1. `enum`: the enumeration of the specified parameter in the list. The list
   will be read as a list of python dictionary
 2. `data_type`: is the type of parameters available to the user
 3. `var_num`: the number of the parameters (typically a unique TRACE ID)
 4. `var_name`: the name of the parameter
 5. `var_type`: the type of the parameter, depends on the data type. e.g.,
   `scalar`, `array`, `table`
 6. `var_mode`: the mode of perturbation (i.e., substitutive, additive,
   multiplicative)
 7. `var_card`: the card of which the specific parameter to be perturbed is
   located
 8. `var_word`: the word in a card of which the specific parameter to be
   perturbed is located
 9. `var_dist`: the distribution of the perturb parameter
10. `var_par1`: the 1st parameter of the distribution
11. `var_par2`: then 2nd parameter of the distribution
12. `str_fmt`: string formatting (e.g., `14.4f`, `14d`, `14.4e`)

Several parameters in a TRACE model can be substituted with a random values
for simulation experiment purpose.
The parameters are classified into several categories or *data types*.
The currently supported *data types* are:

 1. Spacer grid with keyword `spacer`
 2. Material properties with keyword `matprop`
 3. (So-called) *sensitivity coefficients* with keyword `senscoefs`
 4. TRACE components of `pipe`, `vessel`, `power`, `fill`, `break`

The parameters that can be accessed for each of these different data types are
of course differ. This difference will be explained in the following section:

## !!! Difference with the Old Format !!!

Several simulation experiments (NUTHOS-10, NURETH-16, etc.) were done previously 
using the old list of parameters file format. 
The format has the following specification:

Major changes compared to the previous format is:

 1. The number of columns are now 12, 3 more compared to the previous version.
   All have to be specified. If a column is undefined for certain `data_type`
   arbitrary string (recommended `-`) is required.
 2. `enum`, the enumeration of perturbed parameter specification has to be 
   specified and sequential. This can force the analyst to check the list of
   parameters file
 3. `var_mode` is new and has to be specified for all `data_type`
   this an important change as now the mode of perturbation is directly specified
   as opposed to inferring from the `data_type` 
 4. `str_fmt` is new and has to be speficied for all `data_type`
   this addition will accomodate different string printing format for various
   parameters (some are integer, some are float in exponential format, etc)
 5. `var_type` is now mandatory for all `data_type` including `senscoef` where 
 	the only acceptable `var_type` is *scalar*
 6. for `matprop` data type with `table` type, the `var_card` now starts with 
   1 for **rho** up to 4 for **emis**, temperature card is excluded from 
   perturbation

## 1. Spacer Grid Parameter

An example of spacer grid data specification int the TRACE input deck is shown
below,

    ********************
    * Spacer Grid Data *
    ********************
    *
    * Card Number 1 (1 word)
    *   gridid
        101
    * Card Number 2 (4 words)
    * spbloc    vnbloc  phi     wetperm
        0.362   0.188   30.0    1.912
    * Card Number 3 (3 words)
    *   height      strthick     spmatid
        0.045       0.001           2

The definition of the parameters are the following

| variable | unit | description |
---------------------------------


All the parameters characterizing the spacer grid are accessible from
the list of parameters file. However, each of these parameters is perturbed
**independently**.

### Parsing `tracin`

Parsing `tracin` for spacer grid parameters is relatively simple.
All the parameters except `spmatid` (`int`) are of type `float`.
The numbers of parameters and their locations are also not variable on some condition:
There is always 4 parameters (words) in the second card and 3 parameters in the third card.

The parsing algorithm for spacer grid parameter works the following:

 1. Loop over input file
  - if **gridid** string is found in a line stay in this line
  - go one line below and check the number (`gridid`).
  - if it is the same as the one specified in the dictionary, proceed
  - get the nominal value based on the specified card and specified word
  - if it's the second card offset the line by 3 and if it's the third card offset by 5
  - take the parameter value from the splitted line according to the specified word.
    Always offset by 1 as python is zero-indexed

## 2. Material Properties

For material properties to be accessible for parameter perturbation, the
material has to be specified a **user-defined**. The currently supported
properties are:

 - `rho`: the density
 - `cond`: the thermal conductivity
 - `cp`: the thermal capacity
 - `emis`: the emissivity

  1. `enum`: the enumeration of perturbed model parameters in the list file
  2. `data_type`: the type of perturbed model parameters (key == `spacer`)
  3. `num`: the `gridid` identifying a unique spacer grid in the model)
  4. `var_name`: the spacer grid parameter name (for completeness)
  5. `var_type`: the `mode` of perturbation (`1 | 2 | 3`)
  6. `var_card`: the card number of spacer grid specifications (`2 | 3`)
  7. `var_word`: the word number of spacer grid specifications
     (`1|2|3|4` if `var_card == 2` and
      `1|2|3` if `var_card == 3`)
  8. `var_dist`: distribution of the random variable
  9. `var_par1`: the minimum or 1st parameter of the distribution
 10. `var_par2`: the maximum or 2nd parameter of the distribution

### Parsing `tracin`

All material properties in a `tracin` has to be put under
**User Defined Materials**.

Parsing `tracin` for material properties can be complicated as two different
types of material property parameters are available: `table` and `fit`

`table` corresponds to the temperature-dependent data, while `fit` corresponds
to functional-fit data.

An example of `table` specification is shown below,

    *  User Defined Material : 50
    *
    *n: MgO
    *
    *d: Magnesium Oxide material properties for FEBA SET Facility
    *d: as specified by GRS for PREMIUM benchmark
    *  prptb         temp         rho          cp        cond        emis
    *  prptb*      273.15      2500.0       946.0         5.0         1.0s
    *  prptb*      293.15      2500.0       963.0        4.95         1.0s
    *  prptb*      373.15      2500.0      1013.0        4.75         1.0s
    *  prptb*      473.15      2500.0      1075.5         4.5         1.0s
    *  prptb*      573.15      2500.0      1163.0        4.25         1.0s
    *  prptb*      673.15      2500.0      1174.0         4.1         1.0s
    *  prptb*      773.15      2500.0      1185.0        3.95         1.0s
    *  prptb*      873.15      2500.0      1206.0         3.6         1.0s
    *  prptb*     1073.15      2500.0      1248.0         3.1         1.0s
    *  prptb*     1273.15      2500.0      1290.0         2.8         1.0s
    *  prptb*     1473.15      2500.0      1311.6         2.4         1.0s
    *  prptb*     1773.15      2500.0      1344.0         1.8         1.0e
    *

So the keyword that defines the location of a specified material is
**User Defined Material** and check the number besides it whether it matches the
one in the list.

the material property specification in the list of parameters file has the
following entries:

    5   matprop    51     cond  table   3        4       17     unif 0.95  1.05

 1. `enum`: the parameter number
 2. `data_type`
 3. `var_num`: the number of user-defined material
 4. `var_name`: the parameter name (`rho | cp | cond | emis`)
 5. `var_type`: the type of parameter (`table | fit`)
 6. `var_card`: the column of the parameter
 7. `var_word`: the number of entries in the temperature dependent table (if `table`)

## 3. Sensitivity Coefficient

The term *sensitivity coefficient* introduced in the special delivery of
`trace v5.0p3` is a misnomer. The term is used as a perturbation factor
for a model parameter inside TRACE. In other words, it is an externalization
attempt of a model parameter, made accessible through the standard input deck.

An example of how a sensitivity coefficient is defined in the trace input deck
is given below where for each sensitivity coefficients, three parameters need to
be specified: `id`, `mode`, and `value`.

    ***************
    * Model flags *
    ***************
    *
    .....
    *
    ****************************
    * Sensitivity Coefficients *
    ****************************
    *
    * Spacer Grid Pressure Loss Coefficient Multiplier
    *id    mode   value
    1033    3     1.0
    *
    *************************
    * component-number data *
    *************************
    *
    ......

`id` is a unique integer number identifying a sensitivity coefficient.
`mode` is the mode of perturbation of a sensitivity coefficient. There are three
modes of perturbation:

 1. substitutive (mode == 1)
 2. additive (mode == 2)
 3. multiplicative (mode == 3)

Finally, `value` is the value of actual perturbation factor.

### Specifying list of params file

An example of how a sensitivity coefficient can be modelled as random and given
a distribution in the list of parameters file used for simulation experiment is
shown below,

    enum data_type   num var_name var_type var_card var_word    dist   min   max
      16  senscoef  1035        -        3        -        - logunif   0.5   2.0

The following inputs must be given in the list of parameters file for each
specified sensitivity coefficients:

 1. `enum`: the enumeration of perturbed model parameters in the list file
 2. `data_type`: the type of perturbed model parameters (key == `senscoef`)
 3. `num`: the `id` identifying a sensitivity coefficient (`[1030-1050]`)
 4. `var_name`: **not used** (`-`)
 5. `var_type`: the `mode` of perturbation (`1 | 2 | 3`)
 6. `var_card`: **not used** (`-`)
 7. `var_word`: **not used** (`-`)
 8. `var_dist`: distribution of the random variable
 9. `var_par1`: the minimum or 1st parameter of the distribution
 10. `var_par2`: the maximum or 2nd parameter of the distribution

### Parsing tracin

Parsing a sensitivity coefficient in tracin is the easiest one to do.
a unique coefficient ID (starting above 1000) is put in the beginning of line.
When parsing, the **ID** can be directly used as the location identifier of sensitivity coefficient definition.

Furthermore, because all sensitivity coefficients are defined in one line using three words (elements),
there is no need for offsetting and conditioning between different coefficient.

**Possible Complication:** junction of hydraulic component is also specified in the beginning of line,
if the model has junction with large numbers, conflict might arise.
Possible solution is to make sensitivity coefficient block more specific.

## 4. Components parameter

Parameters which are associated with a TRACE component are classified into
three different categories:

 1. `scalar`: simple single value
 2. `table`: sets of values of different type, usually multiple lines without
    continuation
 3. `array`: a set of values of the same type, usually written in multiple
    lines with continuation


 ## Specifying Distributionlele
