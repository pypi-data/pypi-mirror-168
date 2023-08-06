from typing import Dict, Union, Any
import random, os, io
from html.parser import HTMLParser

LIST_TITLES_WARNINGS = ("inconsistency", "inconsistencies")
LIST_TITLES_TIPS = ("tip", "tips")
LIST_TITLES_ERRORS = ("error", "errors")

COLORS = {
    "brand": "#714488",
    "success": "green",
    "error": "#E2548A",
}


class WarningErrorTip:

  def __init__(self, kind: str):
    self.kind = kind


class GenericError(WarningErrorTip):

  def __init__(self, errorText: str):
    super().__init__("GenericError")
    self.errorText = errorText


class MismatchedPackageWarning(WarningErrorTip):

  def __init__(self, desiredPackage: str, similarPackage: str):
    super().__init__("MismatchedPackageWarning")
    self.desiredPackage = desiredPackage
    self.similarPackage = similarPackage


class MissingPackageFromImportWarning(WarningErrorTip):

  def __init__(self, importedModule: str, localPackage: str):
    super().__init__("MissingPackageFromImportWarning")
    self.importedModule = importedModule
    self.localPackage = localPackage


class DifferentPythonVerWarning(WarningErrorTip):

  def __init__(self, desiredVersion: str, localVersion: str):
    super().__init__("DifferentPythonVerWarning")
    self.desiredVersion = desiredVersion
    self.localVersion = localVersion


class GenericTip(WarningErrorTip):

  def __init__(self, tipText: str, docUrl: str):
    super().__init__("GenericTip")
    self.tipText = tipText
    self.docUrl = docUrl


class UserImage:

  def __init__(self, imageUrl: Union[str, None], ownerName: Union[str, None]):
    self.imageUrl = imageUrl
    self.ownerName = ownerName
    if self.imageUrl is None:
      self.imageUrl = "https://app.modelbit.com/images/profile-placeholder.png"


class TableHeader:
  LEFT = 'left'
  CENTER = 'center'
  RIGHT = 'right'

  def __init__(self, name: str, alignment: str = LEFT, isCode: bool = False, isPassFail: bool = False):
    self.name = name
    self.style = makeCssStyle({
        "text-align": alignment,
        "padding": "10px",
        "vertical-align": "middle",
        "line-height": 1,
    })
    self.isCode = isCode
    self.isPassFail = isPassFail
    if alignment not in [self.LEFT, self.CENTER, self.RIGHT]:
      raise Exception(f'Unrecognized alignment: {alignment}')


# From https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):

  def __init__(self):
    super().__init__()
    self.reset()
    self.strict = False
    self.convert_charrefs = True
    self.text = io.StringIO()

  def handle_data(self, data: str):
    self.text.write(data)

  def get_data(self):
    return self.text.getvalue()


def _strip_tags(html: str):
  s = MLStripper()
  s.feed(html)
  return s.get_data()


def _baseElementStyles():
  headerCss: Dict[str, str | int] = {
      "font-weight": "bold",
      "color": COLORS["brand"],
  }
  headerSuccess = headerCss.copy()
  headerSuccess.update({"color": COLORS["success"]})
  headerError = headerCss.copy()
  headerError.update({"color": COLORS["error"]})

  return {
      "base":
          makeCssStyle({}),
      "bottomSpacing":
          makeCssStyle({"margin": "0 0 20px 0"}),
      "container":
          makeCssStyle({"padding": "5px"}),
      "borderedGroup":
          makeCssStyle({
              "padding": "5px",
              "border-left": f"1px solid {COLORS['brand']}",
              "margin-bottom": "10px",
          }),
      "header":
          makeCssStyle(headerCss),
      "headerSuccess":
          makeCssStyle(headerSuccess),
      "headerError":
          makeCssStyle(headerError),
      "errorLabel":
          makeCssStyle({
              "color": COLORS["error"],
              "font-weight": "bold"
          }),
      "link":
          makeCssStyle({
              "color": "#106ba3",
              "text-decoration": "none",
              "cursor": "pointer"
          }),
      "ul":
          makeCssStyle({
              "background-color": "red",
              "padding": "10px",
          }),
      "li":
          makeCssStyle({
              "margin": "0 0 0 10px",
              "list-style": "circle",
          }),
      "code":
          makeCssStyle({
              "font-family": "monospace",
              "color": COLORS["brand"],
              "font-size": "13px",
              "font-weight": "400",
              "background-color": "#f3f4f6",
              "padding": "3px"
          }),
      "codeInTable":
          makeCssStyle({
              "font-family": "monospace",
              "color": COLORS["brand"],
              "font-size": "13px",
              "font-weight": "400",
              "white-space": "pre-wrap",
          }),
      "userImage":
          makeCssStyle({
              "display": "inline-block",
              "border-radius": "9999px",
              "width": "2rem",
              "height": "2rem",
              "background-color": "rgb(229 231 235)"
          })
  }


def makeCssStyle(styles: Dict[str, Union[str, int]]):
  baseStyles = {
      "margin": 0,
      "padding": 0,
      "line-height": 1.75,
      "font-size": "14px",
      "vertical-align": "baseline",
      "list-style": "none",
      "font-family": "Roboto, Arial, sans-serif",
      "background": "none",
  }
  baseStyles.update(styles)
  return "; ".join([f"{s[0]}: {s[1]}" for s in baseStyles.items()]) + ";"


def renderTemplate(templateName: str, styles: Dict[str, str] = {}, **kwargs: Any):
  stylesWithBase = _baseElementStyles()
  stylesWithBase.update(styles)
  from jinja2 import Environment, FileSystemLoader, select_autoescape
  _jinjaTemplates = Environment(loader=FileSystemLoader(
      os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')),
                                autoescape=select_autoescape(['html.j2']))
  renderId = f"mb-{random.randint(1, 999999999)}"
  return _jinjaTemplates.get_template(f"{templateName}.html.j2").render(styles=stylesWithBase,
                                                                        renderId=renderId,
                                                                        **kwargs)


def printTemplate(templateName: str, displayId: Union[str, None], styles: Dict[str, str] = {}, **kwargs: Any):
  # TODO: have separate templates for html and txt mode
  txtMode = os.getenv('MB_TXT_MODE')
  try:
    from IPython import display
  except:
    txtMode = "1"

  html = renderTemplate(templateName, styles=styles, **kwargs)
  dispText = _strip_tags(html.replace("<br/>", "\n"))

  if txtMode:
    print(dispText)
  else:
    # Note: Jupyter display clearing doesn't work in hex (or future txt mode), so don't rely on it
    display.display(display.HTML(html), display_id=displayId, clear=bool(displayId))  # type: ignore
