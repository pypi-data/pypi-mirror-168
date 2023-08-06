from typing import Any, Union, Dict, List
import re, inspect, pkg_resources, sys, json
from .secure_storage import getSecureData
from .utils import timeago, sizeOfFmt
from .helpers import ModelPackage, PickledObj, getJsonOrPrintError, isAuthenticated
from .ux import UserImage, TableHeader, printTemplate, renderTemplate


class Model:

  def __init__(self,
               modelObj: Any = None,
               name: Union[str, None] = None,
               properties: Union[Dict[str, Any], None] = None,
               helpers: Union[Dict[str, Any], None] = None,
               modelPackage: Union[ModelPackage, None] = None):
    if modelPackage:
      self._modelPackage = modelPackage
    else:
      self._modelPackage = ModelPackage({})
      self._modelPackage.requirementsTxt = self._getEnvPackages()
      self._modelPackage.pythonVersion = self._getPythonVersion()
      if modelObj:
        self.set_model(modelObj)
      if name:
        self.set_name(name)
      else:
        self._modelPackage.name = self._inferName()
      if properties:
        self.set_properties(properties)
      if helpers:
        self.set_helpers(helpers)

  def set_model(self, modelObj: Any):
    self._addArtifactId(modelObj)
    self._modelPackage.model = PickledObj(obj=modelObj)

  def get_model(self):
    if self._modelPackage.model:
      return self._modelPackage.model.unpickle()
    return None

  def set_name(self, name: str):
    if type(name) == str and re.fullmatch(r"[a-z0-9/\s_-]+", name):
      self._modelPackage.name = name.strip()
    else:
      raise Exception("Model name should be a string of lowercase letters and numbers and spaces")

  def get_name(self):
    return self._modelPackage.name

  def set_helpers(self, helpers: Dict[str, Any]):
    if type(helpers) != dict:
      raise Exception("Helpers must be a dictionary with string keys.")
    self._modelPackage.helpers = {}
    for k, v in helpers.items():
      self.set_helper(k, v)

  def get_helpers(self):
    helpers: Dict[str, Any] = {}
    for hName, hPkl in self._modelPackage.helpers.items():
      helpers[hName] = hPkl.unpickle()
    return helpers

  def set_helper(self, name: str, value: Any):
    if type(name) != str:
      raise Exception("Helper names must be strings.")
    self._modelPackage.helpers[name] = PickledObj(obj=value)

  def get_helper(self, name: str):
    if name in self._modelPackage.helpers:
      return self._modelPackage.helpers[name].unpickle()
    return None

  def set_properties(self, props: Dict[str, Any]):
    self._modelPackage.properties = {}
    for k, v in props.items():
      if type(k) != str:  # type: ignore
        raise Exception("Property names must be strings.")
      self._modelPackage.properties[k] = v

  def get_properties(self):
    return self._modelPackage.properties

  def set_property(self, name: str, val: Any):
    self._modelPackage.properties[name] = val

  def get_property(self, name: str):
    return self._modelPackage.properties.get(name, None)

  def save(self):
    if self._modelPackage.model == None:
      raise Exception("Unable to save because no model has been supplied.")
    printTemplate("message", None, msgText='Saving model...')
    resp = getJsonOrPrintError("jupyter/v1/models/create", {"modelPackage": self._modelPackage.asDict()})
    if not isAuthenticated():
      return None
    if not resp:
      printTemplate("error", None, errorText="Unable to save model: no response from server.")
    elif resp.error:
      printTemplate("error", None, errorText=f'Unable to save model: {resp.error}')
    elif resp.modelOverviewUrl:
      printTemplate("model-saved",
                    None,
                    modelName=self._modelPackage.name,
                    modelOverviewUrl=resp.modelOverviewUrl)
    else:
      printTemplate("error",
                    None,
                    errorText="Unknown error while saving model (server response in unexpected format).")
    return None

  def _repr_html_(self):
    if not isAuthenticated():
      return ""
    headers = [
        TableHeader("Property", TableHeader.LEFT),
        TableHeader("Value", TableHeader.LEFT, isCode=True),
    ]
    rows: List[List[str]] = []
    ms = self._modelPackage
    rows.append(["Description", ms.model.desc if ms.model and ms.model.desc else ""])
    rows.append(["Module", ms.model.kind if ms.model and ms.model.kind else ""])
    rows.append(["Size", sizeOfFmt(ms.model.size) if ms.model and ms.model.size else ""])

    if ms.properties is not None:
      rows.append(["Properties", json.dumps(ms.properties)])
    else:
      rows.append(["Properties", "None"])

    helpers = "\n".join([f'{k}: {v.desc if v.desc else ""}' for k, v in ms.helpers.items()])
    rows.append(["Helpers", helpers if helpers else "None"])

    modelName = ms.name if ms.name else "<unnamed model>"
    return renderTemplate("model-description", modelName=modelName, headers=headers, rows=rows)

  def _getEnvPackages(self):
    pks = sorted(["%s==%s" % (i.key, i.version) for i in pkg_resources.working_set])  # type: ignore
    return "\n".join(pks)

  def _getPythonVersion(self):
    info = sys.version_info
    return f"{info.major}.{info.minor}"

  def _addArtifactId(self, obj: Any):
    try:
      obj.__setattr__("mb_uuid", self._modelPackage.uuid)
    except:
      pass

  def _inferName(self):
    try:
      codeContexts = [f.code_context for f in inspect.stack()]
      for ccList in codeContexts:
        if not ccList:
          continue
        for cc in ccList:
          captures = re.search(r"\.(save_model|Model)\(([^\s,)]+)", cc)
          if captures:
            return captures.group(2)
    except Exception as _:
      pass
    return "unnamed model"


class ModelsList:

  def __init__(self):
    self._modelPackages: List[ModelPackage] = []
    resp = getJsonOrPrintError("jupyter/v1/models/list")
    if resp and resp.models:
      self._modelPackages = resp.models

  def _repr_html_(self):
    if not isAuthenticated():
      return ""
    if len(self._modelPackages) == 0:
      return "There are no models to show."
    headers = [
        TableHeader("Name", TableHeader.LEFT, isCode=True),
        TableHeader("Owner", TableHeader.CENTER),
        TableHeader("Description", TableHeader.LEFT, isCode=True),
        TableHeader("Created", TableHeader.RIGHT),
    ]
    rows: List[List[Union[str, UserImage]]] = []
    for m in self._modelPackages:
      if not m.name or not m.model or not m.ownerInfo or not m.createdAtMs:
        continue

      rows.append([
          m.name,
          UserImage(m.ownerInfo.imageUrl, m.ownerInfo.name),
          m.model.desc if m.model.desc else "",
          timeago(m.createdAtMs),
      ])
    return renderTemplate("table", headers=headers, rows=rows)


def list():
  return ModelsList()


def get(name: str):
  resp = getJsonOrPrintError("jupyter/v1/models/get", {"modelName": name})
  if resp and resp.modelDownloadInfo:
    stStream = getSecureData(resp.modelDownloadInfo, name)
    if not stStream:
      raise Exception("Unable to download model data.")
    jData = json.load(stStream)
    return Model(modelPackage=ModelPackage(jData))
