'''
Created on May 11, 2015

@author: Oli
'''


import struct
import math
import os
import StringIO
import pickle
import sys
from time import strftime, localtime 


from gen_class import gen

g = gen()
# from numpy import array,frombuffer,dtype

pflag = 1
# Class for setting up the file structure 

class fn:
    # sets root directory and tests writing permission
    def set_start_directory(self,direc):
        
        self.c_dir = direc
#         self.c_dir = os.getcwd()
        
        self.start=direc
        
        try:
            os.chdir(self.start)
            g.printer(direc+' is a valid path.',pflag)
        except:
            g.printer(direc+' is NOT a valid path!',pflag)
            
            g.printer('set '+self.c_dir+' to root!',pflag)
            self.start=os.getcwd()
            g.printer(os.getcwd(),pflag)
            
        os.chdir(self.start)
        
        try:
            open('test.txt','w+')
            os.remove('test.txt')
            os.chdir(self.c_dir)
        except:
            g.printer('No writing permission',pflag)
            sys.exit()
    
    # returns the root directory, if not set then sets the current directory to root 
    def start_direc(self):
        try: 
            os.chdir(self.start)
        except:
            self.start=os.getcwd()
        return self.start 
    
    # prints the current directory
    def p_dir(self):
        print os.getcwd()
        
    # lists the .trc files in ...
    def create_f_list(self,flag):
        
        os.chdir(self.start)
        self.f_list = []
        # ...in the rot directory and ALL sub directories
        if flag =='all':
            for (path, dirs, files) in os.walk(self.start):
                for ii in files:
                    if ii.endswith(".trc"):
                        self.f_list.append([path,ii])
            self.f_list_flag = 1
            self.out = 'decoding all files, sub directories'
            g.printer(self.out,pflag)
        # ...in the root directory 
        else:
            for files in os.listdir("."):
                if files.endswith(".trc"):
                    self.f_list.append([self.start,files])
            self.f_list_flag = 0   
            self.out = 'decoding files only in root directory'  
            g.printer(self.out,pflag)   
            
        return self.f_list
    
    def write_test(self):
        self.flag_writing_test = 1
        for i in self.f_list:
            os.chdir(i[0])
            try:
                open('test.p','w+')
                os.remove('test.p')
                self.flag_writing_test = 1
            except:
                self.flag_writing_test = 0
                sys.exit()
        os.chdir(self.c_dir)
        if self.run_total!=0:
            
            if self.flag_writing_test == 0:
                g.tprinter('no writing permission in all file directories',pflag)
            else:
                g.tprinter('permission to write files',pflag)

                
        else: pass
    
    # lists the .trc files in the current directory    
