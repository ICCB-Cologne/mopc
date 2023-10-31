# MOP-C - Molecular Prognostic Index for Central Nervous System Lymphomas

This repository contains the Shiny Python app MOP-C for predicting patient outcome and risk in lymphomas of the central nervous system, based on plasma and cerebrospinal fluid circulating tumor DNA sequencing. Based on user input the tool will output a patient-specific score describing the relapse risk of the patient and the risk category.
For general use, use the following link: https://www.mop-c.com/

MOP-C predicts risk of relapse in patients with CNS lymphoma. MOP-C includes clinical and molecular features assessed at baseline, after one cycle of therapy and at the end of induction therapy (Heger et al., Blood, 2023).

## Important notes:

If "0" is provided for the ctDNA level at baseline and "no" is chosen for the detection of PRD after 1 cycle of therapy and/or at the end of induction therapy, these values are submitted to MOP-C and assessed as "undetectable ctDNA" and "PRD negative" instead of "not available". These values therefore influence the risk model and MOP-C cannot be used without the required variables. 

## Disclaimer:
MOP-C is not validated in prospective clinical trials and does therefore not provide evidence to adjust, omit or intensify treatment of patients with CNS lymphoma. MOP-C should only be used by healthcare professionals and is provided without any warranty. All information contained in this system and produced by it are provided for educational purposes only. In particular, any information found here or generated from the use of this system should not be used for the diagnosis or treatment of any health problem or disease. MOP-C is not intended to replace any clinical judgement or guide individual patient care in any way.

## Credits
MOP-C was developed in collaboration with the Borchman Lab at the University Hospital Colgone.
Shiny app implementation: Teodora Bucaciuc (teodora.bucaciuc@iccb-cologne.org) and Roland Schwarz (roland.schwarz@iccb-cologne.org).

## License
This MOP-C Shiny app is distributed under the MIT license.

## References
If you use MOP-C for research, please cite:
Heger M, et al., **Entirely noninvasive outcome prediction in central nervous system lymphomas using circulating tumor DNA.** Blood 2023.


