#!/usr/bin/env python

"""
"""

__RCSID__ = "$Id$"

import os
from statistics import mean
from statistics import stdev

from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

@Script()

def main():

  Script.parseCommandLine(ignoreErrors=True)

  #optionList = ['','with-scts-with-moon_']
  optionList = ['']
  particleList = ['gamma', 'proton']
  #particleList = ['gamma']
  #compilerList = ['gcc83_noOpt', 'gcc83_matchcpu']
  compilerList = ['gcc83_matchcpu']
  dirNameList = []
  for option in optionList:
    for particle in particleList:
      for compiler in compilerList:
        for cersiz in ['3', '5']:
          dirName = 'Paranal_%s_North_20_cersiz_%s_%s_%s01' % (particle, cersiz, compiler, option)
          dirNameList.append(dirName)

  for dirName in dirNameList:
    #print(dirName)
    if 'gamma' in dirName and 'with-scts-with-moon' not in dirName and 'cersiz_5' in dirName:
      string = 'S-/g bs 5:'
    if 'gamma' in dirName and 'with-scts-with-moon' not in dirName and 'cersiz_3' in dirName:
      string = 'S-/g bs 3:'
    if 'proton' in dirName and 'with-scts-with-moon' not in dirName and 'cersiz_5' in dirName:
      string = 'S-/p bs 5:'
    if 'proton' in dirName and 'with-scts-with-moon' not in dirName and 'cersiz_3' in dirName:
      string = 'S-/p bs 3:'
    if 'gamma' in dirName and 'with-scts-with-moon' in dirName and 'cersiz_5' in dirName:
      string = 'S+/g bs 5:'
    if 'gamma' in dirName and 'with-scts-with-moon' in dirName and 'cersiz_3' in dirName:
      string = 'S+/g bs 3:'
    if 'proton' in dirName and 'with-scts-with-moon' in dirName and 'cersiz_5' in dirName:
      string = 'S+/p bs 5:'
    if 'proton' in dirName and 'with-scts-with-moon' in dirName and 'cersiz_3' in dirName:
      string = 'S+/p bs 3:'
    wallTimeList = []
    for subdir in os.listdir(dirName):
      for subsubdir in os.listdir(os.path.join(dirName,subdir)):
        fileName = os.path.join(dirName,subdir,subsubdir,'CorsikaSimtel_Log.txt')
        if os.path.exists(fileName):
          file = open(fileName, 'r')
          for line in file:
            if 'Multipipe_corsika finished after' in line:
              wallTime = line.split('Multipipe_corsika finished after ')[1].split(' seconds run-time.')[0]
              #print (wallTime)
              wallTimeList.append(float(wallTime))

    print( "%s  %.2f +- %.2f s" % (string, mean(wallTimeList), stdev(wallTimeList)))

if __name__ == "__main__":
  main()
