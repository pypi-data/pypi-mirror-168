from time import sleep
from typing import Union, Any, List, Dict, cast
from enum import Enum
import json, requests, os, uuid
from .utils import deprecated_pickleObj, sizeOfFmt, getEnvOrDefault, deprecated_unpickleObj
from .environment import getInstalledPythonVersion, ALLOWED_PY_VERSIONS, listMissingPackages
from .ux import COLORS, DifferentPythonVerWarning, MismatchedPackageWarning, WarningErrorTip, makeCssStyle, printTemplate
from threading import Thread

pkgVersion: str = ""  # set in __init__
_MAX_DATA_LEN = 50_000_000
_DEFAULT_CLUSTER = "app.modelbit.com"

_cluster = ""
_region = ""
_api_host = ""
_login_host = ""
_api_url = ""
_currentBranch = "main"


def _setUrls(cluster: Union[str, None]):
  global _cluster, _region, _api_host, _login_host, _api_url
  if cluster is None:
    return
  _cluster = cluster
  _region = _cluster.split(".")[0]
  if cluster == "localhost":
    _api_host = f'http://web:3000/'
    _login_host = f'http://localhost:3000/'
  else:
    _api_host = f'https://{_cluster}/'
    _login_host = _api_host
  _api_url = f'{_api_host}api/'


class OwnerInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: Union[str, None] = data.get("id", None)
    self.name: Union[str, None] = data.get("name", None)
    self.imageUrl: Union[str, None] = data.get("imageUrl", None)


class DatasetDesc:

  def __init__(self, data: Dict[str, Any]):
    self.name: str = data["name"]
    self.sqlModifiedAtMs: Union[int, None] = data.get("sqlModifiedAtMs", None)
    self.query: str = data["query"]
    self.recentResultMs: Union[int, None] = data.get("recentResultMs", None)
    self.numRows: Union[int, None] = data.get("numRows", None)
    self.numBytes: Union[int, None] = data.get("numBytes", None)
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class ResultDownloadInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]


class ObjectUploadInfo:

  def __init__(self, data: Dict[str, Any]):
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]
    self.objectExists: bool = data["objectExists"]


class WhType(Enum):
  Snowflake = 'Snowflake'
  Redshift = 'Redshift'


class GenericWarehouse:

  def __init__(self, data: Dict[str, Any]):
    self.type: WhType = data["type"]
    self.id: str = data["id"]
    self.displayName: str = data["displayName"]
    self.deployStatusPretty: str = data["deployStatusPretty"]
    self.createdAtMs: int = data["createdAtMs"]


class RuntimeFile:

  def __init__(self, name: str, contents: str):
    self.name = name
    self.contents = contents

  def asDict(self):
    return {"name": self.name, "contents": self.contents}


class RuntimePythonProps:
  excludeFromDict: List[str] = ['errors']

  def __init__(self):
    self.source: Union[str, None] = None
    self.name: Union[str, None] = None
    self.argNames: Union[List[str], None] = None
    self.argTypes: Union[Dict[str, str], None] = None
    self.namespaceVarsDesc: Union[Dict[str, str], None] = None
    self.namespaceFunctions: Union[Dict[str, str], None] = None
    self.namespaceImports: Union[Dict[str, str], None] = None
    self.namespaceFroms: Union[Dict[str, str], None] = None
    self.errors: Union[List[str], None] = None
    self.namespaceVars: Union[Dict[str, Any], None] = None


class RuntimeType(Enum):
  Deployment = 'Deployment'


class RuntimeInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.name: str = data["name"]
    self.version: str = data["version"]
    self.deployedAtMs: int = data["deployedAtMs"]
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class PickledObj:

  def __init__(self, obj: Any = None, jDict: Union[Dict[str, Any], None] = None):
    self.pkl: Union[str, None] = None
    self.desc: Union[str, None] = None
    self.kind: Union[str, None] = None
    self.size: Union[int, None] = None
    if obj:
      self.pkl = deprecated_pickleObj(obj)
      self.desc = str(obj)
      self.kind = self._getClassName(obj)
      self.size = len(self.pkl)
    elif jDict:
      self.pkl = jDict.get("pkl", None)
      self.desc = jDict.get("desc", None)
      self.kind = jDict.get("kind", None)
      self.size = jDict.get("size", None)

  def unpickle(self):
    if self.pkl:
      return deprecated_unpickleObj(self.pkl)
    else:
      return None

  def asDict(self):
    return self.__dict__

  def _getClassName(self, obj: Any):
    try:
      return f"{obj.__module__}.{obj.__class__.__name__}"
    except:
      return ""


class ModelPackage:

  def __init__(self, data: Dict[str, Any]):
    self.uuid: str = data.get("uuid", str(uuid.uuid4()))
    self.name: Union[str, None] = data.get("name", None)
    self.ownerInfo: Union[OwnerInfo, None] = None
    if "ownerInfo" in data:
      self.ownerInfo = OwnerInfo(data["ownerInfo"])
    self.model: Union[PickledObj, None] = None
    if "model" in data:
      self.model = PickledObj(jDict=data["model"])
    self.helpers: Dict[str, PickledObj] = {}
    if "helpers" in data:
      helpers = cast(Dict[str, Any], data["helpers"])
      for hName, hVal in helpers.items():
        self.helpers[hName] = PickledObj(jDict=hVal)
    self.properties: Dict[str, Any] = data.get("properties", {})
    self.requirementsTxt: Union[str, None] = data.get("requirementsTxt", None)
    self.pythonVersion: Union[str, None] = data.get("pythonVersion", None)
    self.createdAtMs: Union[int, None] = data.get("createdAtMs", None)

  def asDict(self):
    d = self.__dict__.copy()
    if self.model:
      d["model"] = self.model.asDict()
    d["helpers"] = {}
    for hName, hPkl in self.helpers.items():
      d["helpers"][hName] = hPkl.asDict()
    del d["ownerInfo"]
    return d


class RuntimeEnvironment:

  def __init__(self, data: Dict[str, Any]):
    self.pythonVersion: str = data.get("pythonVersion", None)
    self.pythonPackages: Union[List[str], None] = data.get("pythonPackages", None)
    self.systemPackages: Union[List[str], None] = data.get("systemPackages", None)


class DeploymentTestError(Enum):
  UnknownFormat = 'UnknownFormat'
  ExpectedNotJson = 'ExpectedNotJson'
  CannotParseArgs = 'CannotParseArgs'


class DeploymentTestDef:

  def __init__(self, data: Dict[str, Any]):
    self.command: str = data.get("command", "")
    self.expectedOutput: Union[str, Dict[Union[str, int, float, bool], Any]] = data.get("expectedOutput", "")
    self.args: Union[List[Any], None] = data.get("args", None)
    self.error: Union[str, None] = data.get("error", None)


class NotebookEnv:

  def __init__(self, data: Dict[str, Any]):
    self.userEmail: Union[str, None] = data.get("userEmail", None)
    self.signedToken: Union[str, None] = data.get("signedToken")
    self.authenticated: bool = data.get("authenticated", False)
    self.workspaceName: Union[str, None] = data.get("workspaceName", None)
    self.mostRecentVersion: Union[str, None] = data.get("mostRecentVersion", None)
    self.cluster: Union[str, None] = data.get("cluster", None)
    self.defaultEnvironment: Union[RuntimeEnvironment, None] = None
    if "defaultEnvironment" in data and data["defaultEnvironment"] is not None:
      self.defaultEnvironment = RuntimeEnvironment(data["defaultEnvironment"])


