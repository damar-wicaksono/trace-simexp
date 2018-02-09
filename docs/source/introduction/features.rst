.. _trace_simexp_features:

========================
List of Current Features
========================

 - Complete separation of the processes in 3 different steps: **prepro**, 
   **exec**, and **postpro**.
 - Three modes of parameter perturbation are supported: additive, 
   multiplicative, and substitutive
 - Four categories of TRACE variables in the input deck can be perturbed:
   spacer grid, material properties, *sensitivity coefficient*, and components
 - For TRACE components, five are supported: PIPE, VESSEL, POWER, FILL, BREAK
 - Specification of the computer experiment by the users is done throug a set 
   of input files (list of parameters file, design matrix file, and list of 
   graphic variables)
 - Iso-probabilistic transformation of the normalized design matrix is 
   available for uniform, discrete, and log-uniform
