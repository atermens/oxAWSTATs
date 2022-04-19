#-------------------------------------------------------------------------------
# Name:        oxGetAWSTATinfo
# Purpose:     Generar un arxiu AWSTATinfo_<dia>.txt amb tota la informacio dels diferents 
#              arxius LOG del mapproxy d'ortoXpres. 
#
# Usage:       oxGetAWSTATinfo.py  oxAWSTAT.xml
#
#
# Els arxius LOG estan emmagatzemats com:
#
#     <root_path>orchid<n>-<yy><mm>\u_ex<yy><mm><dd>.log
# 
#date       time     s-sitename s-ip         cs-method cs-uri-stem  cs-uri-query s-port cs-username c-ip        cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status sc-bytes
#2017-12-12 00:00:05 W3SVC3     172.30.22.53 GET       /client/icc/ -            80     -           172.30.22.2 -              -           200       0            0               1856
#2017-12-12 00:00:08 W3SVC3     172.30.22.53 GET       /client/icc/ -            80     -           172.30.22.3 -              -           200       0            0               1856
#
#date       time     s-sitename s-ip         cs-method cs-uri-stem            cs-uri-query                                                                                                                                              s-port cs-username c-ip         cs(User-Agent)                                                             cs(Referer) sc-status sc-substatus sc-win32-status sc-bytes
#2017-12-12 00:00:00 W3SVC3     172.30.22.53 GET       /server/SgdWms.dll/WMS &VERSION=1.1.1&REQUEST=GetMap&FORMAT=image/jpeg&LAYERS=ox3dcosta2015&SRS=EPSG:25831&BBOX=358850.00,4554750.00,358950.00,4554800.00&WIDTH=745&HEIGHT=558   80     -           172.17.27.12 Mozilla/5.0+(compatible;+PRTG+Network+Monitor+(www.paessler.com);+Windows) -           200       0            0                90390
#2017-12-12 00:00:03 W3SVC3     172.30.22.53 GET       /server/sgdwms.dll/wms REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.1.1                                                                                                         80     -           172.30.22.3  -                                                                          -           200       0            0               253300
#2017-12-12 00:00:05 W3SVC3     172.30.22.53 GET       /server/sgdwms.dll/wms REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.1.1                                                                                                         80     -           172.30.22.2  -                                                                          -           200       0            0               253300
#2017-12-12 00:00:06 W3SVC3     172.30.22.53 GET       /server/sgdwms.dll/WMS &VERSION=1.1.1&REQUEST=GetMap&FORMAT=image/jpeg&LAYERS=ox3durbanes2015&SRS=EPSG:25831&BBOX=479000.00,4662800.00,479300.00,4663000.00&WIDTH=928&HEIGHT=674 80     -           172.17.27.12 Mozilla/5.0+(compatible;+PRTG+Network+Monitor+(www.paessler.com);+Windows) -           200       0            0               159925
#
#
# Author:      a.termens
# Created:     02/02/2018
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
import AWSTATlog



def GetHeader():
    sep=';'
    fields = 'date time s-sitename s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status sc-bytes\n'
    fields_list = fields.split(' ')
    return sep.join(fields_list)

def GetHeaderClient():
    sep=';'
    fields = 'date time c-ip\n'
    fields_list = fields.split(' ')
    return sep.join(fields_list)

def GetHeaderServer():
    sep=';'
    fields = 'date time cs-uri-query c-ip cs(User-Agent) cs(Referer)\n'
    fields_list = fields.split(' ')
    return sep.join(fields_list)
    