class NotebookResponse:

  def __init__(self, data: Dict[str, Any]):
    self.error: Union[str, None] = data.get("error", None)
    self.message: Union[str, None] = data.get("message", None)

    self.notebookEnv: Union[NotebookEnv, None] = None
    if "notebookEnv" in data:
      self.notebookEnv = NotebookEnv(data["notebookEnv"])

    self.datasets: Union[List[DatasetDesc], None] = None
    if "datasets" in data:
      self.datasets = [DatasetDesc(d) for d in data["datasets"]]

    self.dsrDownloadInfo: Union[ResultDownloadInfo, None] = None
    if "dsrDownloadInfo" in data:
      self.dsrDownloadInfo = ResultDownloadInfo(data["dsrDownloadInfo"])

    self.warehouses: Union[List[GenericWarehouse], None] = None
    if "warehouses" in data:
      self.warehouses = [GenericWarehouse(w) for w in data["warehouses"]]

    self.runtimeOverviewUrl: Union[str, None] = None
    if "runtimeOverviewUrl" in data:
      self.runtimeOverviewUrl = data["runtimeOverviewUrl"]

    self.deployments: Union[List[RuntimeInfo], None] = None
    if "deployments" in data:
      self.deployments = [RuntimeInfo(d) for d in data["deployments"]]

    self.modelOverviewUrl: Union[str, None] = None
    if "modelOverviewUrl" in data:
      self.modelOverviewUrl = data["modelOverviewUrl"]

    self.models: Union[List[ModelPackage], None] = None
    if "models" in data:
      self.models = [ModelPackage(m) for m in data["models"]]

    self.modelDownloadInfo: Union[ResultDownloadInfo, None] = None
    if "modelDownloadInfo" in data:
      self.modelDownloadInfo = ResultDownloadInfo(data["modelDownloadInfo"])

    self.tests: Union[List[DeploymentTestDef], None] = None
    if "tests" in data:
      self.tests = [DeploymentTestDef(d) for d in data["tests"]]

    self.objectUploadInfo: Union[ObjectUploadInfo, None] = None
    if "objectUploadInfo" in data:
      self.objectUploadInfo = ObjectUploadInfo(data["objectUploadInfo"])


def getJson(path: str, body: Dict[str, Any] = {}) -> NotebookResponse:
  global _state
  requestToken = _state.signedToken
  if requestToken == None:
    requestToken = os.getenv('MB_RUNTIME_TOKEN')
  data: Dict[str, Any] = {"requestToken": requestToken, "version": pkgVersion, "branch": _currentBranch}
  data.update(body)
  dataLen = len(json.dumps(data))
  if (dataLen > _MAX_DATA_LEN):
    return NotebookResponse({
        "error":
            f'API Error: Request is too large. (Request is {sizeOfFmt(dataLen)} Limit is {sizeOfFmt(_MAX_DATA_LEN)})'
    })
  with requests.post(f'{_api_url}{path}', json=data) as url:  # type: ignore
    nbResp = NotebookResponse(url.json())  # type: ignore
    if nbResp.notebookEnv:
      _state = nbResp.notebookEnv
    return nbResp


def getJsonOrPrintError(path: str, body: Dict[str, Any] = {}):
  nbResp = getJson(path, body)
  if not isAuthenticated():
    performLogin()
    return False
  if nbResp.error:
    printTemplate("error", None, errorText=nbResp.error)
    return False
  return nbResp


def refreshAuthentication() -> bool:
  global _state
  nbResp = getJson("jupyter/v1/login")
  if nbResp.error:
    printTemplate("error", None, errorText=nbResp.error)
    return False
  if nbResp.notebookEnv:
    _state = nbResp.notebookEnv
    _setUrls(_state.cluster)
  return isAuthenticated()


def isAuthenticated() -> bool:
  return _state.authenticated


