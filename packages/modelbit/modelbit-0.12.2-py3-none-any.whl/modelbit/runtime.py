from typing import Union, List, Dict, Any, Callable, Tuple
import inspect, re, json

from .environment import ALLOWED_PY_VERSIONS, getInstalledPythonVersion, listMissingPackages
from .utils import unindent
from .helpers import DeploymentTestDef, DeploymentTestError, RuntimeFile, RuntimePythonProps, RuntimeType, getJson, getJsonOrPrintError, isAuthenticated, getDefaultPythonVersion, getDefaultPythonPackages, getDefaultSystemPackages
from .ux import COLORS, DifferentPythonVerWarning, GenericError, GenericTip, MismatchedPackageWarning, WarningErrorTip, makeCssStyle, TableHeader, printTemplate, renderTemplate
from .secure_storage import uploadRuntimeObject


class RuntimeStatusNotes:

  def __init__(self, tips: List[WarningErrorTip], warnings: List[WarningErrorTip],
               errors: List[WarningErrorTip]):
    self.tips = tips
    self.warnings = warnings
    self.errors = errors
    self.deployable = len(errors) == 0

  def statusMsg(self):
    if self.deployable:
      return 'Ready'
    return 'Not Ready'

  def statusStyle(self):
    if self.deployable:
      return "color:green; font-weight: bold;"
    return "color:gray; font-weight: bold;"


class NamespaceCollection:

  def __init__(self):
    self.functions: Dict[str, str] = {}
    self.vars: Dict[str, Any] = {}
    self.imports: Dict[str, str] = {}
    self.froms: Dict[str, str] = {"*": "typing"}