#     def files_in_dir(self):
#         os.chdir(self.start)
#         self.f_list = []
# #         self.start = os.getcwd()
# #         print os.getcwd()
# #         os.chdir("C:\\work\workspace\\LeCroy_1.0\\test")
#         for files in os.listdir("."):
#             if files.endswith(".trc"):
#                 self.f_list.append([self.start,files])
#         self.f_list_flag = 0   
#         self.out = 'decoding files only in root directory'     
#         return self.f_list
 
 
    def f_list_mes(self):
        print self.out
    # prints the file list with the directories and the .trc files 
    def p_f_list(self):
               
        print self.f_list
     
    # takes a specific file from the .trc file list    
    def take_file_from_f_list(self,num):
        self.f_list = self.f_list[num]
        
        return self.f_list
    
    # calculates the number of total runs and dumps it into run_total.p file
    def run_total(self):
        self.run_total=len(self.f_list)
        pickle.dump(self.run_total, open('run_total.p','w+'))

        return self.run_total

    # loads the number of total runs from the run_total. p file    
    def run_total_load(self):
        self.run_total=pickle.load(open('run_total.p','r'))
        
        return self.run_total
    
    # resets the current run number and dumps it into run_number.p file
    def run_number_reset(self):
        self.run_number_reset = 0
        pickle.dump(self.run_number_reset, open('run_number.p','w+'))
        
        return self.run_number_reset

    # loads the current run number from run_number.p file
    def run_number_load(self):
        os.chdir(self.start)
        self.run_number=pickle.load(open('run_number.p','r'))
        
        return self.run_number
    def create_infra_struc(self,path,pflag):
        g.tprinter('Running create_infra_struc',pflag)
        self.data_path = os.path.join(path,'data')
        self.param_path = os.path.join(path,'param')
        self.raw_data_path = os.path.join(path,'raw_data')
        self.log_path = os.path.join(path,'log')
        if os.path.exists(self.data_path) is not True:
            os.mkdir(self.data_path)
        if os.path.exists(self.param_path) is not True:
            os.mkdir(self.param_path)
        if os.path.exists(self.log_path) is not True:
            os.mkdir(self.log_path) 
        if os.path.exists(self.raw_data_path) is not True:
            os.mkdir(self.raw_data_path) 
            
            
    
    # creates a log file in the root directory where all the output during the decoding is written
    # no data or parameters are written into this file     
    def log_file_set(self,name):
        self.creat_time = strftime("%Y%m%d_%H%M", localtime())
        self.log_file_path=os.path.join(self.log_path,str(name)+'_'+self.creat_time+'.txt')
        print self.log_file_path
        self.log_file=open(self.log_file_path,'w+')
        
        print >> self.log_file, 'Dec_1_0 Log_file'
        print >> self.log_file, ''
        print >> self.log_file, 'Log_file dir: '+str(self.c_dir)
        print >> self.log_file, 'Log_file name: '+str(name)+'_'+self.creat_time+'.txt'
        print >> self.log_file, ''
        print >> self.log_file, 'date: '+strftime("%a, %d %b %Y", localtime())
        print >> self.log_file, 'time: '+strftime("%H:%M:%S", localtime())
        print >> self.log_file, ''
        print >> self.log_file, 'current directory: '+str(self.c_dir)
        print >> self.log_file, 'root directory: '+str(self.start)
        print >> self.log_file, ''
        print >> self.log_file, self.out
        print >> self.log_file, ''
        
        
        self.log_file.close()
    
    def run_check(self):
        
        if self.run_total == 0:
            g.tprinter('No .trc files found.',pflag) 


    
    # returns the log file path    
    def log_path(self):
        return self.log_file_path
            
    def clean_up(self):
        os.chdir(self.start)
        os.remove('run_total.p')
        os.remove('run_number.p')
        os.chdir(self.c_dir)

# class to redirect the output to the console AND the log file 
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

# f = open("out.txt",'w')
# original = sys.stdout
# sys.stdout = Tee(sys.stdout, f)







# def count_set():
#     global count1
#     global error_count
#     global offset1
#     global err_mess
#     
#     count1 = 0
#     error_count = 0
#     err_mes = 'err'
    
# reads the file length    
def file_len(f):
    global count1
    global error_count
    f.seek(2)
    try:
        out=int(f.read(offset1-2))
    except:
        print  err_mes
                
    return out 

# reads a string from file, f at the position, pos of the length s
def r_string(f,pos,s):

    global count1
    global error_count
    global err_mes
    
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = f.read(s)
        out = out.split('\x00')[0]
    except:
        error_count +=1
        out = err_mes   
    return out 
 
hilo = 1

# reads a byte from file, f at the position, pos 
def r_byte(f,pos):
    
    global count1
    global error_count
    global err_mes
    
    frmt = 'b'
    s=struct.calcsize(frmt)
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = struct.unpack(frmt,f.read(s))[0]
    except: 
        error_count +=1
        out = err_mes
        
    return out



# reads a short integer (2 bytes) from file, f at the position, pos 
def r_short(f,pos):
    
    global count1
    global error_count
    global err_mes
    
    frmt = 'h'
    s=struct.calcsize(frmt)
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = struct.unpack(frmt,f.read(s))[0]
    except: 
        error_count +=1
        out = err_mes
#     if hilo == 1:
#         out = struct.unpack(frmt,f.read(s))[0]
#     else:
# #         print f.read(len)
#         print >> temp,f.read(s)
#         f.seek(0)
#         out = struct.unpack(frmt,temp.read(s))[0]
 
    return out 
 
