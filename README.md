# Hydrolight_MFile_reader_py
This python notebook reformats a series of Hydrolight-generated m-files (radiative transfer outputs) into hdf5 files. This enables easier access to data for investigators, who can work with structured variables inside the hdf5 files rather than unweildy ascii files, which are difficult to utilize on a large scale. See GitHub readme for more details.

Overview:

The primary purpose of Hydrolight_MFile_reader_py is to convert so called "m-files", ascii files output by Hydrolight (radiative transfer completing computer software) into structure hdf5 files, allowing for more seemless data analyses using a coding language (e.g. matlab, python, R, etc.). The program can convert multiple m-files into hdf5 files. It also selects sevaral values (chosen by me) from m-files/hdf5 files and publishes them in a csv file (rows = filename, columns = variable). These selected variables (listed below) are conducive to my personal research needs. However, I have provided detailed annotation of my code which are intended to allow a user to make alterations to the original script if he/she wants to change the variables output to the csv file. 

The creator (yours truly) assumes that Hydrolight_MFile_reader_py will re-format m-files generated using 
LogNorm_Draw_Hydrolight.ipynb. Thus best practices would dictate that m-files have a consistent nomenclature that begins with the letter "M" and ends in "itr_#" with # being a sequential series of integers used to sequence individual m-files (example: MFileExample_itr_0.txt, MFileExample_itr_1.txt, MFileExample_itr_2.txt, etc). Before running Hydrolight_MFile_reader_py, user should place all m-files into a single folder. Best practices suggest that this folder should be devoid of all ascii files which are not m-files. 


User Directions:
1. Run Hydrolight_MFile_reader_py
2. Select the folder containing m-files
3. Sit back and let Hydrolight_MFile_reader_py do the rest!

Inputs:
m-file folder - user-selected folder containing m-files 

Outputs:
"hdf5/" - folder contianing hdf5 files. These will be named similarly to the m-files from which they are dirived. Only the ending will be changed in the name. For example, MFileExample_itr_0.txt becomes MFileExample_itr_0.h5.
Ch2_HE53_bbph#.###bbmin$.$$$.csv - csv file containing variables corresponding with the crator's (my) research needs. 
  #.### and $.$$$ denote backscatter/scatter fraction of phytoplankton and minerals. These are generated from m-files automatically. All m-files in a given folder should have THE SAME #.### and $.$$$.

m-file - name of the original Hydrolight m-file from which data came
Index - iteration, or series number at the end of each m-/hdf5 file 
Chlorophyll (ug/L) - input chlorophyll
CDOM (/m) - input Gelbstoff absorption (440 nm)
TSM (g/m^3) - input total suspended sediment/total suspended matter (I use these interchangeably in readme and annotations)
kd320 - diffuse attenuation coefficient 320 nm
kd780 - diffuse attenuation coefficient 780 nm
Kd412 - diffuse attenuation coefficient 412 nm
Kd667 - diffuse attenuation coefficient 667 nm
aph443 - phytoplankton absorption 443 nm
ag443 - Galbstoff absorption 443 nm
amin443 - mineral absorption 443 nm
bb_ph667 - phytoplankton backscattering 667 nm
bb_min667 - mineral backscattering 667 nm
** all AOP/IOP data represent the most shallow depth bin within the water column (e.g. 0 - bin size)



 
