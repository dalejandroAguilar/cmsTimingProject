###################################################################################################         
#    Daniel Aguilar                                                                               #
#    dalejandro_acdc@yahoo.com                                                                    #
#    June 16, 2018                                                                                #
#    This script shows a file with a sorted  list of the paths with most contribution of time     #
#    in a interval specified                                                                      #
#    Ex: python hlt_MostContributingPaths.py fileDQM.root 305670 lowerLimit upperLimit            #
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

class Duplet:
    def __init__(self, path, weight):
        self.path=path
        self.weight=weight

def usage():
    if (DEBUG):
        print "This is the usage function"       
    print '\n'
    print 'Usage: '+sys.argv[0]+' <file> <run> <lowerLimit> <upperLimit>'
    print 'e.g.:  '+sys.argv[0]+' \n'

def getPathOrderByIntegral(file,run,lowerLimit,upperLimit):
    pathList = []
    process = "TIMING"
    tfile = TFile(file)
    dirname = "DQMData/Run %s/HLT/Run summary/TimerService/process %s paths" % (run, process)
    gDirectory.cd(dirname)

    for everyPath in gDirectory.GetListOfKeys():
        if everyPath.GetName().startswith("path "):
            hist=tfile.Get(dirname+"/"+everyPath.GetName()+"/path time_real")
            pathList.append(Duplet(everyPath.GetName(),hist.Integral(lowerLimit/5,upperLimit/5)))

    pathList=sorted(pathList,key=lambda duplet: duplet.weight, reverse=True)

    return pathList

def wirte_csv(pathList,file,lowerLimit,upperLimit):
    f = io.open(unicode("MostContributingPaths_"+file.split('_')[1].strip(".csv"))+unicode("from")+unicode(lowerLimit+"to"+upperLimit+".csv"),'w',encoding='utf8')
    f.write(unicode("Path name,Weight"+"\n"))
    for eachPathDuplet in pathList:
        f.write(unicode(eachPathDuplet.path+","))
        f.write(unicode(eachPathDuplet.weight))
        f.write(unicode("\n"))

def main():
    #check the number of parameter
    if len(sys.argv) < 5:
        usage()
        return 1
    infile = sys.argv[1]
    run = sys.argv[2]
    lowerLimit = sys.argv[3]
    upperLimit = sys.argv[4]

    #check if input files exist
    if  not(os.path.isfile(infile)):
        print infile+" does not exist. Please check."
        sys.exit(1)

    intLowerLimit =int(lowerLimit)
    intUpperLimit =int(upperLimit)

    #check the ranges of the limits
    if not(intLowerLimit>=0 and intUpperLimit<=1000 and intLowerLimit<=intUpperLimit):
        print " Out of range limits. Please check."
        sys.exit(1)

    #check the value of the limits
    if not(intLowerLimit%5==0 and intUpperLimit%5==0):
        print " The limits must be a multiple of 5."
        sys.exit(1)

    #getPathOrderByIntegral and print in a csv file
    wirte_csv(getPathOrderByIntegral(infile,run,intLowerLimit,intUpperLimit),infile,lowerLimit,upperLimit)

if __name__ =='__main__':
    sys.exit(main())