# reads a long integer (4 bytes) from file, f at the position, pos 
def r_long(f,pos):
    
    global count1
    global error_count
    global err_mes
    
    frmt = 'l'
    s=struct.calcsize(frmt)
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = struct.unpack(frmt,f.read(s))[0]
    except:
        error_count +=1
        out = err_mes     
    return out 

#reads a short integer (2 bytes) and returns b1 if integer == 1, b2 otherwise
def r_bool(f,pos,b1,b2):
    
    global count1
    global error_count
    global err_mes
    
    if r_short (f,pos) != err_mes:
        if r_short(f,pos) == 1:
            count1 -=1
            out = b1
        else:
            count1 -=1
            out = b2
    else:
        out = err_mes     
    return out 


# rounds the float number to round_digits digits after the first digit which is not zero
def rounder(fl):
    round_digits = 4
    try:
        exp = str(fl).split('e')[1]
        abso = int(math.fabs(int(exp)))
        out = float(round(fl,abso+round_digits))
    except:
        flstr = list(str(fl))
        index = 0
        for i in flstr:
            if i != '+':
                if i != '-': 
                    if i != '.':
                        if i != '0':
                            break
            index +=1
             
        out = round(fl,index-1+round_digits)    
    return out
 
# reads a single float (4 bytes) from file, f at the position, pos
def r_single(f,pos):
    
    global count1
    global error_count
    global err_mes 
    
    frmt = 'f'
    s=struct.calcsize(frmt)
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = struct.unpack(frmt,f.read(s))[0]
        out = rounder(out)
    except:
        error_count +=1
        out = err_mes     
    
#     out=round(out,digit)    
    return out 

# reads a double (8 byte) from file, f at the position, pos
def r_double(f,pos):
    
    global count1
    global error_count
    global err_mes
    
    frmt = 'd'
    s=struct.calcsize(frmt)
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = struct.unpack(frmt,f.read(s))[0]
        out = rounder(out)
    except:
        error_count +=1
        out = err_mes     
    return out 
 

# reads time string from file, f at the position, pos
def r_time(f,pos):
    
    global count1
    global error_count
    global err_mes
    
    fmt='dBBBBHH'
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = struct.unpack(fmt,f.read(struct.calcsize(fmt)))
        out = (out[-2],out[-3],out[-4],out[-5],out[-6],round(out[0],9))
        out = '%d/%02d/%02d %d:%02d:%02.9f' % out
    except:
        error_count +=1
        out= err_mes
    return out
#     return dict(zip('sec min hour day month year noop'.split(),out))

def trig_time_file(f,pos):
    
    global count1
    global error_count
    global err_mes
    
    fmt='dBBBBHH'
    f.seek(pos+offset1)
    count1 +=1
    try:
        out = struct.unpack(fmt,f.read(struct.calcsize(fmt)))
        out = (out[-2],out[-3],out[-4],out[-5],out[-6],round(out[0],9))
        out = '%d%02d%02d%02d%02d%02d' % out
    except:
        error_count +=1
        out= err_mes
    return out 
 
# def readarray(f,fmt,count,pos):
#     fmt=dtype(fmt)
#     s=fmt.itemsize*count
#     f.seek(pos+offset1)
#     return frombuffer(f.read(s),dtype=fmt,count=count)
# count1 = 0
# error_count = 0
# count1 = 0
# error_count = 0
# err_mes = 'param not readable'
# run_number = 1
# run_total = 1

# class to convert the .trc file from f_list
class data_descriptor():


    def data_convert(self,cwd,f_list,data_path,param_path,start):
        g.tprinter('Running data_converter',1)
        
        # defining global variables
