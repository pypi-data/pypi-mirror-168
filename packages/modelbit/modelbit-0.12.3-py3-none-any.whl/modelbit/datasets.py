from typing import Union, Any, List, cast, Dict
import pandas, os, base64, io, gzip
from urllib.parse import quote_plus
from Cryptodome.Util.Padding import unpad
from Cryptodome.Cipher import AES
from .utils import sizeOfFmt, timeago, timestamp
from .helpers import DatasetDesc, getJsonOrPrintError, isAuthenticated, getCurrentBranch
from .secure_storage import getSecureData
from .ux import TableHeader, UserImage, renderTemplate


class TimedDatasetCache:

  def __init__(self, expireSeconds: int):
    self.expireSeconds = expireSeconds
    self.initTime = timestamp()
    self.cache: Dict[str, pandas.DataFrame] = {}

  def _maybeResetCache(self):
    if self.initTime + (self.expireSeconds * 1000) < timestamp():
      self.cache = {}
      self.initTime = timestamp()

  def set(self, key: str, val: pandas.DataFrame):
    self._maybeResetCache()
    self.cache[key] = val

  def get(self, key: str):
    self._maybeResetCache()
    return self.cache.get(key, None)


_datasetCache = TimedDatasetCache(5 * 60)


class DatasetList:

  def __init__(self):
    self._datasets: List[DatasetDesc] = []
    self._iter_current = -1
    resp = getJsonOrPrintError("jupyter/v1/datasets/list")
    if resp and resp.datasets:
      self._datasets = resp.datasets

  def _repr_html_(self):
    if not isAuthenticated():
      return ""
    return self._makeDatasetsHtmlTable()

  def __iter__(self):
    return self

  def __next__(self) -> str:
    self._iter_current += 1
    if self._iter_current < len(self._datasets):
      return self._datasets[self._iter_current].name
    raise StopIteration

  def _makeDatasetsHtmlTable(self):
    if len(self._datasets) == 0:
      return "There are no datasets to show."
    headers = [
        TableHeader("Name", TableHeader.LEFT, isCode=True),
        TableHeader("Owner", TableHeader.CENTER),
        TableHeader("Data Refreshed", TableHeader.RIGHT),
        TableHeader("SQL Updated", TableHeader.RIGHT),
        TableHeader("Rows", TableHeader.RIGHT),
        TableHeader("Bytes", TableHeader.RIGHT),
    ]
    rows: List[List[Union[str, UserImage]]] = []
    for d in self._datasets:
      rows.append([
          d.name,
          UserImage(d.ownerInfo.imageUrl, d.ownerInfo.name),
          timeago(d.recentResultMs) if d.recentResultMs != None else '',
          timeago(d.sqlModifiedAtMs) if d.sqlModifiedAtMs != None else '',
          _fmt_num(d.numRows),
          sizeOfFmt(d.numBytes)
      ])
    return renderTemplate("table", headers=headers, rows=rows)


def list():
  return DatasetList()


def _cacheKey(dsName: str):
  return f"{getCurrentBranch()}/{dsName}"


def get(dsName: str, filter_column: Union[str, None] = None, filter_values: Union[List[Any], None] = None):
  cacheKey = _cacheKey(dsName)
  inDeployment = 'WORKSPACE_ID' in os.environ
  df = _datasetCache.get(cacheKey)
  if df is None or not inDeployment:
    if inDeployment:
      stream = _getFromS3(dsName)
    else:
      stream = _getFromWeb(dsName)
    if stream == None:
      return None
    df = cast(
        pandas.DataFrame,
        pandas.read_csv(  # type: ignore
            stream, sep='|', low_memory=False, na_values=['\\N', '\\\\N']))
    _datasetCache.set(cacheKey, df)

  if df is None:
    raise Exception(f"Unable to fetch dataset '{dsName}'")
  elif filter_column != None and filter_values != None:
    return df[df[filter_column].isin(filter_values)]  # type: ignore
  return df


def _getFromWeb(dsName: str):
  data = getJsonOrPrintError(f'jupyter/v1/datasets/get?dsName={quote_plus(dsName)}')
  if data and data.dsrDownloadInfo:
    return getSecureData(data.dsrDownloadInfo, dsName)
  if not isAuthenticated():
    return None
  return None


def _getFromS3(dsName: str):
  _workspaceId = os.getenv('WORKSPACE_ID')
  _pystateBucket = os.getenv('PYSTATE_BUCKET')
  _pystateKeys = os.getenv('PYSTATE_KEYS')
  if _workspaceId == None or _pystateBucket == None or _pystateKeys == None:
    raise Exception(f"EnvVar Missing: WORKSPACE_ID, PYSTATE_BUCKET, PYSTATE_KEYS")
  import boto3  # type: ignore
  try:
    dsKey = f'{_workspaceId}/datasets/{dsName}/{getCurrentBranch()}'
    s3Obj = boto3.client('s3').get_object(Bucket=_pystateBucket, Key=dsKey)  # type: ignore
    fileKeyEnc = base64.b64decode(s3Obj['Metadata']["x-amz-key"])  # type: ignore
    fileIv = base64.b64decode(s3Obj['Metadata']["x-amz-iv"])  # type: ignore
    for key64 in str(_pystateKeys).split(","):
      cipher = AES.new(base64.b64decode(key64), AES.MODE_ECB)  # type: ignore
      fileKey = unpad(cipher.decrypt(fileKeyEnc), AES.block_size)
      cipher = AES.new(fileKey, AES.MODE_CBC, fileIv)  # type: ignore
      bodyDataEnc = cast(bytes, s3Obj['Body'].read())  # type: ignore
      decState = unpad(cipher.decrypt(bodyDataEnc), AES.block_size)
      return io.BytesIO(gzip.decompress(decState))
  except Exception as err:
    strErr = str(err)
    if 'AccessDenied' in strErr or 'NoSuchKey' in strErr:
      raise Exception('Version not found.')
    else:
      raise err
  return None


def _fmt_num(num: Union[int, Any]):
  if type(num) != int:
    return ""
  return format(num, ",")
