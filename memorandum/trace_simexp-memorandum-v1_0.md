# TRACE-SIMEXP v1.0 - Scripting Utility for Computer Experiment of TRACE

# STARS Memorandum

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

# Abstract

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

# Introduction and Scope of the Utility

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

# List of Features (v1.0)

The current version and all its features were consolidated from the
developments made for the PSI contributions to the PREMIUM Phase-IV benchmark
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

# Usage

<!--TODO General usage of the utility-->

## Step 1: Preprocessing

In the preprocessing step, the base TRACE input deck is modified by changing
the parameter values of the parameters listed in the list of parameter files
according to the values listed in the design matrix file. A set of new
perturbed TRACE input decks will be created into separate directories.
In subsequent execute step, these directories will serve as the run
directories. The preprocessing step driver script can be invoked in the
terminal using the following command:

    python prepro.py {-as, -ns, -nr} <argument to select samples to create> \
                     -b <the base run directory name> \
                     -tracin <the base TRACE input deck> \
                     -dm <the design matrix> \
                     -parlist <the list of parameters file> \
                     -info <The short description of the campaign> \
                     -ow <flag to overwrite existing directory structure>

Brief explanation on this parameter can be shown using the following command:

    python prepro.py --help

The table below lists all the arguments in detail.

|No.|Short Name|Long Name      |Type      |Required                         |Description                                    |Default     |
|---|----------|---------------|----------|---------------------------------|-----------------------------------------------|------------|
|1  |-as       |--all_sample   |flag      | Yes, iff -nr or -ns not supplied| Preprocess all samples in design matrix       |False       |
|2  |-ns       |--num_samples  |integer(s)| Yes, iff -as or -nr not supllied| Preprocess the selected samples               |None        |
|3  |-nr       |--num_range    |2 integers| Yes, iff -as or -ns not supplied| Preprocess the range of samples, inclusive    |None        |
|4  |-b        |--base_name    |string    | No                              | The base run directory name                   |./simulation|
|5  |-tracin   |--base_tracin  |string    | Yes                             | The base TRACE input deck, path+filename      |None        |
|6  |-dm       |--design_matrix|string    | Yes                             | The design matrix, path+filename              |None        |
|7  |-parlist  |--params_list  |string    | Yes                             | The list of parameters file, path+filenam     |None        |
|8  |-info     |--info         |string    | No                              | Short message of the experiment               |None        |
|9  |-ow       |--overwrite    |flag      | No                              | Flag to overwrite existing directory structure|False       |


The directories created is nested in the following form:

    .
    |
    +---<the base run directory name>
    |   +---<tracin>
    |       +---<name based on dm and parlist>
    |           +---<tracin-run_1>
    |                   tracin-run_1.inp
    |           +---<tracin-run_2>
    |                   tracin-run_2.inp
    |           +---<tracin-run_3>
    |                   tracin-run_3.inp
    |
    ...

In addition to the creation of the run directory structure and perturbed TRACE
input deck, the script execution will also produce an info file (from here on
in will be called *prepro info file*). The info file is produced by default
with the following naming convention:

    prepro-<tracin name>-<parlist name>-<dm name>-<sample_start>_<sample_end>.info

The file is used to document the command line arguments specified when the
script was called. It will also be used in the subsequent step.

**Example**

For example, upon executing the following command:

    python prepro.py -as \
                     -b ./simulation \
                     -tracin ./simulation/base/febaTrans214.inp \
                     -dm ./simulation/dmfiles/optLHS_110_2.csv \
                     -parlist ./simulation/paramfiles/febaVars2Params.inp \
                     -info "FEBA Test No. 214, 110 Samples, 2 Parameters"

A set of directory will be created

    .
    |
    +---simulation
    |   +---febaTrans214
    |       +---febaVars7Params-optLHS_110_2
    |           +---febaTrans214-run_1
    |                   febaTrans214-run_1.inp
    |           +---febaTrans214-run_2
    |                   febaTrans214-run_2.inp
    |           +---febaTrans214-run_2
    |                   febaTrans214-run_3.inp
    ...
    |           +---febaTrans214-run_110
    |                   febaTrans214-run_110.inp              

Based on the command above, the prepro info file will be created with the 
following name:

    prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info

