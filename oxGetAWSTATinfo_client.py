#-------------------------------------------------------------------------------
# Name:        oxGetAWSTATinfo_client
# Purpose:     Analisis de l'arxiu oxAWSTATinfo_client.csv
#
# Author:      a.termens
# Created:     05/02/2018
# Copyright:   (c) a.termens 2018
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import sys
import os
import string
#import csv,shutil,re
import urllib

import option_file
  
if __name__ == '__main__':
    options=option_file.loadOptions()
    
    sClientCSVfile = option_file.getOption(options,'ClientCSVfile')
    sLogFileName = option_file.getOption(options,'LOGfilename')
    
    fLog = open(sLogFileName,'w')
    fLog.write('---------------------------------------------------------------------- \n')
    fLog.write(' oxAWSTATinfo_client options: \n')
    fLog.write('---------------------------------------------------------------------- \n')
    fLog.write(' Log file(this file): '+sLogFileName+'\n')
    fLog.write(' Input Client CSV file: '+sClientCSVfile+'\n')
    fLog.write('---------------------------------------------------------------------- \n')
   
    
    c_ip_list=[]
    
    fIn = open(sClientCSVfile,'r')    
    for ele in fIn.readlines():
        ele_list=ele.split(';')
        if not('c-ip' in ele_list[2]):
            c_ip_list.append(ele_list[2].rstrip().lstrip())
    fIn.close()
    
    fLog.write('\n')
    print ' '
    
    fLog.write('---------------------------------------------------------------------- \n')
    print '----------------------------------------------------------------------'
    
    c_ip_set_list = list(set(c_ip_list))
    c_ip_set_list.sort()
    
    fLog.write(' Num c-ip found: '+str(len(c_ip_set_list))+'\n')
    print ' '
        
    for ele in c_ip_set_list:
        if len(ele)>0:
            fLog.write(ele+'\n')
    #
    #    
    fLog.close()
    # --- END oxGetAWSTATinfo ---

