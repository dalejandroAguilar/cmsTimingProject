###################################################################################################         
#    Daniel Aguilar                                                                               #
#    dalejandro_acdc@yahoo.com                                                                    #
#    9 de Junio de 2018                                                                           #
#    This script shows the module with the largest time of each path                              #
#    Ex: python hlt_Max.py file1DQM.root file2DQM.root 305636 305670                              #
###################################################################################################
import os,sys
import subprocess
import string, re
import fileinput
import commands
import operator
from time import gmtime, localtime, strftime
#README Change the path to your root directory
sys.path.append(r'C:\root_v5.34.34\bin') 
from ROOT import gPad, gROOT, TCanvas, TH1F, TFile, TLegend, gStyle,gDirectory
import io

#just a debug flag
DEBUG = False

class Triplet:
    def __init__(self, path, process, time):
        self.path=path
        self.process=process
        self.time=time

def usage():
    if (DEBUG):
        print "This is the usage function"       
    print '\n'
    print 'Usage: '+sys.argv[0]+' <file> <run>'
    print 'e.g.:  '+sys.argv[0]+' \n'

def getMax(file,run):
    pathList = []
    process = "TIMING"
    tfile = TFile(file)
    dirname = "DQMData/Run %s/HLT/Run summary/TimerService/process %s paths" % (run, process)
    gDirectory.cd(dirname)
    #f = io.open('asno3.txt','w',encoding='utf8')
    for everyPath in gDirectory.GetListOfKeys():
        if everyPath.GetName().startswith("path "):
            hist=tfile.Get(dirname+"/"+everyPath.GetName()+"/module_time_real_total")
            nbins=hist.GetNbinsX()
            maxBin=0
            maxTime=0
            for everyIndexProcces in range(0,nbins+1):
                if hist.GetBinContent(everyIndexProcces) > maxTime:
                    maxBin=everyIndexProcces
                    maxTime=hist.GetBinContent(maxBin)
            pathList.append(Triplet(everyPath.GetName(),hist.GetXaxis().GetBinLabel(maxBin),hist.GetBinContent(maxBin)))
            #f.write(unicode(everyPath.GetName())+' '+unicode(hist.GetXaxis().GetBinLabel(maxBin))+' '+unicode(hist.GetBinContent(maxBin))+'\n')
    return pathList

def wirte_csv(pathList,file):
    f = io.open(unicode("MaxTimeValueFromEachPath_"+file.split('_')[1].strip(".csv")+".csv"),'w',encoding='utf8')
    f.write(unicode("Path name,Slowest Process Name,Time/[ms]"+"\n"))
    for eachPathTriplet in pathList:
        f.write(unicode(eachPathTriplet.path+","+eachPathTriplet.process+","))
        f.write(unicode(eachPathTriplet.time))
        f.write(unicode("\n"))

def main():
    #check the number of parameter
    if len(sys.argv) < 3:
        usage()
        return 1
    infile = sys.argv[1]
    run = sys.argv[2]
    #check if input files exist
    if  not(os.path.isfile(infile)):
        print infile+" does not exist. Please check."
        sys.exit(1)
    #getMax and print in a csv file
    wirte_csv(getMax(infile,run),infile)

if __name__ =='__main__':
    sys.exit(main())