The file has the following (abridged) contents:

    TRACE Simulation Experiment - Date: 2016-03-27 00:21:07.196979
    FEBA Test No. 214, 110 Samples, 2 Parameters
    ***Preprocessing Phase Info***
    Base Name                     -> simulation
    Base Directory Name           -> ./simulation
    Base Case Name                -> febaTrans214
    Base Case File                -> ./simulation/base/febaTrans214.inp
    List of Parameters Name       -> febaVars2Params
    List of Parameters File       -> ./simulation/paramfiles/febaVars2Params.inp
    Design Matrix Name            -> optLHS_110_2
    Design Matrix File            -> ./simulation/dmfiles/optLHS_110_2.csv
    Overwrite Directory           -> 0
    Samples to Run                ->
    1      2      3      4      5      6      7      8      9     10
     ...
    101    102    103    104    105    106    107    108    109    110
    *** 1***
    Sensitivity Coefficient with ID *1039* is specified
    Parameter type: scalar
    Parameter perturbation mode: 3 (multiplicative)
    Parameter distribution: logunif
    1st distribution parameter: 0.250
    2nd distribution parameter: 4.000
    *** 2***
    Sensitivity Coefficient with ID *1011* is specified
    Parameter type: scalar
    Parameter perturbation mode: 3 (multiplicative)
    Parameter distribution: logunif
    1st distribution parameter: 0.500
    2nd distribution parameter: 2.000

## Step 2: Execute

In the execute step, all the input decks that were created in the preprocessing
step are executed sequentially in batch. This means that the script will 
traverse the run directories created before and execute the input deck inside 
sequentially. The size of a batch is controlled by the number of processors 
supplied by the user through the command line argument. 

Simultaneous execution of multiple TRACE simulation often requires large amount
of disk space even for a single case. To save disk space, the utility takes two 
measures. First, the binary `xtv` file is not written directly in the running 
directory during the execution. Instead a soft link is created inside the 
running directory, linked to the actual `xtv` file written in a *scratch* 
directory. This approach was adopted to limit the disk space usage in a 
STARS project working directory (or *the activity folder*) that is a backup 
volume and limited to 200 [GB] currently. 
The so-called *scratch* directory usually resides in a non-backup volume.
Second, after each execution, the resulting `xtv` file will be directly 
converted to the more space efficient *dmx* format. This is done by using 
`xtv2dmx` utility. As such, the path to the scratch directory as well as the 
path to the executable for `xtv2dmx` utility are needed to be supplied during 
the call.

The execute step driver script can be invoked in the terminal using the
following command:

    python execute-py -prepro <the preprocessing step info file> \
                      -nprocs <the number of available processors> \
                      -{ns, nr, as} <selection of samples to be executed> \
                      -scratch <the scratch directory> \
                      -trace <the trace executable> \
                      -xtv2dmx <the xtv2dmx executable>

Brief explanation on the required arguments can be printed on the screen 
using the following command:

    python execute.py --help

The table below lists all the arguments used in the `execute.py` driver script.

|No.|Short Name|Long Name           |Type      |Required                         |Description                                    |Default     |
|---|----------|--------------------|----------|---------------------------------|-----------------------------------------------|------------|
|1  |-prepro   |--prepro_file       |string    | Yes                             | The path to the preprocess info file          |None        |
|2  |-nprocs   |--num_processors    |integer   | No                              | The number of processors to use for execution |1           |
|3  |-as       |--all_sample        |flag      | Yes, iff -nr or -ns not supplied| Preprocess all samples in design matrix       |False       |
|4  |-ns       |--num_samples       |integer(s)| Yes, iff -as or -nr not supplied| Preprocess the selected samples               |None        |
|5  |-nr       |--num_range         |2 integers| Yes, iff -as or -ns not supplied| Preprocess the range of samples, inclusive    |None        |
|6  |-scratch  |--scratch_directory |string    | Yes                             | The path of the scratch directory             |None        |
|7  |-trace    |--trace_executable  |string    | Yes                             | The path to the TRACE executable              |None        |
|8  |-xtv2dmx  |--xtv2dmx_executable|string    | Yes                             | The path to the XTV2DM executable             |None        |

The script execution will also produce an info file (from here on
in will be called *exec info file*). The info file is produced by default
with the following naming convention:

    exec-<tracin name>-<parlist name>-<dm name>-<sample_start>_<sample_end>.info

The file is used to document the command line arguments specified when the
script was called, to log the process run for diagnostic purpose, as well as be 
used in the subsequent (postpro) step. See below for the example of the 
contents.

**Example**

Following the previous example, executing the following command will
execute all of the TRACE input decks created in the previous step using 5 
processors (or, parallel jobs with multiple batches each of size 5).

    python execute.py -prepro prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info \
                      -as \
                      -scratch /afs/psi.ch/group/lrs/scratch/grp.lrs.scr001.nb/wicaksono_d/ \
                      -trace trace_v5.0p3.uq_extended \
                      -xtv2dmx xtv2dmx_v6.5.2_inst01.sh \
                      -nprocs 5 >& 214_1060_7.log &

