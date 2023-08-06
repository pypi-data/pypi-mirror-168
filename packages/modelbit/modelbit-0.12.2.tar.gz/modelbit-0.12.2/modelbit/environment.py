from typing import List, Union, Tuple
import os, sys, re

ALLOWED_PY_VERSIONS = ['3.6', '3.7', '3.8', '3.9', '3.10']


def _listInstalledPackages():
  pkgList: List[str] = []
  pkgLines = os.popen("pip list --disable-pip-version-check").read().strip().split("\n")
  for pkgLine in pkgLines:
    parts = re.split(r'\s+', pkgLine)
    pkgList.append("==".join(parts).lower())
  return pkgList


# Returns List[(desiredPackage, installedPackage|None)]
def listMissingPackages(
    deploymentPythonPackages: Union[List[str], None]) -> List[Tuple[str, Union[str, None]]]:
  missingPackages: List[Tuple[str, Union[str, None]]] = []

  if deploymentPythonPackages is None or len(deploymentPythonPackages) == 0:
    return missingPackages

  installedPackages = _listInstalledPackages()
  for dpp in deploymentPythonPackages:
    if dpp not in installedPackages:
      similarPackage: Union[str, None] = None
      dppNoVersion = dpp.split("=")[0].lower()
      for ip in installedPackages:
        if ip.startswith(dppNoVersion):
          similarPackage = ip
      missingPackages.append((dpp, similarPackage))

  return missingPackages


def getInstalledPythonVersion():
  installedVer = f"{sys.version_info.major}.{sys.version_info.minor}"
  return installedVer
