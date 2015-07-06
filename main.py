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


sys.path.append('/Users/Oli/work/python/minions')

from log_file_setup import log_files
# from analysis_modules import data
from log_file_setup import Tee
import matplotlib.pyplot as plt
from gen_class import gen
from data_import import imp
from plotter_class import plotter
from ana_data import ana_data
from ana_res import ana_res
from plotter import *
from csv_list_class import csv_list



a = ana_data()
ar = ana_res()
g = gen()
l = log_files()
i = imp() 
p = plotter()
hp = histplot()
c  =csv_list()





''' Path for root directory with .trc files '''
''' Windows vs. Linux directory separator ??'''
# 

pflag = 1
# Oliver's mac path
cwd = '/Users/Oli/work/dBLM_readout/IP2/data/' 
# fn.set_start_directory('C:\\work\\diamonds\\data\\store\\UFOs')
fn.set_start_directory(cwd,pflag)
fn.start_direc()
fn.create_infra_struc(cwd,pflag)

'''Sets name for log file. Log file is created in the directory of the python scripts'''

fn.log_file_set('log',pflag)

f = open(fn.log_file_path,'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)



'''all: searches for .trc files  in root AND sub directories'''
'''only: searches for .trc files ONLY in root'''
flag = 'all'
# aflag = 'force'
aflag = '0'
fn.converter(flag,aflag,pflag)
# fn.create_f_list(flag,pflag)

# sys.exit('script stop')


fn.run_total(pflag)
fn.run_number_reset()


fn.write_test()
fn.run_check()

# sys.exit('script stop')

'''Converts the .trc files listed in f_list'''    

for i in fn.f_list:
    print i
    print i[0]
    if i[0] == '0':
        g.printer('Running converter',pflag)
        d.data_convert(cwd,i,fn.data_path,fn.param_path,fn.raw_data_path)
        
        i[0] = 1
        print i
    else:
        g.printer('Skip data',pflag)
# while fn.run_number_load() < fn.run_total_load(): 
#     d.data_convert(cwd,fn.f_list[fn.run_number_load()],fn.data_path,fn.param_path,fn.raw_data_path)

c.csv_file_saver(fn.c_dir,'f_list.csv',fn.f_list,1,pflag)
print 'converting of data finished !!'
f.close

fn.clean_up()