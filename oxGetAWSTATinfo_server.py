#-------------------------------------------------------------------------------
# Name:        oxGetAWSTATinfo_server
# Purpose:     Analisis de l'arxiu oxAWSTATinfo_server.csv
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
    
    sServerCSVfile = option_file.getOption(options,'ServerCSVfile')
    sLogFileName = option_file.getOption(options,'LOGfilename')
    
    fLog = open(sLogFileName,'w')
    fLog.write('---------------------------------------------------------------------- \n')
    fLog.write(' oxAWSTATinfo_client options: \n')
    fLog.write('---------------------------------------------------------------------- \n')
    fLog.write(' Log file(this file): '+sLogFileName+'\n')
    fLog.write(' Input Server CSV file: '+sServerCSVfile+'\n')
    fLog.write('---------------------------------------------------------------------- \n')
   
    
    fIn = open(sServerCSVfile,'r')    
    for ele in fIn.readlines():
        #           0    1    2            3    4              5 
        #fields:: 'date time cs-uri-query c-ip cs(User-Agent) cs(Referer)\n'
        ele_list=ele.split(';')
        
    fIn.close()
    
    fLog.write('\n')
    print ' '
    
    fLog.write('---------------------------------------------------------------------- \n')
    print '----------------------------------------------------------------------'
    
    fLog.write(' Num c-ip found: '+str(len(c_ip_set_list))+'\n')
    print ' '
        
    #
    #    
    fLog.close()
    # --- END oxGetAWSTATinfo ---

