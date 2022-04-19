#-------------------------------------------------------------------------------
# Name:        AWSTATlog
# Purpose:     Llibreria que carrega informacio dels arxius LOG servidor OX
#
# Format arxiu u_ex<yy><mm><dd>.log:
# ----------------------------------
# #Software: Microsoft Internet Information Services 7.5
# #Version: 1.0
# #Date: 2017-01-01 00:00:01
# #Fields: date time s-sitename s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status sc-bytes
# 2017-01-01 00:00:01 W3SVC3 172.30.22.53 GET /server/sgdwms.dll/WMS &VERSION=1.1.1&REQUEST=GetMap&FORMAT=image/jpeg&LAYERS=ox3dmtn29603ndvi&SRS=EPSG:25831&BBOX=510800.00,4655500.00,511000.00,4655675.00&WIDTH=928&HEIGHT=674 80 - 172.17.27.12 Mozilla/5.0+(compatible;+PRTG+Network+Monitor+(www.paessler.com);+Windows) - 200 0 0 51029
# 2017-01-01 00:00:01 W3SVC3 172.30.22.53 GET /client/icc/ - 80 - 172.30.22.2 - - 200 0 0 1856
# 2017-01-01 00:00:06 W3SVC3 172.30.22.53 GET /server/sgdwms.dll/wms REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.1.1 80 - 172.30.22.2 - - 200 0 0 197225
# 2017-01-01 00:00:06 W3SVC3 172.30.22.53 GET /server/sgdwms.dll/WMS &VERSION=1.1.1&REQUEST=GetMap&FORMAT=image/jpeg&LAYERS=ox3dmtn29606ndvi&SRS=EPSG:25831&BBOX=510800.00,4655500.00,511000.00,4655675.00&WIDTH=928&HEIGHT=674 80 - 172.17.27.12 Mozilla/5.0+(compatible;+PRTG+Network+Monitor+(www.paessler.com);+Windows) - 200 0 0 47235
# 2017-01-01 00:00:07 W3SVC3 172.30.22.53 GET /server/sgdwms.dll/wms REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.1.1 80 - 172.30.22.3 - - 200 0 0 197225
# 2017-01-01 00:00:09 W3SVC3 172.30.22.53 GET /client/icc/ - 80 - 172.30.22.3 - - 200 0 0 1856
# 2017-01-01 00:00:11 W3SVC3 172.30.22.53 GET /client/icc/ - 80 - 172.30.22.2 - - 200 0 0 1856
# 2017-01-01 00:00:14 W3SVC3 172.30.22.53 GET /server/sgdwms.dll VERSION=1.1.1&SERVICE=WMS&REQUEST=GetMap&LAYERS=Catalunya+10cm.+2011&STYLES=&SRS=EPSG%3A23031&BBOX=262736.3384660574,4541322.640908446,475395.5040186554,4728963.081101915&WIDTH=425&HEIGHT=375&FORMAT=image%2Fjpeg&EXCEPTIONS=application/vnd.ogc.se_xml&_SPATINEO_ID=13483 80 - 54.217.35.217 Spatineo+Monitor+GetMapBot+(http://www.spatineo.com/spatineo-monitor;+MonitoredService+http://directory.spatineo.com/service/13483) - 206 0 0 1032
# ...
#
# Author:      a.termens
# Created:     01/02/2018
# Copyright:   (c) a.termens 2018
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#import sys
#import os
#import shutil
#import string


def load(logname):
    logdat_dict_list=[]
    f=open(logname,'r')
    for line in f.readlines():
#        line_list=string.split(string.lstrip(string.rstrip(line)),' ')
        line_list=line.lstrip().rstrip().split(' ')
        if not ('#' in line_list[0]):
            #len(line_list)=16
            #Index:  0    1    2          3    4         5           6            7      8           9    10             11          12        13           14              15
            #Fields: date time s-sitename s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status sc-bytes
            if len(line_list)==16:
                logdat_dict={}
                logdat_dict['date']=line_list[ 0]
                logdat_dict['time']=line_list[ 1]
                logdat_dict['s-sitename']=line_list[ 2]
                logdat_dict['s-ip']=line_list[ 3]
                logdat_dict['cs-method']=line_list[ 4]
                logdat_dict['cs-uri-stem']=line_list[ 5]
                logdat_dict['cs-uri-query']=line_list[ 6]
                logdat_dict['s-port']=line_list[ 7]
                logdat_dict['cs-username']=line_list[ 8]
                logdat_dict['c-ip']=line_list[ 9]
                logdat_dict['cs(User-Agent)']=line_list[10]
                logdat_dict['cs(Referer)']=line_list[11]
                logdat_dict['sc-status']=line_list[12]
                logdat_dict['sc-substatus']=line_list[13]
                logdat_dict['sc-win32-status']=line_list[14]
                logdat_dict['sc-bytes']=line_list[15]
                logdat_dict_list.append(logdat_dict)
            else:
                print ' Erroneous line? ',line_list
    f.close()
    return logdat_dict_list

def main():
    pass

if __name__ == '__main__':
#    main()
    arxiu = r'\\icgc.local\dades\geoproces\Fotogrametria_i_Teledeteccio\projectes\ortoXpres\8_WorkingArea\81_AWSTATlog\orchid1-1701\u_ex170101.log'
    load(arxiu)
