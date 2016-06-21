# TRACE-SIMEXP v1.0 - Scripting Utility for TRACE Simulation Experiment

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

A computer experiment is a multiple model runs using different values of 
the model parameters. Its design, in particular the selection of the 
design points, as well as its analysis, in particular the analysis of 
the output variation in relation to the inputs variation, are useful for 
sensitivity and uncertainty analyses of the model subjected to the 
experimentation.

a Python3-based scripting utility has been developed to assist in the 
logistical aspects of carrying such experiments for TRACE code. 
The scope of the utility is ranging from the pre-processing the TRACE 
input deck amenable for batch parallel execution to the post-treatment 
of the resulting binary xtv file amenable to sensitivity and uncertainty 
analyses. This memorandum describes the development of the tool, 
including the descriptions on its implementation, its assumptions, 
as well as its usage.

## Introduction and Scope of the Utility
 
In the context of PSI contribution to the OECD/NEA PREMIUM Benchmark Phase IV, 
there was a need to be able to execute numerous TRACE runs of a given model with 
different values of the input parameters in a systematic manner. 
By taking the developments from the design and analysis of computer experiment, 
the resulting outputs can then be analyzed further, either for the purpose of 
quantifying the model prediction uncertainty (*uncertainty propagation*) or 
of understanding better the input/output relationship of the complex model 
(*sensitivity analysis*). This document details the implementation of a 
Python3-based utility to assist in carrying out computer experiment for 
TRACE model.

The global flowchart of the utility is shown in Figure 1.
The process is done in three sequential steps with clearly defined inputs 
and outputs as well as a set of required command line arguments.
The flowchart also explicitly states the scope of the utility development that 
begins with a set of input files and ends with a set of csv files. 
The most important input file for a computer experiment campaign is the 
design matrix which contains normalized input parameters values at which 
TRACE will be run. The design matrix is produced by generic numerical routine 
and is outside the scope of `trace-simexp`.
The set of csv files, each of which contains TRACE graphic variables extracted 
from the produced binary xtv files.
The csv files are ready to be further post-processed for sensitivity/uncertainty 
analysis. The tools required to carry out such an analysis is also outside 
the scope of `trace-simexp`.

![Figure 1: Generic flowchart of trace-simexp including the required input files](figures/flowchart.png)

The current version and its features were a consolidation from the developments
made for the PSI contributions to the PREMIUM Phase-IV benchmark 
(application of uncertainty propagation), the NUTHOS-11 conference 
(application of the Morris method), and the NURETH-16 conference (application 
of the Sobol' method). All the aforementioned applications were related to TRACE
reflood model on the basis of FEBA separate effect facility for reflood 
experiment.
In the subsequent sections, the implementation will be explained in more detail.

## Description of Features (v1.0)

<!--TODO Give short listing of features that have been implemented so far --> 

## Implementation

<!--TODO Some notes on implementation--> 

### Assumptions

<!--TODO Carefully mention/list the assumptions used--> 

### Usage

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

### Distribution 

<!--TODO How the utility being distributed within STARS--> 

## Examples of Use Cases

<!--TODO Some example of use cases-->
