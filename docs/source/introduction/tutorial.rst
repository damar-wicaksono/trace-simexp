.. _trace_simexp_tutorial:

====================================================================
Tutorial: Simple Uncertainty Propagation of a Reflood Facility Model
====================================================================

In this tutorial, we are going to propagate the uncertainty of parameters related to spacer grid model in TRACE
in the simulation of a reflood experimental facility model.

Spacer grid specification in TRACE requires 7 prameters to be specified.
In the specification of FEBA reflood facility given as part of the OECD/NEA
PREMIUM benchmark, only two of those parameters were given explicitly, 
two were derived from simple schematic of the test test section, 
and the rest of the parameters are considered unknown.
Furthermore, the specification also stated that "the applied spacers were original PWR spacers as used by KWU"
which is not specific enough to obtain the actual technical data.
The table below summarized the required inputs to fully specify TRACE spacer grid model.

=== ========= ======================================================== ============= ================ ================= =========
No. Parameter Description                                              Unit          Allowable Values Nominal Value     Remark
=== ========= ======================================================== ============= ================ ================= =========
1   spbloc    spacer grid blockage ratio                               :math:`[-]`   :math:`[0.,1.]`  :math:`0.2`       Specified
2   vnbloc    mixing vane blockage ratio                               :math:`[-]`   :math:`[0.,1.]`  :math:`0.`        Assumed
3   phi       mixing vane angle from parallel with the top of the grid :math:`[^o]`  :math:`[0.,45.]` :math:`0.`        Assumed
4   wetperm   spacer grid wetted perimeter                             :math:`[m]`   :math:`\geq 0.`  :math:`1.803`     Derived
5   height    spacer grid axial height                                 :math:`[m]`   :math:`\geq 0.`  :math:`3.8E-2`    Specified
6   strhick   grid strap thickness                                     :math:`[m]`   :math:`\geq 0.`  :math:`1.3275E-3` Derived
7   spmatid   spacer grid material number                              :math:`[-]`   :math:`[-]`      Inconel 718       Assumed
=== ========= ======================================================== ============= ================ ================= =========

Note that for the spacer grid material number, TRACE supports 7 built-in material given in the table below

======= ===================
spmatid Description
======= ===================
2       zircaloy
6       stainless steel 304
7       stainless steel 316
8       stainless steel 347
9       carbon steel A508
10      Inconel 718
11      ZrO2
12      Inconel 600
======= ===================

As such, the unknown parameters have to be assumed and are considered *uncertain*
To have a robust analysis it is wise to check how the model behave under the change of these assumptions.
Statistical method is adopted for the problem of uncertainty quantification where the unknown parameters are modeled as random variables allowed to vary within certain range.
Furthermore, the other 4 parameters, though specified, are also allowed to vary around their respective nominal values.
These parameters are to be sampled and for each combination of inputs the output will be evaluated.
The dispersion of the output will give some ideas on how the output of the model behave under the assumed parameter uncertainties.

In ``trace-simexp``, an uncertain model parameter change its value due to perturbation by a factor.
This perturbation factor is the one which is modeled explicitly as random variable, following certain known distribution, which in turn can be sampled from.
The perturbation factor affects the actual value of model parameter through three modes of operation:

1. substitutive: the sampled perturbation factor directly substitutes the value of a model parameter
2. additive: the sampled perturbation factor is added to the nominal value of the model parameter
3. multiplicative: the sampled perturbation factor is multiplied to the nominal value of the model parameter

The table below summarizes the specification of the perturbation factor associated with each of the model parameters

=== ========= ==================== ================ ====================== =====================
No. Parameter Mode of Perturbation Distribution     Dist. Parameters       Remarks
=== ========= ==================== ================ ====================== =====================
1   spbloc    multiplicative       uniform          min = 0.75, max = 1.25 :math:`\pm 25\%`
2   vnbloc    substitutive         uniform          min = 0.0, max = 0.5   
3   phi       substitutive         discrete uniform {0.,15.,30.,45.}       to reduce input space
4   wetperm   multiplicative       uniform          min = 0.75, max = 1.25 :math:`\pm 25\%`
5   height    multiplicative       uniform          min = 0.75, max = 1.25 :math:`\pm 25\%`
6   strhick   multiplicative       uniform          min = 0.75, max = 1.25 :math:`\pm 25\%`
7   spmatid   substitutive         discrete uniform {2,6,7,8,9,10,11,12}   no preferred choice
=== ========= ==================== ================ ====================== =====================

The nature of the present analysis is rather exploratory, 
with a main purpose to see how the predicted cladding temperature is dispersed due to the uncertainties of the model parameters.
This is the main reason to use uniform distribution within a certain range to model the perturbation factor.
Furthermore, the uncertainties given in the above table are assumed to be independent.
This, strictly speaking, is not a correct assumption as the strap thickness and the grid flow blockage ratio are correlated.
The same goes for the mixing vane angle and the vane blockage ratio.
However, for simplicity, in line with the purposed of the analysis, the independent assumption is kept.

Preparing the List of Parameters File
=====================================

Preparing the Design Matrix File
================================

Conducting Simulation Experiment 
================================

Results
=======

Variation in Clad Temperature Evolution
---------------------------------------

.. image:: ../../figures/feba_grid.png

Scatterplot Sensitivity Analysis
--------------------------------