#         global run_number
#         global run_total

        # directory from the f_list 
        self.direc = f_list[0]
        # .trc file from the f_list
        self.file_name = f_list[1]
        
        # changes to the given start directory
        os.chdir(str(start))
        
        # loads the total run number
        self.run_total_file = os.path.join(cwd,'run_total.p')
        self.run_total=pickle.load(open(self.run_total_file,'r'))
        print 'ok'
        # loads the run number
        self.run_number_file = os.path.join(cwd,'run_number.p')
        self.run_number=pickle.load(open(self.run_number_file,'r'))
        print 'ok'
        # increases run number by one to the current run number
        self.run_number +=1
        
        # dumps the current run number                      
        pickle.dump(self.run_number,open(self.run_number_file,'w+'))
        
        # run header with:
        # run number of total runs
        # directory name of the file
        # file name
        # date
        # time
        
        print '---------------------------------------------------------'
        print 'run '+str(self.run_number)+' of '+str(self.run_total)+' total runs'
        print 'directory name: '+str(self.direc)
        print 'file name: '+str(self.file_name)
        print 'date: '+strftime("%a, %d %b %Y", localtime())
        print 'time: '+strftime("%H:%M:%S", localtime())
        print '---------------------------------------------------------'
        
        print 'start converting'     
        
        print 'set directory to: '+str(self.direc)
        os.chdir(self.direc)
        
        global offset1      # from beginning of the file to the descriptor WAVEDES           
        global count1       # count variable
        global error_count  # count variable for exceptions
        global err_mes      # error message for exceptions
        
        count1 = 0
        error_count = 0
        err_mes = 'param not readable'  # for parameter read out 
        
        
        # try to open the input file
        print 'try to open input file'
        self.flag1 = 1
        try:        
            self.file = open(self.file_name)
            print 'done'
        except:
            print 'file does not exist, abort'
            self.flag1 = 0
        

        
        
