'''
Created on May 11, 2015

@author: Oli
'''
'''
Created on 24 May 2013

@author: ostein
'''
import sys
from modules import fn
from modules import data_descriptor
from modules import Tee



fn = fn()
d = data_descriptor()


''' Path for root directory with .trc files '''
''' Windows vs. Linux directory separator ??'''
# 


# Oliver's mac path
cwd = '/Users/Oli/work/dBLM_readout/IP2/data/' 
# fn.set_start_directory('C:\\work\\diamonds\\data\\store\\UFOs')
fn.set_start_directory(cwd)
fn.start_direc()
fn.create_infra_struc(cwd,1)



'''all: searches for .trc files  in root AND sub directories'''
'''only: searches for .trc files ONLY in root'''



fn.create_f_list('all')

fn.run_total()
fn.run_number_reset()

'''Sets name for log file. Log file is created in the directory of the python scripts'''

fn.log_file_set('log')


f = open(fn.log_file_path,'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)

fn.write_test()
fn.run_check()


'''Converts the .trc files listed in f_list'''    

while fn.run_number_load() < fn.run_total_load(): 
    d.data_convert(cwd,fn.f_list[fn.run_number_load()],fn.data_path,fn.param_path,fn.raw_data_path)


print 'converting of data finished !!'
f.close

fn.clean_up()