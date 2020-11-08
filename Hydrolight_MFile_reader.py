# Hydrolight_MFile_reader
# Jesse Bausell
# October 31, 2020
#
# This python script reformats a series of Hydrolight-generated m-files (radiative 
# transfer outputs) into hdf5 files. This enables easier access to data for investigators, 
# who can work with structured variables inside the hdf5 files rather than unweildy ascii 
# files, which are difficult to utilize on a large scale. See GitHub readme for more details.

### 1. Import python libraries into the workspace
import h5py
import numpy as np
from tkinter import filedialog as fd
import os

### 2. Define functions used for the script.

def createFolder(directory):
    """ createFolder searches for a dirctory specified by the user. If there is none, it creates one"""
    try:
        if not os.path.exists(directory): # If the folder doesn't exist
            os.makedirs(directory) # Create a folder
    except OSError: # If there is an error other than a non-existant folder
        print ('Error: Creating directory. ' +  directory) # report error and shut down createFolder


def hdf5_fileWRITER(filE_NAME,HE53_dict):
    """Takes the python dictionary that was generated by ascii_MFILE_compiler and writes them
    into a hdf5 (.h5) file. Data within hdf5 file is formatted the same as the aforementioned 
    python dictionary. User should note however that "bb/b ratio" will be changed to "bb fraction"
    in all headers.
    Inputs: 
        filE_NAME - name of future hdf5 file that will contain dictionary data
        HE53_dict - dictionary formatted by ascii_MFILE_compiler
    Outputs:
        filE_NAME.h5 - hdf5 file containing python dictionary data"""
    filE_NAME = filE_NAME[:-4]
    with h5py.File(filE_NAME + '.h5','w') as hf: # Create an open hdf5 file for writing.
        for k in HE53_dict:
            # for-loop disects the m-file dictionary and writes data and dictionary elements
            # into a hdf5 file.
            k1 = k.replace('/','-') # replace the forward slash with a hyphen
            hf.create_group(k) # Create a key/element in hdf5 file based on nested python dictionary
            for l in HE53_dict[k]:
                # Within the python dictionary, take all elements (keys and data) and incorporate them 
                # into hdf5 file
                hf[k][l] = HE53_dict[k][l] # Create new nested element with data in hdf5 file