#         #  extracts the file name as string and creates two new file ..._data and ..._param           
#         g.printer('creating files',pflag)
#         self.flag2 = 1    
#         if self.flag1==1:
#             self.buf = StringIO.StringIO(self.file_name)
#             self.fname = self.buf.read(self.file_name.find('.trc'))
#             self.data_file = open(self.fname+'_data.txt','w+')
#             g.printer(self.fname+'_data.txt',pflag)
#             self.param_file=open(self.fname+'_param.txt','w+')
#             g.printer(self.fname+'_param.txt',pflag)
#             g.printer('done',pflag)
#         else:
#             self.flag2 = 0
#             g.printer('no files created',pflag)  
        
        self.flag2 = 1        
        # search for #9 as identifier and WAVEDES as beginning of the file
        g.printer('search for identifier',pflag)
        self.flag3 = 1
        if self.flag2 == 1: 
            self.header = self.file.read(30)
            try:
                self.start=self.header.find('#9')         
                offset1 = self.header.find('WAVEDES')

                g.printer('#9 and WAVEDES found',pflag)
            except:
                self.flag3 = 0
                g.printer('#9/WAVEDES NOT found',pflag)
        else:
            self.flag3 = 0
            g.printer('stop converting',pflag)  
        
        
        # extracting parameters from the file
        g.printer('extracting parameters',pflag)
        if self.flag3 == 1:

        # count1 increases by one for every parameter 
        # in the end count one should be at 56
        # error_count increases every time when a parameter could not be read
        # instead of the parameter the err_mess is written    
            self.descriptor_name = r_string(self.file,0,8)                        #  1 DESCRIPTOR_NAME = 0   '  string
            self.template_name = r_string (self.file,16,10)                       #  2 TEMPLATE_NAME = 16   '  string
            self.comm_type = r_bool(self.file,32,'word','byte')                   #  3 COMM_TYPE = 32   '  Word (2 byte integer)
            self.comm_order = r_bool(self.file,32,'low first','high first')       #  4 COMM_ORDER = 34   '  Word (2 byte integer)
            self.wave_descriptor = r_long(self.file,36)                           #  5 WAVE_DESCRIPTOR = 36   '  Long (4 byte integer)
            self.user_text = r_long(self.file,40)                                 #  6 USER_TEXT = 40   '  Long (4 byte integer)
            self.res_desc1 = r_long(self.file,44)                                 #  7 RES_DESC1 = 44   '  Long (4 byte integer)
            self.trigtime_array = r_long(self.file,48)                            #  8 TRIGTIME_ARRAY = 48   '  Long (4 byte integer)
            self.ris_time_array =  r_long(self.file,52)                           #  9 RIS_TIME_ARRAY = 52   '  Long (4 byte integer)
            self.res_array1 = r_long(self.file,46)                                # 10 RES_ARRAY1 = 56   '  Long (4 byte integer) 
            self.wave_array_1 = r_long(self.file,60)                              # 11 WAVE_ARRAY_1 = 60   '  Long (4 byte integer)
            self.wave_array_2 = r_long(self.file,64)                              # 12 WAVE_ARRAY_2 = 64   '  Long (4 byte integer)
            self.res_array2 = r_long(self.file,40)                                # 13 RES_ARRAY2 = 68   '  Long (4 byte integer)
            self.res_array3 = r_long(self.file,72)                                # 14 RES_ARRAY3 = 72   '  Long (4 byte integer)
            self.instrument_name = r_string(self.file,76,16)                      # 15 INSTRUMENT_NAME = 76   '  string
            self.instrument_number = r_long(self.file,92)                         # 16 INSTRUMENT_NUMBER = 92   '  Long (4 byte integer)
            self.trace_label = r_string(self.file,96,10)                          # 17 TRACE_LABEL = 96   '  string
            self.reserved1 = r_short(self.file,112)                               # 18 Reserved1 = 112   '  Word (2 byte integer)
            self.reserved2 = r_short(self.file,114)                               # 19 Reserved2 = 114   '  Word (2 byte integer)
            self.wave_array_count= r_long(self.file,116)                          # 20 WAVE_ARRAY_COUNT = 116   '  Long (4 byte integer)
            self.pnts_per_screen = r_long(self.file,120)                          # 21 PNTS_PER_SCREEN = 120   '  Long (4 byte integer)
            self.first_valid_pnt = r_long(self.file,124)                          # 22 FIRST_VALID_PNT = 124   '  Long (4 byte integer)
            self.last_valid_pnt = r_long(self.file,128)                           # 23LAST_VALID_PNT = 128   '  Long (4 byte integer)
            self.firstpoint = r_long(self.file,132)                               # 24 FIRST_POINT = 132   '  Long (4 byte integer)
            self.sparsing_factor = r_long(self.file,136)                          # 25 SPARSING_FACTOR = 136   '  Long (4 byte integer)
            self.segment_index = r_long(self.file,140)                            # 26 SEGMENT_INDEX = 140   '  Long (4 byte integer)
            self.subarray_count = r_long(self.file,144)                           # 27 SUBARRAY_COUNT = 144   '  Long (4 byte integer)
            self.sweeps_per_acq = r_long(self.file,148)                           # 28 SWEEPS_PER_ACQ = 148   '  Long (4 byte integer)
            self.points_per_pair = r_short(self.file,152)                         # 29 POINTS_PER_PAIR = 152   '  Word (2 byte integer)
            self.pair_offset = r_short(self.file,154)                             # 30 PAIR_OFFSET = 154   '  Word (2 byte integer)
            self.vertical_gain = r_single(self.file,156)                          # 31 VERTICAL_GAIN = 156   '  Single (4 byte float)
            self.vertical_offset= r_single(self.file,160)                         # 32 VERTICAL_OFFSET = 160   '  Single (4 byte float)
            self.max_value = r_single(self.file,164)                              # 33 MAX_VALUE = 164   '  Single (4 byte float)
            self.min_value =  r_single(self.file,168)                             # 34 MIN_VALUE = 168   '  Single (4 byte float)
            self.nominal_bits = r_short(self.file,172)                            # 35 NOMINAL_BITS = 172   '  Word (2 byte integer)
            self.nom_subarray_count = r_short(self.file,174)                      # 36 NOM_SUBARRAY_COUNT = 174   '  Word (2 byte integer)
            self.horiz_interval = r_single(self.file,176)                         # 37 HORIZ_INTERVAL = 176   '  Single (4 byte float)
            self.horiz_offset = r_double(self.file,180)                           # 38 HORIZ_OFFSET = 180   '  Double (8 byte float)
            self.pixel_offset = r_double(self.file,188)                           # 39 PIXEL_OFFSET = 188   '  Double (8 byte float)
            self.vertunit = r_string(self.file,196,10)                            # 40 VERTUNIT = 196   '  string
            self.horunit = r_string(self.file,244,10)                             # 41 HORUNIT = 244   '  string
            self.horiz_uncertainty  = r_single(self.file,292)                     # 42 HORIZ_UNCERTAINTY = 292   '  Single (4 byte float)
            self.trigger_time = r_time(self.file,296)                             # 43 TRIGGER_TIME = 296   '  time_stamp
            self.acq_duration = r_single(self.file,312)                           # 44 ACQ_DURATION = 312   '  Single (4 byte float)
            self.record_type = r_short(self.file,316)                             # 45 RECORD_TYPE = 316   '  Word (2 byte integer)
            self.processing_done = r_short(self.file,318)                         # 46 PROCESSING_DONE = 318   '  Word (2 byte integer)
            self.reserveds = r_short(self.file,320)                               # 47 RESERVED5 = 320   '  Word (2 byte integer)
            self.ris_sweeps = r_short(self.file,322)                              # 48 RIS_SWEEPS = 322   '  Word (2 byte integer) 
            self.timebase = r_short(self.file,324)                                # 49 TIMEBASE = 324   '  Word (2 byte integer)
