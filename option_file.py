#! /usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        option_file
# 
# Author:      a.termens
# Created:     01/02/2018
# Copyright:   (c) a.termens 2018
# Licence:     GPL
#-------------------------------------------------------------------------------
import sys
import os
import string
import xml.etree.ElementTree as ET

def loadOptions():
    #usage <oxGetSIIexe> <OptionsFile>
    if len(sys.argv)<2:
        print ' Invalid number of arguments!!!'
        exit(-1)
    tree=ET.parse(sys.argv[1]) # carreguem xml amb opcions
    return tree.getroot()

    
def getOption(root,inkey):  
    for child in root:
        option = child.attrib
        key=string.lstrip(string.rstrip(option['key']))
        if key==inkey:
            outval=option['value']
            if len(outval)==0:
                return string.lstrip(string.rstrip(raw_input(option['help'])))
            else:
                return outval
    return ''


  
if __name__ == '__main__':
    #--------------------------------------------------------------------------
    # carreguem les opcions. Es tindra en compte si es passen les opcions com
    # arguments per la linia de comandes
    #
    root = loadOptions()
    print '    '+getOption(root,'SiiOriExe')
    print ' -----------------------------------------------------------------'