class Runtime:
  _runtimeTypeName = "runtime"

  MAX_REQUIREMENTS_TXT = 20_000
  LAMBDA_RAM_MAX_MB = 10_240
  LAMBDA_RAM_MIN_MB = 128

  def __init__(self,
               rtType: RuntimeType,
               name: Union[str, None] = None,
               main_function: Union[Callable[..., Any], None] = None,
               python_version: Union[str, None] = None,
               requirements_txt_filepath: Union[str, None] = None,
               requirements_txt_contents: Union[List[str], None] = None,
               python_packages: Union[List[str], None] = None,
               system_packages: Union[List[str], None] = None,
               docker_run: Union[str, None] = None,
               source_override: Union[str, None] = None):
    self._pythonPackages: Union[List[str], None] = None
    self._systemPackages: Union[List[str], None] = None
    self._dockerRun: Union[str, None] = None
    self._deployName: Union[str, None] = None
    self._deployFunc: Union[Callable[..., Any], None] = None
    self.rtType: RuntimeType = rtType
    self._sourceOverride = source_override
    self._testOutputs: List[Tuple[bool, DeploymentTestDef, Dict[str, str]]] = []

    self._pythonVersion = getDefaultPythonVersion()
    self.set_python_packages(getDefaultPythonPackages())
    self.set_system_packages(getDefaultSystemPackages())

    if name:
      self.set_name(name)
    if main_function:
      self._set_main_function(main_function)
    if python_version:
      self.set_python_version(python_version)
    if requirements_txt_filepath:
      self.set_requirements_txt(filepath=requirements_txt_filepath)
    if requirements_txt_contents:
      self.set_requirements_txt(contents=requirements_txt_contents)
    if python_packages is not None:
      self.set_python_packages(python_packages)
    if system_packages is not None:
      self.set_system_packages(system_packages)
    if docker_run:
      self.set_docker_run(docker_run)
    self._prepEnvironment()

  def _repr_html_(self):
    return self._describeHtml()

  def set_name(self, name: str):
    if not re.match('^[a-zA-Z0-9_]+$', name):
      raise Exception("Names should be alphanumeric with underscores.")
    self._deployName = name
    return self

  def set_python_version(self, version: str):
    if version not in ALLOWED_PY_VERSIONS:
      return self._selfError(f'Python version should be one of {ALLOWED_PY_VERSIONS}.')
    self._pythonVersion = version
    return self

  def set_requirements_txt(self, filepath: Union[str, None] = None, contents: Union[List[str], None] = None):
    # if filepath == None and contents == None:
    # return self._filepicker_requirements_txt()
    lines: List[str] = []
    if filepath != None and type(filepath) == str:
      f = open(filepath, "r")
      lines = [n.strip() for n in f.readlines()]
      return self.set_python_packages(lines)
    elif contents != None:
      return self.set_python_packages(contents)
    return self

  def set_python_packages(self, packages: Union[List[str], None]):
    if packages is None:
      self._pythonPackages = None
      return
    if type(packages) != list:
      raise Exception("The python_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise Exception("The python_packages parameters must be a list of strings.")
      if "\n" in pkg or "\r" in pkg:
        raise Exception("The python_packages parameters cannot contain newlines")
    self._pythonPackages = packages

  def set_system_packages(self, packages: Union[List[str], None]):
    if packages is None:
      self._systemPackages = None
      return
    if type(packages) != list:
      raise Exception("The system_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise Exception("The system_packages parameters must be a list of strings.")
      if "\n" in pkg or "\r" in pkg:
        raise Exception("The system_packages parameters cannot contain newlines.")
    self._systemPackages = packages

  def set_docker_run(self, commands: Union[str, None]):
    if commands is None:
      self._dockerRun = None
      return
    if type(commands) != str:
      raise Exception("The docker_run parameter must be a string.")
    if "\n" in commands or "\r" in commands:
      raise Exception("The docker_run parameter cannot contain newlines.")
    self._dockerRun = commands

  def _set_main_function(self, func: Callable[..., Any]):
    self._deployFunc = func
    if callable(func) and self._deployName == None:
      self.set_name(func.__name__)
    tests = self._getTests()
    if tests == None:
      self._testOutputs = []
    else:
      self._testOutputs = self._getTestOutputs(tests)
    return self

  def _getRequirementsTxt(self):
    if self._pythonPackages:
      return "\n".join(self._pythonPackages)
    else:
      return None

  def _prepEnvironment(self):
    getJson(
        "jupyter/v1/runtimes/prep_environment", {
            "environment": {
                "requirementsTxt": self._getRequirementsTxt(),
                "pythonVersion": self._pythonVersion,
                "systemPackages": self._systemPackages,
                "dockerRun": self._dockerRun,
            }
        })

  def deploy(self):
    status = self._getStatusNotes()
    rtProps, errors = self._getFuncProps()
    if not status.deployable or len(errors) > 0:
      printTemplate("error", None, errorText="Unable to continue because errors are present.")
      return self

    printTemplate("runtime-deploying",
                  None,
                  deploymentName=self._deployName,
                  warningsList=status.warnings,
                  tipsList=status.tips,
                  errorsList=status.errors)

    sourceFile = self._makeSourceFile(rtProps)
    valueFiles = self._makeAndUploadValueFiles(rtProps)
    resp = getJsonOrPrintError(
        "jupyter/v1/runtimes/create", {
            "runtime": {
                "name": self._deployName,
                "type": self.rtType.value,
                "pyState": {
                    "sourceFile": sourceFile.asDict(),
                    "valueFiles": valueFiles,
                    "name": rtProps.name,
                    "module": self._sourceFileName(),
                    "argNames": rtProps.argNames,
                    "argTypes": rtProps.argTypes,
                    "requirementsTxt": self._getRequirementsTxt(),
                    "pythonVersion": self._pythonVersion,
                    "systemPackages": self._systemPackages,
                    "dockerRun": self._dockerRun
                }
            }
        })
    if not isAuthenticated():
      return None
    if not resp:
      printTemplate("error", None, errorText='Error processing request: no response from server.')
    elif resp.error:
      printTemplate("error", None, errorText=f'Error processing request: {resp.error}')
    elif resp.runtimeOverviewUrl:
      printTemplate("runtime-deployed",
                    None,
                    deploymentName=self._deployName,
                    deployMessage=resp.message,
                    deployTimeWords=self._parseTimeFromDeployMessage(resp.message),
                    runtimeOverviewUrl=resp.runtimeOverviewUrl)
    else:
      printTemplate(
          "error",
          None,
          errorText="Unknown error while processing request (server response in unexpected format).")
    return None

  # a bit of a hack for now
  def _parseTimeFromDeployMessage(self, message: Union[str, None]):
    if not message:
      return None
    if "will be ready in" in message:
      return message.split("will be ready in")[1]
    return None

  def _sourceFileName(self):
    return "source"

  def _makeSourceFile(self, pyProps: RuntimePythonProps):

    def addSpacer(strList: List[str]):
      if len(strList) > 0 and strList[-1] != "":
        strList.append("")

    sourceParts: List[str] = ["import modelbit, sys"]

    if pyProps.namespaceFroms:
      for iAs, iModule in pyProps.namespaceFroms.items():
        sourceParts.append(f"from {iModule} import {iAs}")
    if pyProps.namespaceImports:
      for iAs, iModule in pyProps.namespaceImports.items():
        sourceParts.append(f"import {iModule} as {iAs}")
    addSpacer(sourceParts)

    if pyProps.namespaceVars and pyProps.namespaceVarsDesc:
      for nName, _ in pyProps.namespaceVars.items():
        sourceParts.append(f'{nName} = modelbit.load_value("{nName}") # {pyProps.namespaceVarsDesc[nName]}')

    addSpacer(sourceParts)
    if pyProps.namespaceFunctions:
      for _, fSource in pyProps.namespaceFunctions.items():
        sourceParts.append(fSource)
        addSpacer(sourceParts)

    addSpacer(sourceParts)
    if pyProps.source:
      sourceParts.append("# main function")
      sourceParts.append(pyProps.source)

    sourceParts.append("# to run locally via git & terminal")
    sourceParts.append('if __name__ == "__main__":')
    sourceParts.append(f"  print({pyProps.name}(*sys.argv[1:]))")
    return RuntimeFile(f"{self._sourceFileName()}.py", "\n".join(sourceParts))

  def _makeAndUploadValueFiles(self, pyState: RuntimePythonProps):
    valueFiles: Dict[str, Dict[str, str]] = {}  # is a RuntimeDataMap
    if pyState.namespaceVars and pyState.namespaceVarsDesc:
      for nName, nVal in pyState.namespaceVars.items():
        valueFiles[nName] = {"contentHash": uploadRuntimeObject(nVal, nName)}
    return valueFiles

  def _selfError(self, txt: str):
    printTemplate("error", None, errorText=txt)
    return None

  def _describeHtml(self):
    customStyles = {
        "readyStyle": makeCssStyle({"color": COLORS["success"]}),
        "errorStyle": makeCssStyle({"color": COLORS["error"]}),
        "passStyle": makeCssStyle({
            "color": COLORS["success"],
            "font-weight": "bold"
        }),
        "failStyle": makeCssStyle({
            "color": COLORS["error"],
            "font-weight": "bold"
        }),
    }
    status = self._getStatusNotes()
    funcProps, _ = self._getFuncProps()

    propHeaders = [
        TableHeader("Property", TableHeader.LEFT),
        TableHeader("Value", TableHeader.LEFT, isCode=True),
    ]
    propRows: List[List[str]] = []

    funcSig = '(None)'
    if funcProps.name and funcProps.argNames:
      funcSig = f"{funcProps.name}({', '.join(funcProps.argNames)})"
    propRows.append(["Function", funcSig])

    if funcProps.namespaceFunctions and len(funcProps.namespaceFunctions) > 0:
      nsFuncs = "\n".join([k for k, _ in funcProps.namespaceFunctions.items()])
      propRows.append(["Helpers", nsFuncs])

    if funcProps.namespaceVarsDesc and len(funcProps.namespaceVarsDesc) > 0:
      nsVars = "\n".join([f'{k}: {v}' for k, v in funcProps.namespaceVarsDesc.items()])
      propRows.append(["Values", nsVars])

    nsImports: List[str] = []
    if funcProps.namespaceFroms and len(funcProps.namespaceFroms) > 0:
      for k, v in funcProps.namespaceFroms.items():
        nsImports.append(f'from {v} import {k}')
    if funcProps.namespaceImports and len(funcProps.namespaceImports) > 0:
      for k, v in funcProps.namespaceImports.items():
        nsImports.append(f'import {v} as {k}')
    if len(nsImports) > 0:
      propRows.append(["Imports", '\n'.join(nsImports)])

    propRows.append(["Python Version", self._pythonVersion])

    if self._pythonPackages and len(self._pythonPackages) > 0:
      maxDepsShown = 7
      if len(self._pythonPackages) > maxDepsShown:
        deps = "\n".join([d for d in self._pythonPackages[:maxDepsShown]])
        numLeft = len(self._pythonPackages) - maxDepsShown
        deps += f'\n...and {numLeft} more.'
      else:
        deps = "\n".join([d for d in self._pythonPackages])
      propRows.append(["Python packages", deps])

    if self._systemPackages:
      propRows.append(["System packages", ", ".join(self._systemPackages)])

    if self._dockerRun:
      propRows.append(["Docker RUN", self._dockerRun])

    testHeaders = [
        TableHeader("Status", TableHeader.LEFT, isPassFail=True),
        TableHeader("command", TableHeader.LEFT, isCode=True),
        TableHeader("Result", TableHeader.LEFT, isCode=True),
    ]
    testRows: List[List[Union[str, bool]]] = []
    for tOut in self._testOutputs:
      result: List[str] = []
      metadata = tOut[2]
      if "error" in metadata:
        result.append(f'Error: {metadata["error"]}')
      if "expected" in metadata:
        result.append(f'Expected: {metadata["expected"]}')
      if "received" in metadata:
        result.append(f'Received: {metadata["received"]}')
      testRows.append([tOut[0], tOut[1].command, " ".join(result)])

    return renderTemplate("runtime-description",
                          styles=customStyles,
                          runtimeName=self._deployName,
                          deployable=status.deployable,
                          warningsList=status.warnings,
                          tipsList=status.tips,
                          errorsList=status.errors,
                          properties={
                              "headers": propHeaders,
                              "rows": propRows
                          },
                          tests={
                              "headers": testHeaders,
                              "rows": testRows
                          })

  def _getFuncProps(self):
    errors: List[GenericError] = []
    props: RuntimePythonProps = RuntimePythonProps()
    if not callable(self._deployFunc):
      errors.append(GenericError('The main_function parameter does not appear to be a function.'))
    else:
      props.name = self._deployFunc.__name__
      props.source = self.getFuncSource()
      props.argNames = self.getFuncArgNames()
      props.argTypes = self._annotationsToTypeStr(self._deployFunc.__annotations__)
      nsCollection = NamespaceCollection()
      self._collectNamespaceDeps(self._deployFunc, nsCollection)
      props.namespaceFunctions = nsCollection.functions
      props.namespaceVars = nsCollection.vars
      props.namespaceVarsDesc = self._strValues(nsCollection.vars)
      props.namespaceImports = nsCollection.imports
      props.namespaceFroms = nsCollection.froms
    return (props, errors)

  def getFuncSource(self):
    if self._sourceOverride:
      return self._sourceOverride
    if not callable(self._deployFunc):
      return None
    return unindent(inspect.getsource(self._deployFunc))

  def getFuncArgNames(self):
    argSpec = inspect.getfullargspec(self._deployFunc)
    if argSpec.varargs:
      return ['...']
    if argSpec.args:
      return argSpec.args
    noArgs: List[str] = []
    return noArgs

  def _annotationsToTypeStr(self, annotations: Dict[str, Any]):
    annoStrs: Dict[str, str] = {}
    for name, tClass in annotations.items():
      try:
        if tClass == Any:
          annoStrs[name] = "Any"
        else:
          annoStrs[name] = tClass.__name__
      except:
        pass
    return annoStrs

  def _collectNamespaceDeps(self, func: Callable[..., Any], collection: NamespaceCollection):
    if not callable(func):
      return collection
    globalsDict = func.__globals__  # type: ignore
    allNames = func.__code__.co_names + func.__code__.co_freevars
    for maybeFuncVarName in allNames:
      if maybeFuncVarName in globalsDict:
        maybeFuncVar = globalsDict[maybeFuncVarName]
        if "__module__" in dir(maybeFuncVar):
          if maybeFuncVar.__module__ == "__main__":  # the user's functions
            argNames = list(maybeFuncVar.__code__.co_varnames or [])
            funcSig = f"{maybeFuncVar.__name__}({', '.join(argNames)})"
            if funcSig not in collection.functions:
              collection.functions[funcSig] = inspect.getsource(maybeFuncVar)
              self._collectNamespaceDeps(maybeFuncVar, collection)
          else:  # functions imported by the user from elsewhere
            if inspect.isclass(maybeFuncVar):
              collection.froms[maybeFuncVarName] = maybeFuncVar.__module__
            elif callable(maybeFuncVar) and not self._hasState(maybeFuncVar):
              collection.froms[maybeFuncVarName] = maybeFuncVar.__module__
            elif isinstance(maybeFuncVar, object):
              collection.froms[maybeFuncVar.__class__.__name__] = maybeFuncVar.__module__
              collection.vars[maybeFuncVarName] = maybeFuncVar
            else:
              collection.froms[maybeFuncVarName] = f"NYI: {maybeFuncVar.__module__}"
        elif str(maybeFuncVar).startswith('<module'):
          collection.imports[maybeFuncVarName] = maybeFuncVar.__name__
        else:
          collection.vars[maybeFuncVarName] = maybeFuncVar

  def _hasState(self, obj: Any) -> bool:
    try:
      return len(obj.__dict__) > 0
    except:
      return False

  def _getStatusNotes(self):
    tips: List[WarningErrorTip] = []
    warnings: List[WarningErrorTip] = []
    errors: List[WarningErrorTip] = []

    # Errors
    if not self._deployName:
      errors.append(GenericError("This deployment needs a name."))
    if not self._deployFunc:
      errors.append(GenericError("This deployment needs a deploy_function."))
    else:
      _, propErrors = self._getFuncProps()
      if len(propErrors) > 0:
        errors.extend(errors)
    for tOut in self._testOutputs:
      if tOut[0] == False:  # failed test
        errors.append(GenericError("This deployment has failing tests."))
        break
    if not isAuthenticated():
      errors.append(GenericError("You are not logged in to Modelbit. Please log in, then deploy."))

    # Tips
    if len(self._testOutputs) == 0:
      tips.append(
          GenericTip("Add unit tests to improve this deployment.",
                     "https://doc.modelbit.com/#/deployments/unit-tests"))

    # Warnings
    missingPackages = listMissingPackages(getDefaultPythonPackages())
    if len(missingPackages) > 0:
      for mp in missingPackages:
        desiredPackage, similarPackage = mp
        if similarPackage is not None:
          warnings.append(MismatchedPackageWarning(desiredPackage, similarPackage))

    localPyVersion = getInstalledPythonVersion()
    if self._pythonVersion != localPyVersion:
      warnings.append(DifferentPythonVerWarning(self._pythonVersion, localPyVersion))

    return RuntimeStatusNotes(tips, warnings, errors)

  def _strValues(self, args: Dict[str, Any]):
    newDict: Dict[str, str] = {}
    for k, v in args.items():
      strVal = re.sub(r'\s+', " ", str(v))
      if len(strVal) > 200:
        strVal = strVal[0:200] + "..."
      newDict[k] = strVal
    return newDict

  def _getTests(self):
    if not callable(self._deployFunc):
      return None
    funcName = self._deployFunc.__name__
    funcSource = self.getFuncSource()
    resp = getJsonOrPrintError("jupyter/v1/runtimes/parse_tests", {
        "funcName": funcName,
        "funcSource": funcSource,
    })
    if resp:
      return resp.tests
    return None

  def _runTest(self, test: DeploymentTestDef):
    if not callable(self._deployFunc):
      return False
    if test.args == None:
      return self._deployFunc()
    return self._deployFunc(*test.args)  # type: ignore

  def _getTestOutputs(self,
                      tests: List[DeploymentTestDef]) -> List[Tuple[bool, DeploymentTestDef, Dict[str, str]]]:
    return [self._getTestOutput(t) for t in tests]

  def _getTestOutput(self, test: DeploymentTestDef) -> Tuple[bool, DeploymentTestDef, Dict[str, str]]:

    if test.error:
      errorMessage = "Unable to run test."
      if test.error == DeploymentTestError.UnknownFormat.value:
        errorMessage = "Unknown test format"
      if test.error == DeploymentTestError.ExpectedNotJson.value:
        errorMessage = "Expected value must be JSON serializeable"
      if test.error == DeploymentTestError.CannotParseArgs.value:
        errorMessage = "Unable to parse function arguments."
      return (False, test, {"error": errorMessage})

    result = self._runTest(test)
    try:
      jResult = json.loads(json.dumps(result))  # dump+load helps clean up numbers like 2.00000000001
      if jResult != test.expectedOutput:
        return (False, test, {"expected": json.dumps(test.expectedOutput), "received": json.dumps(jResult)})
    except:
      return (False, test, {"error": "Output must be JSON serializeable.", "received": type(result).__name__})
    return (True, test, {"expected": json.dumps(test.expectedOutput)})


class Deployment(Runtime):
  _runtimeTypeName = "deployment"

  def __init__(self,
               name: Union[str, None] = None,
               deploy_function: Union[Callable[..., Any], None] = None,
               python_version: Union[str, None] = None,
               requirements_txt_filepath: Union[str, None] = None,
               requirements_txt_contents: Union[List[str], None] = None,
               python_packages: Union[List[str], None] = None,
               system_packages: Union[List[str], None] = None,
               docker_run: Union[str, None] = None,
               source_override: Union[str, None] = None):
    Runtime.__init__(self,
                     RuntimeType.Deployment,
                     name=name,
                     main_function=deploy_function,
                     python_version=python_version,
                     requirements_txt_filepath=requirements_txt_filepath,
                     requirements_txt_contents=requirements_txt_contents,
                     python_packages=python_packages,
                     system_packages=system_packages,
                     docker_run=docker_run,
                     source_override=source_override)

  def set_deploy_function(self, func: Callable[..., Any]):
    self._set_main_function(func)
