# Parsing Input Parameters for Simulation Experiment (trace_simexp package)

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

## General formats

## 1. Spacer Grid Parameter

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


## 2. Material Properties

For material properties to be accessible for parameter perturbation, the
material has to be specified a **user-defined**. The currently supported
properties are:

 - `rho`: the density
 - `cond`: the thermal conductivity
 - `cp`: the thermal capacity
 - `emis`: the emissivity

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

 1. additive (mode == 1)
 2. substitutive (mode == 2)
 3. multiplicative (mode == 3)

Finally, `value` is the value of actual perturbation factor.

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
 8. `dist`: distribution of the random variable
 9. `min`: the minimum or 1st parameter of the distribution
 10. `max`: the maximum or 2nd parameter of the distribution

## 4. Components parameter
