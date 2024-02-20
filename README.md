

READ ME File For 'Dataset supporting the publication "A systematic investigation into the effect of roughness on self-propelled swimming plates"'



Dataset DOI: https://doi.org/10.5258/SOTON/D2963



Date that the file was created: 01/2022



-------------------

GENERAL INFORMATION

-------------------



ReadMe Author: Jonathan	Massey, University of Southampton [0000-0002-2893-955X]



Related projects: Massey, J., Ganapathisubramani, B., & Weymouth, G. (2023). A systematic investigation into the effect of roughness on self-propelled swimming plates. *Journal of Fluid Mechanics*, 971, A39. [doi:10.1017/jfm.2023.703](https://doi.org/10.1017/jfm.2023.703)




--------------------------

SHARING/ACCESS INFORMATION

-------------------------- 



Licenses/restrictions placed on the data, or limitations of reuse: The data is accessible via CC BY license.



Recommended citation for the data: Massey, J., Ganapathisubramani, B., & Weymouth, G. (2023). A systematic investigation into the effect of roughness on self-propelled swimming plates. *Journal of Fluid Mechanics*, 971, A39. [doi:10.1017/jfm.2023.703](https://doi.org/10.1017/jfm.2023.703)


This dataset supports the publicly accessible publication:

Massey, J., Ganapathisubramani, B., & Weymouth, G. (2023). A systematic investigation into the effect of roughness on self-propelled swimming plates. *Journal of Fluid Mechanics*, 971, A39. [doi:10.1017/jfm.2023.703](https://doi.org/10.1017/jfm.2023.703)


--------------------

DATA & FILE OVERVIEW

--------------------



This dataset contains:


```plaintext
├── analysis
│   ├── domain.py
│   ├── envelopes
│   ├── extract-delta.py
│   ├── figures
│   ├── forces.py
│   ├── inout.py
│   ├── lit_data
│   ├── outer-scaled-enstrophy.py
│   ├── __pycache__
│   ├── resolution.py
│   ├── validation.py
│   └── zeta_lambda.npy
├── domain-test
│   ├── 12000
│   ├── 24000
│   ├── 6000
│   └── analysis
├── outer-scaling
│   ├── 12000
│   ├── 24000
│   ├── 6000
│   └── analysis
├── paraSub
├── README.md
├── res-study
│   ├── 12000
│   ├── 24000
│   ├── 48000
│   ├── 6000
│   └── analysis
├── tidy_res_test
│   ├── 16x16
│   ├── 52x52
│   ├── analysisSub
│   ├── convergence_plots.py
│   ├── fft.py
│   ├── figures
│   ├── get_vort.py
│   ├── inout.py
│   ├── __pycache__
│   ├── save_np_binary.py
│   ├── save.out
│   └── vort_x.py
└── validation
    ├── analysis
    └── convergence-to-lucas
```


Relationship between files, if important for context:  


If data was derived from another source, list source: The flow field data was produced using our in house LES solver, access is available upon request.


--------------------------

METHODOLOGICAL INFORMATION

--------------------------



Description of methods used for collection/generation of data: The data is generated, for the most part by our in-house LES solver 'Lotus'. The details are set out in the linked publication, and access can be granted upon request.


Software- or Instrument-specific information needed to interpret the data, including software and hardware version numbers: AMD nodes on the HPC architecture 'IRIDIS 5' was used to run the simulations.



--------------------------

DATA-SPECIFIC INFORMATION

--------------------------

The python files in ./analysis provide the methods for manipulation, and plotting of the data relating to the publication. The fort.9 files contain the forces, the .npy files contain checkpoints in the software to avoid expensive analysis techniques from repeating themselves (e.g. reading in flow field data). The vti, vtr, pvti, pvtr file extension denotes flow field data in paraview readable form, this dataset contains a very small fraction of that analysed, and more is available upon request.





