def ASCII_to_hdf5(fileNAME_mfile):
    """ASCII_to_hdf5 takes an ascii file produced by Hydrolight (m-file) and puts the data into
    a python dictionary.
    Input:
        fileNAME_mfile - name of the ascii file
    Output:
        Hydro_OUTPUT - python dictionary containing data from ascii file"""
    with open(fileNAME_mfile) as FID_mFILE: # Open a Hydrolight m-file that is prescribed by the user
        Hydro_OUTPUT = {} # Create an empty dictionary to store all of the data extracted from the
        # Before any data is collected and stored, process the first four lines of the m-file
        for n in range(4): 
            # for-loop discards the first four lines of mfile text because they are worthless~
            tLINE = FID_mFILE.readline() # Grab a line from the mfile, but don't save it
            #print(n,tLINE)
            if n == 1: 
                # if the script is examining the second header line of the entire m-file (sometimes called ascii file)
                tLINE = tLINE.split() # Assign the second header line to a variable and split it into a list
                wv_NUM = int(tLINE[0]) # Take the first list element (number of wavelengths). Set it equal to wv_NUM
        keY = 0 # Set Key equal to 0. This variable will determine when to break the subsequent while loop
        # every time the subequent while loop doesn't complete itself from start to finish, 
        while 1:
            # while loop will cycle through the entire m-file until it reaches the end. It will allow
            # all data to be examined, filtered, and stored in the Hydro_OUTPUT dictionary
            #######################################################################################
            if keY > 1: 
                # if script is unable to run twice
                break # break the while loop!
            ### The code below places ascii data into a dictionary.
            #######################################################################################
            try: # attempt to run the following code for each while-loop iteration
                ### 1. For each section of the ascii file, prepare the first three header lines
                temP_DICT = {} # Create an empty dictionary with each new while loop iteration
                temP_DICT['linE']  = FID_mFILE.readline()[:-1].split('"') # Grab one line of the m-file
                temP_DICT['linE2'] = FID_mFILE.readline()[:-1].split('"') # take the second line of the m-file and (again) split it by "
                temP_DICT['linE3'] = FID_mFILE.readline()[:-1].split('"') # take the third line of the m-file and (again) split it by "
                #print(temP_DICT['linE3'])
                for t in temP_DICT:
                    # for-loop cycles through the temporary dictionary (temP_DICT), which contains
                    # ascii data headers, and eliminates empty list elements.
                    for i in np.flip(np.arange(len(temP_DICT[t])),0):
                        # nested for-loop removes empty elements from each dictionary key (list)
                        if not temP_DICT[t][i].strip():
                            # if the list element is empty...
                            temP_DICT[t].pop(i) # excise the element from the list completely
                if temP_DICT['linE'] == []:
                    # If the first line of the ascii header is empty
                    temP_DICT['linE'] = temP_DICT['linE2'] # make the first ascii header the second
                    temP_DICT['linE2'] = [] # make the second ascii header the first
                ################################################################################################################################    
                ### 2. Now that the first three header lines have been fixed, try and determine the 
                ### dimensions of the data below the three-line header
                try:
                    # If the last element of the line1 list contains number of rows and columns, create variables
                    roW,coL = np.asarray(temP_DICT['linE'][-1].split(),dtype=int) # take the last list element (matrix dimensions) and split it
                    temP_DICT['linE'].pop(-1) # remove last element from the line 1 list
                except:
                    # If there are no row and column values listed in line 1 list
                    coL = np.nan # set column number equal to nan
                Hydro_OUTPUT[temP_DICT['linE'][0]] = {} # Create a dictionary within a dictionary
                Hydro_OUTPUT[temP_DICT['linE'][0]]['Meta'] = temP_DICT['linE'][-1] # Include a metadata description of each nested dictionary
                ################################################################################################################################        
                ### 3. m-file sections have several different formats. Some are matrices, others are headered columns
                ### It is therefore important to distinguish between each type of m-file section and preceed accordingly
                if coL == len(temP_DICT['linE3']):
                    # If the number of column headers, as indicated in the first line of the header, is the same as the 
                    # number of column headers listed in the third line of the header. These AOPs are typically modeled 
                    # according to wavelength, but NOT according to depth.
                    for r in range(roW):
                        # for-loop sorts through data row-by-row and sorts them into the appropriate dictionary lists.
                        # the for-loop will run for as many iterations as there are subsequent rows of data.
                        linE4 = FID_mFILE.readline()[:-1] # Grab a new line of data and remove end-of-line character
                        if "in air" in linE4:
                            # If the words, "in air" appear in the row of data...
                            INDr = linE4.rfind('"') # Find index the end of the "in air" statement
                            linE4 = '-1 ' + linE4[INDr+1:] # replace "in air" with "-1" within the string
                        linE4 = np.asarray(linE4.split(),dtype=float) # linE4 string and make it into a numpy array
                        for c,k3 in enumerate(temP_DICT['linE3']):
                            # nested for-loop distributes linE4 into appropriate dictionary elements via indexing
                            try:
                                # if nested Hydro_OUTPUT dictionary key (and element) already exist
                                Hydro_OUTPUT[temP_DICT['linE'][0]][k3] = np.append(Hydro_OUTPUT[temP_DICT['linE'][0]][k3],linE4[c]) #append
                            except:
                                # if nested Hydro_OUTPUT dictionary key (and element) do not yet exist
                                Hydro_OUTPUT[temP_DICT['linE'][0]][k3] = np.array(linE4[c]) #create a new one               
                else:
                    # If the number of columns headers, as indicated in the first line of the header, is NOT the same as 
                    # the number of column headers listed in the third line of the header. These AOPs are typically structured
                    # as a 2D matrix, with one matrix dimension representing depth bins and the other dimension representing 
                    # wavelengths
                    ### Set up the appropriate dictionary keys/elements using the ascii header
                    temP_DICT['linE3'].pop(0) # remove the first element of the third header line (now a list) 
                    try:
                        # Attempt to convert the rest of the third header line  (now a list) into a numpy array
                        Hydro_OUTPUT[temP_DICT['linE'][0]]['depth'] = np.asarray(temP_DICT['linE3'][0].split(),dtype=float)
                    except:
                        # If the list to numpy array conversion (see above) was unsuccessful, it means that the first list element is a string
                        temP_DICT['linE3'][0] = -1 # replace the first list element with "-1"
                        deptH = [temP_DICT['linE3'][0]] + temP_DICT['linE3'][1].split() # Re-create a list with the third header 
                        Hydro_OUTPUT[temP_DICT['linE'][0]]['depth'] = np.asarray(deptH,dtype=float) # Convert list of depths into numpy array
                    ### Set up the row and column numbers, as well as a nan-matrix in which to place data
                    coL = len(Hydro_OUTPUT[temP_DICT['linE'][0]]['depth']) + 1 # calculate the number of columns based on depth bins
                    roW = wv_NUM # re-assign the number of rows based on the number of wavelengths in the m-file
                    TEMP_MATRIX = np.ones([roW,coL])*np.nan # Create a nan matrix in which to place AOP and wavelenth data
                    ### Fill TEMP_MATRIX with data from m-file                 
                    for r in range(roW):
                        # for-loop goes through the m-file row by row and fills the nan-matrix (TEMP_MATRIX)
                        linE4 = np.asarray(FID_mFILE.readline()[:-1].split(),dtype=float) # grab line from m-file. Convert to numpy array
                        TEMP_MATRIX[r,:] = linE4 # Fill row of TEMP_MATRIX
                    Hydro_OUTPUT[temP_DICT['linE'][0]]['data'] = TEMP_MATRIX[:,1:] # Assign all columns (except for the first) of TEMP_MATRIX as "data"
                    Hydro_OUTPUT[temP_DICT['linE'][0]]['wvl'] = TEMP_MATRIX[:,0] # Assign first column of TEMP_MATRIX as "wvl"
                keY = 0 # upon successful completion of "try" script, reset keY to zero
            except:
                keY += 1 # if "try" script fails to run for ANY REASON, increase keY by one
                pass # skip to the next ascii header section
    return(Hydro_OUTPUT) # returns full ascii file in a dictionary
                