**Remarks**: The utility was so far tested in the `lclrs` machines. To keep the 
kerberos token active for a long session, it is advised to use the `k5run -B` 
command and put the job in the background with the following command instead:

    k5run -B python execute.py -prepro prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info \
                               -as \
                               -scratch /afs/psi.ch/group/lrs/scratch/grp.lrs.scr001.nb/wicaksono_d/ \
                               -trace trace_v5.0p3.uq_extended \
                               -xtv2dmx xtv2dmx_v6.5.2_inst01.sh \
                               -nprocs 5 >& 214_1060_7.log &

Based on the command above, the prepro info file will be created with the 
following name:

    exec-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info

The file has the following (abridged) contents:

    TRACE Simulation Experiment - Date: 2016-03-27 00:26:06.547934
    ***Execute Phase Info***
    prepro.info Filename          -> prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info
    TRACE Executable              -> trace_v5.0p3.uq_extended      
    XTV2DMX Executable            -> xtv2dmx_v6.5.2_inst01.sh      
    Scratch Directory Name        -> /afs/psi.ch/group/lrs/scratch/grp.lrs.scr001.nb/wicaksono_d
    Number of Processors          -> 5  (lclrs73)
    Samples to Run                -> 
      1      2      3      4      5      6      7      8      9     10
     11     12     13     14     15     16     17     18     19     20
    ...
    101    102    103    104    105    106    107    108    109    110
    *** Batch Execution -     1 ***
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_1
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_3
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_5
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_2
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_4
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_1.xtv -d febaTrans214-run_1.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_3.xtv -d febaTrans214-run_3.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_5.xtv -d febaTrans214-run_5.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_2.xtv -d febaTrans214-run_2.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_4.xtv -d febaTrans214-run_4.dmx
    ...
    *** Batch Execution -    22 ***
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_106
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_108
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_110
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_107
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_109
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_106.xtv -d febaTrans214-run_106.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_108.xtv -d febaTrans214-run_108.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_110.xtv -d febaTrans214-run_110.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_107.xtv -d febaTrans214-run_107.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_109.xtv -d febaTrans214-run_109.dmx

## Step 3: Postprocessing

After all the requested TRACE input decks (or samples) have been executed, the 
resulting `xtv` files can be post-processed to extract the relevant variables 
and put them into separate `csv` files, placed inside the respective running 
directory. The `csv` files, being text files, can be easily processed further 
with other tool for various purposes. Similar to the execute step before, the 
utility will traversed each of the executed running directory and process the 
`xtv` file inside using the `aptplot` program to extract the requested 
variables. The script also supports batch parallel execution.

The postprocessing step driver script can be invoked in the terminal using 
the following command:

    python postpro.py -exec <the execute phase info file> \
                      -aptplot <the aptplot executable> \
                      -nprocs <the number of available processors> \
                      -vars <the list of TRACE graphic variables file>

Brief explanation on the required arguments can be printed on the screen using 
the following command:

    python postpro-py --help

The table below lists all the required arguments in detail.

|No.|Short Name|Long Name           |Type      |Required|Description                                       |Default|
|---|----------|--------------------|----------|--------|--------------------------------------------------|-------|
|1  |-exec     |--exec_info         |string    |Yes     |the path to the execute info file                 |None   |
|2  |-aptplot  |--aptplot_executable|string    |Yes     |the path to `aptplot` executable                  |None   |
|3  |-nprocs   |--num_processors    |integer   |No      |The number of processors to use for postprocessing|1      |
|4  |-vars     |--trace_variables   |string    |Yes     |Preprocess the selected samples                   |None   |

**Remarks 1**: When running the script interactively under Windows which is 
connected to an `lclrs` machine, the `aptplot` program requires an X Server 
running in the background (e.g., `Xming`).

**Remarks 2**: Make sure there is enough disk space in the running directory 
as the csv files being produced. Depending on how many variables are being 
extracted, the files (being a text file) can take considerable amount of disk
space.

In addition to the postprocessing of the `xtv` files, the execution of postpro
script will also produced an info file (hereinafter *postpro info file*). 
The info file is produced by default with the following naming convention:

    postpro-<tracin name>-<parlist name>-<dm name>-<sample_start>-_<sample_end>-<vars name>.info

The file is used to document the command line arguments specified when the
script was called as well as to log all the shell commands run during the 
execution. See below for example of the contents.


**Example**

Following the previous example, executing the following command will
postprocessed all of the TRACE `xtv` files produced in the previous step using 
5 processors (or, parallel jobs with multiple batches each of size 5) to 
extract TRACE graphic variables listed in the `./simulation/listVars.apt` file.

    python postpro.py -exec exec-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info \
                      -aptplot aptplot_v6.5.2_inst01.sh \
                      -nprocs 5 \
                      -vars ./simulation/listVars.apt

