from typing import List, Dict, Union

from .utils import timeago
from .helpers import RuntimeInfo, getJsonOrPrintError, isAuthenticated
from .ux import TableHeader, renderTemplate, UserImage


class DeploymentsList:

  def __init__(self):
    self._deployments: List[RuntimeInfo] = []
    resp = getJsonOrPrintError("jupyter/v1/runtimes/list?runtimeType=Deployment")
    if resp and resp.deployments:
      self._deployments = resp.deployments

  def _repr_html_(self):
    if not isAuthenticated():
      return ""
    return self._makeDeploymentsHtmlTable()

  def _makeDeploymentsHtmlTable(self):
    from collections import defaultdict

    if len(self._deployments) == 0:
      return "There are no deployments to show."
    deploymentsByName: Dict[str, List[RuntimeInfo]] = defaultdict(lambda: [])
    for d in self._deployments:
      deploymentsByName[d.name].append(d)

    headers = [
        TableHeader("Name", TableHeader.LEFT, isCode=True),
        TableHeader("Owner", TableHeader.CENTER),
        TableHeader("Version", TableHeader.RIGHT),
        TableHeader("Deployed", TableHeader.LEFT),
    ]
    rows: List[List[Union[str, UserImage]]] = []
    for dList in deploymentsByName.values():
      ld = dList[0]
      connectedAgo = timeago(ld.deployedAtMs)
      rows.append([ld.name, UserImage(ld.ownerInfo.imageUrl, ld.ownerInfo.name), ld.version, connectedAgo])
    return renderTemplate("table", headers=headers, rows=rows)


def list():
  return DeploymentsList()