### 3. Create a script that converts Hydrolight m-files one at a time
### 3a. Create  new folder in which to place newly-created HDF5 files
template_dir = fd.askdirectory() # Select directory containing m-files
if '/' in template_dir:
    # If files are on a mac
    dasH = '/' # Folder separator for directory pathway
else:
    # If files are on a pc
    dasH = '\\' # Folder separator for directory pathway
dasH_IND = template_dir.rfind(dasH) # Find the last nested directory
repository_dir = template_dir[:dasH_IND]+dasH+'HDF5'+dasH # Create a new pathway for HDF5 files
createFolder(repository_dir) # Create a new folder adjacent to m-file folder
matLISt = os.listdir(template_dir) # list all files in m-file directory
### 3b. Covert m-files into HDF5
for i,mFILE in enumerate(matLISt):
    # This for-loop cyles through m-files in user-selected folder. Data in each m-file (ascii)
    # is re-formatted into a hdf5 file (.h5) which is placed into a folder named "hdf5" 
    # adjacent to the user-selected m-file folder.
    try: # If mFILE is a Hydroligth m-file
        HE53_dict = ASCII_to_hdf5(template_dir+dasH+mFILE) # Puts m-file data into dictionary
        hdf5_fileWRITER(repository_dir+mFILE,HE53_dict) # Converts dictionary into hdf5 file
    except: # If mFILE is NOT a Hydrolight m-file 
        pass # Ignore it!