#             self.timebase = 1                            
            self.vert_coupling = r_short(self.file,326)                           # 50 VERT_COUPLING = 326   '  Word (2 byte integer)
            self.probe_att =r_single(self.file,328)                               # 51 PROBE_ATT = 328   '  Single (4 byte float)
            self.fixed_vert_gain = r_short(self.file,332)                         # 52 FIXED_VERT_GAIN = 332   '  Word (2 byte integer)
            self.bandwidth_limit = r_short(self.file,334)                         # 53 BANDWIDTH_LIMIT = 334   '  Word (2 byte integer)
            self.vertical_vernier = r_short(self.file,336)                        # 54 VERTICAL_VERNIER = 336   '  Word (2 byte integer)
            self.acq_vert_offset = r_short(self.file,340)                         # 55 ACQ_VERT_OFFSET = 340   '  Word (2 byte integer)
            self.wave_source = r_short(self.file,344)                             # 56 WAVE_SOURCE = 344   '  Word (2 byte integer)
            
            # writing parameters in a list
            self.param = [['descriptor_name',self.descriptor_name],['template_name',self.template_name],['comm_type',self.comm_type],['comm_order',self.comm_order],
            ['wave_discriptor',self.wave_descriptor],['user_text',self.user_text],['res_desc1',self.res_desc1],['trigtime_array',self.trigtime_array],
            ['ris_time_array',self.ris_time_array],['res_array1',self.res_array1],['wave_array_1',self.wave_array_1],['wave_array_2',self.wave_array_2],
            ['res_array2',self.res_array2],['res_array3',self.res_array3],['instrument_name',self.instrument_name],['instrument_number',self.instrument_number],
            ['trace_label',self.trace_label],['reserved1',self.reserved1],['reserved2',self.reserved2],['wave_array_count',self.wave_array_count],
            ['pnts_per_screen',self.pnts_per_screen],['first_valid_pnt',self.first_valid_pnt],['last_valid_pnt',self.last_valid_pnt],
            ['firstpoint',self.firstpoint],['sparsing_factor',self.sparsing_factor],['segment_index',self.segment_index],['subarray_count',self.subarray_count],
            ['sweeps_per_acq',self.sweeps_per_acq],['points_per_pair',self.points_per_pair],['pair_offset',self.pair_offset],['vertical_gain',self.vertical_gain],
            ['vertical_offset',self.vertical_offset],['max_value',self.max_value],['min_value',self.min_value],['nominal_bits',self.nominal_bits],
            ['nom_subarray_count',self.nom_subarray_count],['horiz_interval',self.horiz_interval],['horiz_offset',self.horiz_offset],
            ['pixel_offset',self.pixel_offset],['vertunit',self.vertunit],['horunit',self.horunit], ['horiz_uncertainty',self.horiz_uncertainty],
            ['trigger_time',self.trigger_time],['acq_duration',self.acq_duration],['record_type',self.record_type],['processing_done',self.processing_done],['reserveds',self.reserveds],
            ['ris_sweeps',self.ris_sweeps],['timebase',self.timebase],['vert_coupling',self.vert_coupling],['probe_att',self.probe_att],
            ['fixed_vert_gain',self.fixed_vert_gain],['bandwidth_limit',self.bandwidth_limit],['vertical_vernier',self.vertical_vernier],
            ['acq_vert_offset',self.acq_vert_offset],['wave_source',self.wave_source]]
            
            
            
            
            print 'number of parameters decoded: '+ str(count1)
            print 'number of errors occurred: '+str(error_count)
            self.flag4 = 1
        else:
            print 'no parameters converted'  
            self.flag4 = 0
         
        print r_time(self.file,296)
        print trig_time_file(self.file,296)