**Remarks**: Similar to the execute phase, if the postprocess step is expected
to take a long time it is advised that the job is sent to the background with 
`k5run -B` utility as given in the previous example.

Based on the command above, the prepro info file will be created with the 
following name:

    postpro-febaTrans214-febaVars2Params-optLHS_110_2-1_110-listVars.info

The file has the following (abridged) contents:

    TRACE Simulation Experiment - Date: 2016-03-24 17:34:10.713350
    ***Post-process Phase Info***
    prepro.info Filename          -> prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info
    exec.info Filename            -> exec-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info
    APTPlot Executable            -> aptplot_v6.5.2_inst01.sh      
    Number of Processors (Host)   -> 5  (lclrs73)
    List of XTV Variables Files   -> ./simulation/listVars.apt
    List of XTV Variables         -> 
        rdzNperm-20A01        rdzNperm-20A02        rdzNperm-20A03
        rdzNperm-20A04        rdzNperm-20A05        rdzNperm-20A06
        rdzNperm-20A07        rdzNperm-20A08        rdzNperm-20A09
        ...
        rftn-20A141R29        rftn-20A142R29 
    Samples to Post-processed     -> 
      1      2      3      4      5      6      7      8      9     10
     11     12     13     14     15     16     17     18     19     20
     21     22     23     24     25     26     27     28     29     30
     31     32     33     34     35     36     37     38     39     40
     41     42     43     44     45     46     47     48     49     50
     51     52     53     54     55     56     57     58     59     60
     61     62     63     64     65     66     67     68     69     70
     71     72     73     74     75     76     77     78     79     80
     81     82     83     84     85     86     87     88     89     90
     91     92     93     94     95     96     97     98     99    100
    101    102    103    104    105 
    *** Batch Execution -     1 ***
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans214-run_1-listVars.apt -nowin
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans214-run_3-listVars.apt -nowin
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans214-run_5-listVars.apt -nowin
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans214-run_2-listVars.apt -nowin
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans214-run_4-listVars.apt -nowin
    ...

## The list of parameters file

<!--TODO Carefully describe the syntax of `paramlist` file-->

## The design matrix file

The design matrix (or *the design of experiment*) file is a text file that 
contains the sampled and normalized (values between 0 - 1) input parameters 
values. The matrix is of dimension *N x K*, where *N* corresponds to the number 
of rows (i.e., the number of samples) and *K* corresponds to the number of 
columns (i.e., the number of parameters/dimensions). The values of each rows 
can be separated by comma, tab, space, or semicolon.

The values inside the file can be generated by various different procedures 
such as the simple random sampling (SRS), Latin Hypercube Sampling (LHS), or 
quasi-random sequence (Sobol' Sequence, Halton Sequence, Hammersley set, etc) 
each with its own statistical property. The procedure to generate the values is 
outside the scope of `trace-simexp` utility. Example of tools to generate such 
values is Simlab [1], DiceDesign (an R package [2]), or OpenTurns 
(a Python module [3]).

**Example**

The excerpt below is taken from the first 7 lines of a design matrix file with
5 parameters separated by comma.

    3.154313e-02,5.621832e-01,1.046621e-01,6.978293e-02,1.599945e-01
    1.475773e-01,1.229935e-01,7.299532e-01,8.951946e-01,4.153665e-01
    2.229898e-01,9.981891e-01,3.783502e-02,1.558353e-01,5.350678e-01
    9.846914e-01,7.849868e-02,4.686996e-01,2.895825e-01,6.436200e-01
    9.250452e-01,6.194709e-01,6.873275e-01,5.125879e-01,8.598690e-01
    1.974221e-01,4.532642e-01,4.914747e-01,6.819097e-01,8.206347e-02
    2.832927e-01,8.773572e-01,3.679600e-01,5.648471e-01,2.747036e-01

## The list of graphic variable file

<!--TODO Carefully describe the syntax of list of graphic variable-->

## TRACE and aptplot

# Implementation

<!--TODO Some notes on implementation-->

## Assumptions

<!--TODO Carefully mention/list the assumptions used-->

## Known Limitations

<!-- TODO list the current known limitations -->

## Distribution

<!--TODO How the utility being distributed within STARS-->

# Examples of Use Cases

<!--TODO Some example of use cases-->

# References

[1]:https://ec.europa.eu/jrc/en/samo/simlab
[2]:https://cran.r-project.org/web/packages/DiceDesign/index.html
[3]:http://www.openturns.org/