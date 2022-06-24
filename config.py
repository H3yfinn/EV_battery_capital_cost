"""This file is intended to be able ot be used in the beginnning of any jupyter ntoebook to set the config variables for the model. This helps to reduce clutter, as that is a big issue for notebooks. So if you ever need to chnage conifgurations, just change this. """
#%%

#import common libraries 
import pandas as pd 
import numpy as np
import glob
import os
from string import digits
# %config Completer.use_jedi = False#Jupiter lab specific setting to fix Auto fill bug

###################################################
#%%
#import and create common variables


config_folder_path = '../config'#folder where all the config files are stored. these may be input data or just general config files like names of eocnomies used, or correspondances
#have set above to config_new for now just so that its clear what is new

output_data_path = '../output_data'#this is data that is output from the model and or other processes, at least for use outside of this project

intermediate_data_path = '../intermediate_data'#this is data that is saved during the process when you reach major checkpoints, before being loaded later in assistance of creating output data. Contains subfolders to reduce the clutter

input_data_path = '../input_data'#this data shouldnt be interacted with manually. rather it is just data you take from another source, maybe reformat, and then put here. eg. EGEDA Data

###################################################
#%%

# Senareo = "Reference"  #can fix spelling of all things later. 
# Senareo = "Net-zero"  
MIN_YEAR = 2018
MAX_YEAR = 2050


###################################################
#%%