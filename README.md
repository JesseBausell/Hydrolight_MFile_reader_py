# Hydrolight_MFile_reader_py
This python notebook reformats a series of Hydrolight-generated m-files (radiative transfer outputs) into hdf5 files. This enables easier access to data for investigators, who can work with structured variables inside the hdf5 files rather than unweildy ascii files, which are difficult to utilize on a large scale. See GitHub readme for more details.

Overview:

The primary purpose of Hydrolight_MFile_reader_py is to convert so called "m-files", ascii files output by Hydrolight (radiative transfer completing computer software) into structure hdf5 files, allowing for more seemless data analyses using a coding language (e.g. matlab, python, R, etc.). The program can convert multiple m-files into hdf5 files. 

The creator (yours truly) assumes that Hydrolight_MFile_reader_py will re-format m-files generated using 
LogNorm_Draw_Hydrolight.ipynb. Thus best practices would dictate that m-files have a consistent nomenclature that begins with the letter "M" and ends in "itr_#" with # being a sequential series of integers used to sequence individual m-files (example: MFileExample_itr_0.txt, MFileExample_itr_1.txt, MFileExample_itr_2.txt, etc). Before running Hydrolight_MFile_reader_py, user should place all m-files into a single folder. Best practices suggest that this folder should be devoid of all ascii files which are not m-files. 


User Directions:
1. Run Hydrolight_MFile_reader.py
2. Select the folder containing m-files
3. Sit back and let Hydrolight_MFile_reader.py do the rest!

Inputs:
m-file folder - user-selected folder containing m-files 

Outputs:
"HDF5/" - folder contianing hdf5 files. These will be named similarly to the m-files from which they are dirived. Only the ending will be changed in the name. For example, MFileExample_itr_0.txt becomes MFileExample_itr_0.h5.



 
