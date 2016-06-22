# TRACE-SIMEXP v1.0 - Scripting Utility for Computer Experiment of TRACE

## STARS Memorandum

Date: 23.06.2016

From: D. Wicaksono

Phone: +41 56 310 2759

Loc.: OHSA/D08

Email: damar.wicaksono@psi.ch

To:

 1. STARS / O. Zerkak
 2. STARS / Y. Aounallah
 3. ERP / G. Perret

cc:

 1. STARS / STARS_TRACE
 2. STARS / M. Krack
 3. STARS / H. Ferroukhi

## Abstract

A computer experiment is a multiple model runs using different values of the
model parameters. Its design, in particular the selection of the design points
at which the model will be evaluated, well as its analysis, in particular the
analysis of the output variation in relation to the inputs variation, are
useful for sensitivity and uncertainty analyses of the model subjected to the
experimentation.

An important prerequisite of carrying out such experiment is the availability
of a supporting tool able to handle the related logistical aspects. a
Python3-based scripting utility has been developed to assist in carrying such
experiments for TRACE code. The scope of the utility is ranging from the
pre-processing the TRACE input deck amenable for batch parallel execution to
the post-treatment of the resulting binary xtv file amenable to subsequent
sensitivity and uncertainty analyses. This memorandum describes the development
of the tool, including the description on its usage, implementations, and
assumptions.

## Introduction and Scope of the Utility

In the context of PSI contribution to the OECD/NEA PREMIUM Benchmark Phase IV,
there was a need to be able to execute numerous TRACE runs of a given model
with different values of the input parameters in a systematic manner. By taking
the developments from the design and analysis of computer experiment, a
reasonable number of inputs combinations (directly translated to the number of
code runs) can be judiciously selected and the resulting outputs can then be
analyzed further. These were done either for the purpose of quantifying the
model prediction uncertainty (*uncertainty propagation*) or of understanding
better the input/output relationship of the complex model
(*sensitivity analysis*). This document details the implementation of a
Python3-based utility to assist in carrying out computer experiment for TRACE
model.

The top-level flowchart of the utility is shown in Figure 1. The process is done
in three sequential steps with clearly defined inputs and outputs as well as a
set of required command line arguments. The flowchart also explicitly states
the scope of the utility development that begins with a set of input files and
ends with a set of csv files. The most important input file for a computer
experiment campaign is the design matrix which contains normalized input
parameters values at which TRACE will be run. The design matrix is produced by
generic numerical routine and is outside the scope of `trace-simexp`.
The set of csv files, each of which contains TRACE graphic variables extracted
from the produced binary xtv files is the ultimate output of the utility.
The csv files are ready to be further post-processed for
sensitivity/uncertainty analysis. The tools required to carry out such an
analysis is also outside the scope of `trace-simexp`.

![Figure 1: Generic flowchart of trace-simexp including the required input files](figures/flowchart.png)


In the subsequent sections, the usage information as well as the notes on the
implementation will be explained in more detail.

## List of Features (v1.0)

The current version and its features were a consolidation from the developments
made for the PSI contributions to the PREMIUM Phase-IV benchmark
(the application of uncertainty propagation), the NUTHOS-11 conference
(the application of the Morris method), and the NURETH-16 conference
(the application of the Sobol' method). All the aforementioned applications
were related to TRACE reflood model on the basis of FEBA separate effect
facility for reflood experiment.

The features of this release are:

1. Complete separation of the process in 3 different steps: prepro,
   exec, and postpro. At each step an auxiliary file (so called info file) is
   produced and used at the subsequent step (except the postpro info file) as
   well as for documentation and diagnostic purposes.
2. Three modes of parameter perturbation are supported: additive,
   multiplicative, and substitutive.
3. Four categories of TRACE variables in the input deck that can be
   perturbed: spacer grid, material properties,
   *sensitivity coefficients*, and components.
4. Specifically for the TRACE components, five different components are
   supported: PIPE, VESSEL, POWER, FILL, BREAK.
5. Specification of the computer experiment by the users is done through a set
   of input files (list of parameters file, design matrix file, and list of
   graphic variables file) and a set of command line arguments given at each
   step.
6. Iso-probabilistic transformation of the normalized design matrix is
   available for uniform, discrete uniform, log-uniform, and normal
   distributions.

## Usage

<!--TODO General usage of the utility-->

### Step 1: Preprocessing

<!--TODO What does the prepro phase do?-->

### Step 2: Execute

<!--TODO What does the exec phase do?-->

### Step 3: Postprocessing

<!--TODO What does the postpro phase do?-->

### The list of parameters file

<!--TODO Carefully describe the syntax of `paramlist` file-->

### The design of experiment file

<!--TODO Carefully describe the syntax of design of experiment file-->

### The list of graphic variable file

<!--TODO Carefully describe the syntax of list of graphic variable-->

### TRACE and aptplot


## Implementation

<!--TODO Some notes on implementation-->

### Assumptions

<!--TODO Carefully mention/list the assumptions used-->

### Known Limitations

<!-- TODO list the current known limitations -->

### Distribution

<!--TODO How the utility being distributed within STARS-->



## Examples of Use Cases

<!--TODO Some example of use cases-->
