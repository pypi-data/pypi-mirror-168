#!/usr/bin/env python

"""
"""

__RCSID__ = "$Id$"

import os

from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

@Script()


def main():

  Script.parseCommandLine(ignoreErrors=True)

  dirNameList = []
  tc = TransformationClient()
  #optionList = ['','with-scts-with-moon_']
  optionList = ['']
  particleList = ['gamma', 'proton']
  compilerList = ['gcc83_noOpt', 'gcc83_matchcpu']
  #compilerList = ['gcc83_noOpt']
  for option in optionList:
    for particle in particleList:
      for compiler in compilerList:
        for cersiz in ['3', '5']:
          transName = 'Prod6_Pipeline_Paranal_%s_North_20_cersiz_%s_%s_%s01' % (particle, cersiz, compiler, option)
          dirName = 'Paranal_%s_North_20_cersiz_%s_%s_%s01' % (particle, cersiz, compiler, option)
          res = tc.getTransformation(transName)
          transID = res['Value']['TransformationID']
          jobGroup='0000' + str(transID)
          dirNameList.append(os.path.join(dirName,jobGroup))
          os.system('dirac-wms-job-get-output -g %s -D %s' % (jobGroup, dirName))


if __name__ == "__main__":
  main()
