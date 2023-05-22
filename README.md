# Crustal-Explorer-DTEnsemble
Ensemble-based Decision Tree algorithms for investigating crustal thickness and velocities. This project applies machine learning techniques to geophysical data, enhancing our understanding of Earth's subsurface structure

## SynRF-generator

Welcome to the 'SynRF-generator' repository. This project contains a suite of codes written in C for generating synthetic receiver functions based on various synthetic structures. These structures include antiform, synform, offset, slope, and fault structures, with possibilities to design even more complex models as per your requirements.

### Code Structure

Here is a brief overview of what each program does:  
* antiform.c - Generates the antiform structure.  
* synform.c - Generates the synform structure.  
* offset.c - Generates the offset structure.  
* slope.c - Generates the slope structure.  
* fault.c - Generates the fault structure.  
* syn_moho - The main program, capable of designing complex structures.  

### Usage

To use 'syn_moho', run the command in the following format:  
./syn_moho -P$type -V$vel -Ooutput.txt -Ddepth

### Parameters

* -P : Specify the structure you want (options include: antiform, synform, offset, slope, and fault).
* -V : Input velocity model that will be used to generate the synthetic receiver functions.
* -O : Output velocity models. The format is: moho depth, vp, vp/vs \ moho depth + 1, vp, vp/vs.
* -D : The output Moho depth.