def performLogin(refreshAuth: bool = False, region: Union[str, None] = None):
  if region is not None:
    _setUrls(f"{region}.modelbit.com")
  if (refreshAuth):
    refreshAuthentication()
  if isAuthenticated():
    printAuthenticatedMessage()
    return
  displayId = "mbLogin"
  printLoginMessage(displayId)

  def pollForLoggedIn():
    triesLeft = 150
    while not isAuthenticated() and triesLeft > 0:
      triesLeft -= 1
      sleep(3)
      refreshAuthentication()
    if isAuthenticated():
      printAuthenticatedMessage(displayId)
    else:
      printTemplate("login-timeout", displayId=displayId)

  loginThread = Thread(target=pollForLoggedIn)
  if os.getenv('MODELBIT_CI') != "1":
    loginThread.start()


def _pipUpgradeInfo():
  if os.getenv('MB_RUNTIME_TOKEN'):
    return None  # runtime environments don't get upgraded
  latestVer = _state.mostRecentVersion

  def ver2ints(ver: str):
    return [int(v) for v in ver.split(".")]

  nbVer = pkgVersion
  if latestVer and ver2ints(latestVer) > ver2ints(nbVer):
    return {"installed": nbVer, "latest": latestVer}
  return None


def _environmentConflicts():
  warnings: List[WarningErrorTip] = []

  de = _state.defaultEnvironment
  if de is None:
    return warnings

  installedPythonVer = getInstalledPythonVersion()
  if getInstalledPythonVersion() != de.pythonVersion:
    warnings.append(DifferentPythonVerWarning(de.pythonVersion, installedPythonVer))

  missingPackages = listMissingPackages(de.pythonPackages)
  if len(missingPackages) > 0:
    for mp in missingPackages:
      desiredPackage, similarPackage = mp
      if similarPackage is not None:
        warnings.append(MismatchedPackageWarning(desiredPackage, similarPackage))

  return warnings


def printAuthenticatedMessage(displayId: Union[str, None] = None):
  inRegion: Union[str, None] = None
  if _cluster != _DEFAULT_CLUSTER:
    inRegion = _region
  styles = {
      "connected": makeCssStyle({
          "color": COLORS["success"],
          "font-weight": "bold",
      }),
      "info": makeCssStyle({
          "font-family": "monospace",
          "font-weight": "bold",
          "color": COLORS["brand"],
      })
  }
  printTemplate("authenticated",
                displayId,
                styles=styles,
                email=_state.userEmail,
                workspace=_state.workspaceName,
                inRegion=inRegion,
                needsUpgrade=_pipUpgradeInfo(),
                warningsList=_environmentConflicts())


def printLoginMessage(displayId: Union[str, None] = None):
  if (_state.signedToken == None or type(_state.signedToken) != str):
    raise Exception("Signed token missing, cannot authenticate.")
  displayUrl = f'modelbit.com/t/{_state.signedToken[0:10]}...'
  linkUrl = f'{_login_host}/t/{_state.signedToken}'
  printTemplate("login",
                displayId=displayId,
                displayUrl=displayUrl,
                linkUrl=linkUrl,
                needsUpgrade=_pipUpgradeInfo())


def _runtimeToken():  # type: ignore
  return _state.signedToken


def setCurrentBranch(branch: str):
  global _currentBranch
  if type(branch) != str:
    raise Exception("Branch must be a string.")
  _currentBranch = branch


def getCurrentBranch():
  return _currentBranch


def getDefaultPythonVersion():
  if _state.defaultEnvironment is None:
    installedVersion = getInstalledPythonVersion()
    if installedVersion in ALLOWED_PY_VERSIONS:
      return installedVersion
    return "3.8"
  else:
    return _state.defaultEnvironment.pythonVersion


def getDefaultPythonPackages() -> Union[List[str], None]:
  if _state.defaultEnvironment is None:
    return []
  return _state.defaultEnvironment.pythonPackages


def getDefaultSystemPackages() -> Union[List[str], None]:
  if _state.defaultEnvironment is None:
    return []
  return _state.defaultEnvironment.systemPackages


# set defaults
_setUrls(getEnvOrDefault("MB_JUPYTER_CLUSTER", _DEFAULT_CLUSTER))
_state = NotebookEnv({})