#         sys.exit('script stop') 
        #  extracts the file name as string and creates two new file ..._data and ..._param           
        g.printer('creating files',pflag)
        self.flag2 = 1    
        if self.flag1==1:
            self.buf = StringIO.StringIO(self.file_name)
            self.fname = self.buf.read(self.file_name.find('.trc'))
            g.printer('file name '+str(self.fname),pflag)
            self.nfname = self.fname.split('_')
            print self.nfname
            self.ffname = trig_time_file(self.file,296)+'_'+self.nfname[1]+'_'+self.nfname[0]+'_'+self.nfname[2]
            print self.ffname
            self.data_file = open(os.path.join(data_path,self.ffname+'_data.txt'),'w+')
#             self.data_file = open(os.path.join(data_path,trig_time_file(self.file,296)+'_'+self.fname+'_data.txt'),'w+')
            g.printer(trig_time_file(self.file,296)+'_'+self.fname+'_data.txt',pflag)
#             self.param_file=open(os.path.join(param_path,trig_time_file(self.file,296)+'_'+self.fname+'_param.txt'),'w+')
            self.param_file=open(os.path.join(param_path,self.ffname+'_param.txt'),'w+')
            g.printer(trig_time_file(self.file,296)+'_'+self.fname+'_param.txt',pflag)
            g.printer('done',pflag)
        else:
            self.flag2 = 0
            g.printer('no files created',pflag)   
        # writes param list to file 
           
        if self.flag4 == 1:
            print 'writing parameters to file'
            for i in self.param:
                print>>self.param_file, i[0],',',i[1]
            print 'done'
            self.flag5 = 1
        else:
            print 'no parameters written into ..._param file'
            self.flag5 = 0
            
        # start decoding data     
        if self.flag5 == 1:
            print 'decoding data' 
            self.segments = self.subarray_count
            self.points = self.wave_array_count/self.segments # number of data points

            # count1 increases with every data point
            # error_count increases when data could not be read
            # err_mess is written instead, must be a number!!             
            
            count1 = 0
            error_count = 0
            err_mes = 0
            
            i = 0
            #tests if data format is word (2 byte)
            #writes the data to ..._data file 
            if self.comm_type == 'word':
                print 'word'
                while (i <=self.points):                    
                    self.dcount = r_short(self.file,self.wave_descriptor+2*i)
                    print >> self.data_file, i*self.horiz_interval+self.horiz_offset,',', self.dcount*self.vertical_gain-self.vertical_offset

                    i +=1
                    
            #tests if data format is byte (1 byte)
            #writes the data to ..._data file         
            elif self.comm_type == 'byte':
                print 'byte'
                while (i <=self.points):                    
                    self.dcount = r_byte(self.file,self.wave_descriptor+i)
                    print >> self.data_file, i*self.horiz_interval+self.horiz_offset,',', self.dcount*self.vertical_gain-self.vertical_offset

                    i +=1
            else:
                print 'error'
                                  
            print 'done'
            print 'data points decoded: ' +str(count1)
            print 'errors occurred: ' +str(error_count-1)
              
         
        else:
            print 'stop converting'  
        print 'end of run'
        print
        print
            
        self.file.close()
        self.data_file.close()
        self.param_file.close()
           
            
            
            
