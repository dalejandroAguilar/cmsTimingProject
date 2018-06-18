###################################################################################################         
#    Daniel Aguilar                                                                               #
#    dalejandro_acdc@yahoo.com                                                                    #
#    June 16, 2018                                                                                #
#    This script shows a file with a log of results if you remove paths wich begin with ...       #
#    or a list of paths in a specified paths                                                      #
#    Ex1: python hlt_ExtractPaths.py fileDQM.root startsWith DST                                  #
#    Ex2: python hlt_ExtractPaths.py fileDQM.root pathListFile file.txt                           #
###################################################################################################

import os,sys
import subprocess
import string, re
import fileinput
import commands
import operator
from time import gmtime, localtime, strftime
#README Change the path to your root directory
#sys.path.append(r'C:\root_v5.34.34\bin') 
from ROOT import gPad, gROOT, TCanvas, TH1F, TFile, TLegend, gStyle,gDirectory
import io

#just a debug flag
DEBUG = False

#options

def usage():
    if (DEBUG):
        print "This is the usage function"       
    print '\n'
    print 'Usage: '+sys.argv[0]+' <file> <run> <optionMode [startsWith/pathListFile]> <argument [string/fileName]>'
    print 'e.g.:  '+sys.argv[0]+' \n'

def func(file,run,mode,argument):
    wholeDict = {}
    process = "TIMING"
    tfile = TFile(file)
    dirname = "DQMData/Run %s/HLT/Run summary/TimerService/" % (run)
    gDirectory.cd(dirname)
    dirnameModule = "process %s modules" % (process)
    gDirectory.cd(dirnameModule)
    
    totalSum=0
    for everyKey in gDirectory.GetListOfKeys():
        keyName=everyKey.GetName()
        if (keyName[0].islower() and keyName.endswith("time_real")):
            hist = tfile.Get(dirname+dirnameModule+"/"+keyName)
            totalSum=totalSum+hist.GetMean()
            keyName=keyName.split()[0]
            wholeDict.update({keyName.split()[0]:hist.GetMean()})

    dirnamePath = "process %s paths" % (process)
    gDirectory.cd("../")
    gDirectory.cd(dirnamePath)

    cuontTotalPaths=0
    countIncludedPaths=0
    excludedDict=wholeDict.copy()
    for everyPath in gDirectory.GetListOfKeys():
        everyPathName= everyPath.GetName()
        if everyPathName.startswith("path ") or everyPathName.startswith("endpath ") :
            cuontTotalPaths+=1
            if not strainer(everyPath,mode,argument):
                countIncludedPaths+=1
                hist=tfile.Get(dirname+dirnamePath+"/"+everyPathName+"/module_time_real_total")
                nbins=hist.GetNbinsX()
                for moduleIndex in range(1,nbins+1):
                    labelModule=hist.GetXaxis().GetBinLabel(moduleIndex)
                    if excludedDict.has_key(labelModule):
                        del excludedDict[labelModule]
    #print sumatory of mean times
    excludeSum=0
    for everyKey in excludedDict:
        excludeSum+=excludedDict[everyKey]

    f = io.open(unicode("ExtractPaths"+file.split('_')[1].strip(".csv")+".csv"),'w',encoding='utf8')

    f.write(unicode("Actual Mean Event Real Time:, %f\n" % (tfile.Get(dirname+"event time_real").GetMean())))
    f.write(unicode("Total Paths:, %i\n"% (cuontTotalPaths)))
    f.write(unicode("Total Modules:, %i\n"% (len(wholeDict))))
    f.write(unicode("Total Mean Modules Sum:, %f\n"% (totalSum)))
    f.write(unicode("Excluded Paths:, %i\n"% (cuontTotalPaths-countIncludedPaths)))
    f.write(unicode("Excluded Modules:, %i\n"% (len(excludedDict))))
    f.write(unicode("Excluded Mean Modules Sum:, %f\n"% (excludeSum)))
    f.write(unicode("Net Paths:, %i\n"% (countIncludedPaths)))
    f.write(unicode("Net Modules:, %i\n"% (len(wholeDict)-len(excludedDict))))
    f.write(unicode("Net Mean Modules Sum:, %f\n"% (totalSum-excludeSum)))

def strainer(path,mode,argument):
    if (mode=="startsWith"):
        return path.GetName().startswith("path "+argument)
    if (mode=="pathListFile"):
        with open(argument) as f:
            lines= f.readlines() 
        for everyline in lines:
            if path.GetName().startswith("path "+everyline.rstrip('\n')):
                return True
    return False

def main():
    #check the number of parameter
    if len(sys.argv) < 5:
        usage()
        return 1
    infile = sys.argv[1]
    run = sys.argv[2]
    option = sys.argv[3]
    argument = sys.argv[4]

    #check if input files exist
    if  not(os.path.isfile(infile)):
        print infile+" does not exist. Please check."
        sys.exit(1)

    if option=="pathListFile":
        if  not(os.path.isfile(argument)):
            print argument+" does not exist. Please check."
            sys.exit(1)

    if not (option=="startsWith" or option =="pathListFile"):
        print "Only these arguments are valid: "+"startsWith"+","+"pathListFile"

    func(infile,run,option,argument)

if __name__ =='__main__':
    sys.exit(main())