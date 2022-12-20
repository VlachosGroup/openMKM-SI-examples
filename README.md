# openMKM-SI-examples

This repository contains OpenMKM templates/examples that are mentioned in the Journal Manuscript. The repository is divided into folders pertaining to each Figure/example mentioned in the paper. Each folder contains input and output files pertaining to that example and in some instances the folder might also have the python scipts used for plotting the respective figures. 

## This is the list of Examples 

1. Example-1-GRI-Mech
- This example compares OpenMKM with Cantera for solving time-dependent gas-phase reaction models using the famous GRI3.0 Mech: a) Oscillatory combustion of H2 and O2 at 60 Torr, and b) adiabatic combustion of lean methane/air mixture. 
2. Example-2-NH3-formation-on-Ru
- This example demonstrates OpenMKM's adsorbate-adsobate lateral interaction adjustment for surface kineitcs. NH3 production from N2 and H2 on Ru catalyst is used to demosntate this.
3. Example-3-pfr-models
- This example compares the results of OpenMKM's PFR-0D (PFR as a series of CSTRs) and PFR-1D (numerically solved 1-D PFR) with that of CHEMKIN's PFR-0D. NH3 model from Example 2 is used here. 
4. Example-4-User-Tprofile
- This example demonstrates the ability to superimpose user-defined Temperature profile along the length of a PFR-1D reactor. Ethane dehydrogenation of Pt is modeled using a) isothermal PFR, b) PFR with an increasing temperature profile, and c) PFR with a parabolic T profile. 
5. Example-5-LSA-NSC
- Example 5 depicts the use OpenMKM's local sensitivity analysis capabilities via normalized sensitivity coefficients. Ethane dehydrogenation model on Pt used in the previous model is also used here.  

## Manuscript DOI
Placeholder. 

## Contact Information
For questions please contact vkineticslab@udel.edu. 