if __name__ == '__main__':
    options=option_file.loadOptions()
    
    sClientCSVfile = option_file.getOption(options,'ClientCSVfile')
    sServerCSVfile = option_file.getOption(options,'ServerCSVfile')
    sCsUriStemfile = option_file.getOption(options,'CsUriStemfile')

    sRootDir = option_file.getOption(options,'RootDir')   
    sLogFileName = option_file.getOption(options,'LOGfilename')
    sYear = option_file.getOption(options,'Year')
    yy=sYear[2:]
    
    fLog = open(sLogFileName,'w')
    fLog.write('---------------------------------------------------------------------- \n')
    fLog.write(' oxAWSTATinfo options: \n')
    fLog.write('---------------------------------------------------------------------- \n')
    fLog.write(' Log file(this file): '+sLogFileName+'\n')
    fLog.write(' Output Client CSV file: '+sClientCSVfile+'\n')
    fLog.write(' Output Server CSV file: '+sServerCSVfile+'\n')
    fLog.write(' Output cs-uri-stem file: '+sCsUriStemfile+'\n')
    fLog.write(' Root path: '+sRootDir+'\n')
    fLog.write(' Year: '+sYear+' >> '+yy+'\n')
    fLog.write('---------------------------------------------------------------------- \n')
   
    
    fOut1 = open(sClientCSVfile,'w')    
    fOut1.write(GetHeaderClient()) # Escrivim header

    fOut2 = open(sServerCSVfile,'w')    
    fOut2.write(GetHeaderServer()) # Escrivim header

    fOut3 = open(sCsUriStemfile,'w')    
        
    num_total_reg = 0
    num_client_reg = 0
    num_server_reg = 0
   
    s_sitename_list=[]
    s_ip_list=[]
    cs_method_list=[]
    c_ip_list=[]
    
    for ele in os.listdir(sRootDir):
        # cal veure si <ele> es un subdirectori de tipus <machine>-<YY><MM> (i.e. orchid1-1707)
        sInDir = os.path.join(sRootDir,ele)
        if os.path.isdir(sInDir) :
            ele_list=ele.split('-')
            sOrchid=ele_list[0]
            # cal veure si es de l'any a processar...
            if yy in ele_list[1]:
                fLog.write(' processem directori '+ele+'\n')
                # ara processem tots els arxius u_ex*.log que hi ha en el directori
                for arxiu in os.listdir(sInDir):
                    if arxiu.endswith(".log") and arxiu.startswith("u_ex"):
                        fLog.write('   carreguem arxiu '+arxiu+'\n')
                        print '   carreguem arxiu '+arxiu
                        for dict in AWSTATlog.load(os.path.join(sInDir,arxiu)):
                            num_total_reg += 1
                            s_sitename_list.append(dict['s-sitename'])
                            s_ip_list.append(dict['s-ip'])
                            cs_method_list.append(dict['cs-method'])
                            c_ip_list.append(dict['c-ip']+' '+dict['cs(User-Agent)']+' '+dict['cs(Referer)'])
                            #
                            if 'CLIENT' in dict['cs-uri-stem'].upper():
                                llista1=[]
                                llista1.append(dict['date'])
                                llista1.append(dict['time'])
                                llista1.append(dict['c-ip']) 
                                line1=';'
                                fOut1.write(line1.join(llista1)+'\n')
                                num_client_reg += 1
                            elif 'SERVER' in dict['cs-uri-stem'].upper():
                                llista2=[]
                                llista2.append(dict['date'])
                                llista2.append(dict['time'])
                                llista2.append(urllib.unquote_plus(dict['cs-uri-query']))
                                llista2.append(dict['c-ip']) 
                                llista2.append(urllib.unquote_plus(dict['cs(User-Agent)'])) 
                                llista2.append(dict['cs(Referer)'])
                                line2=';'
                                fOut2.write(line2.join(llista2)+'\n')
                                num_server_reg += 1
                            else:
                            	llista3=[]
                            	llista3.append(dict['date'])
                            	llista3.append(dict['time'])
                            	llista3.append(dict['cs-uri-stem'])
                            	llista3.append(dict['c-ip'])
                            	llista3.append(dict['cs(User-Agent)'])
                            	llista3.append(dict['cs(Referer)'])
                            	line3=';'
                                fOut3.write(line3.join(llista3)+'\n')
                            #
    fOut1.close()
    fOut2.close()
    fOut3.close()
    
    fLog.write('\n')
    print ' '
    
    fLog.write('---------------------------------------------------------------------- \n')
    print '----------------------------------------------------------------------'
    
    fLog.write(' Num. total registres processats: '+str(num_total_reg)+'\n')
    print ' Num. total registres processats: ',num_total_reg
    
    fLog.write(' Num. registres client:           '+str(num_client_reg)+'\n')
    print ' Num. registres client:           ',num_client_reg
    
    fLog.write(' Num. registres server:           '+str(num_server_reg)+'\n')
    print ' Num. registres server:           ',num_server_reg
    
    fLog.write('---------------------------------------------------------------------- \n')    
    print '----------------------------------------------------------------------'
    
    fLog.write('\n')
    print ' '
    
    msg = ' s-sitename: '
    for ele in list(set(s_sitename_list)):
    	if len(ele)>0:
        	msg += ele.lstrip().rstrip()+' / '
    msg += '\n'
    fLog.write(msg)
    print msg
    
    fLog.write('---------------------------------------------------------------------- \n')    
    print '----------------------------------------------------------------------'

    fLog.write('\n')
    print ' '
    
    msg = ' s-ip: '
    for ele in list(set(s_ip_list)):
        if len(ele)>0:
            msg += ele.lstrip().rstrip()+' / '
    msg += '\n'
    fLog.write(msg)
    print msg
    
    fLog.write('---------------------------------------------------------------------- \n')    
    print '----------------------------------------------------------------------'

    fLog.write('\n')
    print ' '

    msg = ' cs-method: '
    for ele in list(set(cs_method_list)):
        if len(ele)>0:
            msg += ele.lstrip().rstrip()+' / '
    msg += '\n'
    fLog.write(msg)
    print msg
    
    fLog.write('---------------------------------------------------------------------- \n')    
    print '----------------------------------------------------------------------'

    fLog.write('\n')
    print ' '
    
    msg = ' c-ip cs(User-Agent) cs(Referer): '
    for ele in list(set(c_ip_list)):
        if len(ele)>0:
            msg += ele.lstrip().rstrip()+' / '
    msg += '\n'
    fLog.write(msg)
    print msg
    #
    #    
    fLog.close()
    # --- END oxGetAWSTATinfo ---

