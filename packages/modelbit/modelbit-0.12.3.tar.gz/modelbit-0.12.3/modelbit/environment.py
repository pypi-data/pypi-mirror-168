from typing import List, Union, Tuple, Dict
import os, sys, json

ALLOWED_PY_VERSIONS = ['3.6', '3.7', '3.8', '3.9', '3.10']


def listInstalledPackages():
  return [f'{p["name"]}=={p["version"]}' for p in getPipList()]


# Returns List[(desiredPackage, installedPackage|None)]
def listMissingPackagesFromPipList(
    deploymentPythonPackages: Union[List[str], None]) -> List[Tuple[str, Union[str, None]]]:
  missingPackages: List[Tuple[str, Union[str, None]]] = []

  if deploymentPythonPackages is None or len(deploymentPythonPackages) == 0:
    return missingPackages

  installedPackages = listInstalledPackages()
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


def packagesToIgnoreFromImportCheck(deploymentPythonPackages: Union[List[str], None]) -> List[str]:
  ignorablePackages: List[str] = []
  if deploymentPythonPackages is None:
    return ignorablePackages

  missingPackages = listMissingPackagesFromPipList(deploymentPythonPackages)
  for mp in missingPackages:
    if mp[1] is not None:
      ignorablePackages.append(mp[1].split("=")[0])

  return ignorablePackages


# Returns List[(importedModule, pipPackageInstalled)]
def listMissingPackagesFromImports(importedModules: Union[List[str], None],
                                   deploymentPythonPackages: Union[List[str], None]) -> List[Tuple[str, str]]:
  missingPackages: List[Tuple[str, str]] = []
  ignoreablePackages = packagesToIgnoreFromImportCheck(deploymentPythonPackages)
  if importedModules is None:
    return missingPackages
  if deploymentPythonPackages is None:
    deploymentPythonPackages = []

  installedModules = listInstalledPackagesByModule()
  for im in importedModules:
    baseModule = im.split(".")[0]
    if baseModule not in installedModules:
      continue  # module is likely a system module, e.g. json
    pipInstall = installedModules[baseModule]
    pipPackage = pipInstall.split("=")[0]
    if pipInstall not in deploymentPythonPackages and pipPackage not in ignoreablePackages:
      missingPackages.append((im, pipInstall))

  return missingPackages


def getPipInstallAndModuleFromDistInfo(distInfoPath: str) -> Dict[str, str]:
  try:
    tPath = os.path.join(distInfoPath, "top_level.txt")
    moduleNames: List[str] = []
    if not os.path.exists(tPath):
      return {}
    with open(tPath) as f:
      moduleNames = f.read().strip().split("\n")

    mPath = os.path.join(distInfoPath, "METADATA")
    if not os.path.exists(mPath):
      return {}

    pipName = None
    pipVersion = None
    with open(mPath) as f:
      metadata = f.read().split("\n")
      for mLine in metadata:
        if mLine.startswith("Name: "):
          pipName = mLine.split(":")[1].strip()
        if mLine.startswith("Version: "):
          pipVersion = mLine.split(":")[1].strip()
        if pipName is not None and pipVersion is not None:
          break

    if pipName is None or pipVersion is None:
      return {}

    modulesToPipVersions: Dict[str, str] = {}
    for moduleName in moduleNames:
      modulesToPipVersions[moduleName] = f"{pipName}=={pipVersion}"
    return modulesToPipVersions
  except Exception as err:
    print(f"Warning, unable to check module '{distInfoPath}': {err}")
    return {}


def listInstalledPackagesByModule():
  packages = getPipList()
  installPaths: Dict[str, int] = {}
  for package in packages:
    installPaths[package["location"]] = 1

  modulesToPipVersions: Dict[str, str] = {}
  for installPath in installPaths.keys():
    for fileOrDir in os.listdir(installPath):
      if fileOrDir.endswith("dist-info"):
        dPath = os.path.join(installPath, fileOrDir)
        modulesToPipVersions.update(getPipInstallAndModuleFromDistInfo(dPath))

  return modulesToPipVersions


def getPipList():
  return json.loads(os.popen("pip list -v --format json --disable-pip-version-check").read().strip())
