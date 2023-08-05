#!/usr/bin/env python3 -B -u
#-*- coding: utf-8 -*-

import re
import sys
import logging
logger = logging.getLogger(__name__)
import argparse
import typing
import pathlib
import urllib.parse
import zlib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests
requests.packages.urllib3.disable_warnings()

WETRANSFER_API_URL = "https://wetransfer.com/api/v4/transfers"
WETRANSFER_DOWNLOAD_URL = WETRANSFER_API_URL + "/{transfer_id}/download"
WETRANSFER_UPLOAD_EMAIL_URL = WETRANSFER_API_URL + "/email"
WETRANSFER_VERIFY_URL = WETRANSFER_API_URL + "/{transfer_id}/verify"
WETRANSFER_UPLOAD_LINK_URL = WETRANSFER_API_URL + "/link"
WETRANSFER_FILES_URL = WETRANSFER_API_URL + "/{transfer_id}/files"
WETRANSFER_PART_PUT_URL = WETRANSFER_FILES_URL + "/{file_id}/part-put-url"
WETRANSFER_FINALIZE_MPP_URL = WETRANSFER_FILES_URL + "/{file_id}/finalize-mpp"
WETRANSFER_FINALIZE_URL = WETRANSFER_API_URL + "/{transfer_id}/finalize"
WETRANSFER_DEFAULT_CHUNK_SIZE = 5242880
WETRANSFER_EXPIRE_IN = 604800

def download_url(url:str) -> typing.Optional[str]:
  logger.debug(f"Getting download URL of {url}")
  if url.startswith("https://we.tl/"):
    r = requests.head(url,allow_redirects=True)
    logger.debug(f"Short URL {url} redirects to {r.url}")
    url = r.url
  recipient_id = None
  params = urllib.parse.urlparse(url).path.split("/")[2:]
  if len(params) == 2:
    transfer_id,security_hash = params
  elif len(params) == 3:
    transfer_id,recipient_id,security_hash = params
  else: return
  logger.debug(f"Getting direct_link of {url}")
  j = {
    "intent":"entire_transfer",
    "security_hash":security_hash
  }
  if recipient_id:
    j["recipient_id"] = recipient_id
  s = _prepare_session()
  if not s:
    raise ConnectionError("Could not prepare session")
  r = s.post(WETRANSFER_DOWNLOAD_URL.format(transfer_id=transfer_id),json=j)
  _close_session(s)
  j = r.json()
  return j.get("direct_link")
def _file_unquote(file:str) -> str:
  return urllib.parse.unquote(file).replace("../","").replace("/","").replace("\\","")
def download(url:str,file:str = "") -> None:
  logger.debug(f"Downloading {url}")
  dl_url = download_url(url)
  if not dl_url:
    logger.error(f"Could not find direct link of {url}")
    return
  if not file:
    file = _file_unquote(urllib.parse.urlparse(dl_url).path.split("/")[-1])
  logger.debug(f"Fetching {dl_url}")
  r = requests.get(dl_url,stream=True)
  with open(file,"wb") as f:
    for chunk in r.iter_content(chunk_size=1024):
      f.write(chunk)
def _file_name_and_size(file:str) -> dict:
  filename = pathlib.os.path.basename(file)
  filesize = pathlib.os.path.getsize(file)
  return {
    "name":filename,
    "size":filesize
  }
def _prepare_session() -> typing.Optional[requests.Session]:
  s = requests.Session()
  r = s.get("https://wetransfer.com/")
  m = re.search('name="csrf-token" content="([^"]+)"',r.text)
  if not m:
    logger.error(f"Could not find any csrf-token")
    return
  s.headers.update({
    "x-csrf-token":m.group(1),
    "x-requested-with":"XMLHttpRequest"
  })
  return s
def _close_session(s:requests.Session) -> None: s.close()
def _prepare_email_upload(filenames:typing.List[str],display_name:str,message:str,
  sender:str,recipients:typing.List[str],
  session:requests.Session) -> dict:
  j = {
    "files":[_file_name_and_size(f) for f in filenames],
    "from":sender,
    "display_name":display_name,
    "message":message,
    "recipients":recipients,
    "ui_language":"en"
  }
  r = session.post(WETRANSFER_UPLOAD_EMAIL_URL,json=j)
  return r.json()
def _verify_email_upload(transfer_id:str,session:requests.Session) -> str:
  code = input("Code:")
  j = {
    "code":code,
    "expire_in":WETRANSFER_EXPIRE_IN
  }
  r = session.post(WETRANSFER_VERIFY_URL.format(transfer_id=transfer_id),json=j)
  return r.json()
def _prepare_link_upload(filenames:typing.List[str],display_name:str,message:str,
  session:requests.Session) -> dict:
  j = {
    "files":[_file_name_and_size(f) for f in filenames],
    "display_name":display_name,
    "message":message,
    "ui_language":"en"
  }
  r = session.post(WETRANSFER_UPLOAD_LINK_URL,json=j)
  return r.json()
def _prepare_file_upload(transfer_id:str,file:str,
  session:requests.Session) -> dict:
  j = _file_name_and_size(file)
  r = session.post(WETRANSFER_FILES_URL.format(transfer_id=transfer_id),json=j)
  return r.json()
def _upload_chunks(transfer_id:str,file_id:str,file:str,
  session:requests.Session,
  default_chunk_size:int = WETRANSFER_DEFAULT_CHUNK_SIZE) -> str:
  with open(file,"rb") as f:
    chunk_number = 0
    while True:
      chunk = f.read(default_chunk_size)
      chunk_size = len(chunk)
      if chunk_size == 0: break
      chunk_number += 1
      j = {
        "chunk_crc":zlib.crc32(chunk),
        "chunk_number":chunk_number,
        "chunk_size":chunk_size,
        "retries":0
      }
      r = session.post(WETRANSFER_PART_PUT_URL.format(transfer_id=transfer_id,file_id=file_id),json=j)
      url = r.json().get("url")
      requests.options(url,
      headers={
        "Origin":"https://wetransfer.com",
        "Access-Control-Request-Method":"PUT"
      })
      requests.put(url,data=chunk)
  j = {"chunk_count":chunk_number}
  r = session.put(WETRANSFER_FINALIZE_MPP_URL.format(transfer_id=transfer_id,file_id=file_id),json=j)
  return r.json()
def _finalize_upload(transfer_id:str,session:requests.Session) -> dict:
  r = session.put(WETRANSFER_FINALIZE_URL.format(transfer_id=transfer_id))
  return r.json()
def upload(files:typing.List[str],display_name:str = "",message:str = "",sender:str = None,
  recipients:typing.List[str] = []) -> str:
  logger.debug(f"Checking that all files exists")
  for f in files:
    if not pathlib.os.path.exists(f):
      raise FileNotFoundError(f)
  logger.debug(f"Checking for no duplicate filenames")
  filenames = [pathlib.os.path.basename(f) for f in files]
  if len(files) != len(set(filenames)):
    raise FileExistsError("Duplicate filenames")
  logger.debug(f"Preparing to upload")
  transfer_id = None
  s = _prepare_session()
  if not s:
    raise ConnectionError("Could not prepare session")
  if sender and recipients:
    transfer_id = _prepare_email_upload(files,display_name,message,sender,recipients,s)["id"]
    _verify_email_upload(transfer_id,s)
  else:
    transfer_id = _prepare_link_upload(files,display_name,message,s)["id"]
  logger.debug(f"Get transfer id {transfer_id}")
  for f in files:
    logger.debug(f"Uploading {f} as part of transfer_id {transfer_id}")
    file_id = _prepare_file_upload(transfer_id,f,s)["id"]
    _upload_chunks(transfer_id,file_id,f,s)
  logger.debug(f"Finalizing upload with transfer id {transfer_id}")
  shortened_url = _finalize_upload(transfer_id,s)["shortened_url"]
  _close_session(s)
  return shortened_url

def main():
  log = logging.getLogger(__name__)
  log.setLevel(logging.INFO)
  log.addHandler(logging.StreamHandler())
  ap = argparse.ArgumentParser(
    prog="transferwee",
    description="Download/upload files via wetransfer.com"
  )
  sp = ap.add_subparsers(dest="action",help="action",required=True)
  dp = sp.add_parser("download",help="download files")
  dp.add_argument("-g",action="store_true",
    help="only print the direct link (without downloading it)")
  dp.add_argument("-o",type=str,default="",metavar="file",
    help="output file to be used")
  dp.add_argument("-v",action="store_true",
    help="get verbose/debug logging")
  dp.add_argument("url",nargs="+",type=str,metavar="url",
    help="URL (we.tl/... or wetransfer.com/downloads/...)")
  up = sp.add_parser("upload",help="upload files")
  up.add_argument("-n",type=str,default="",metavar="display_name",
    help="title for the transfer")
  up.add_argument("-m",type=str,default="",metavar="message",
    help="message description for the transfer")
  up.add_argument("-f",type=str,metavar="from",help="sender email")
  up.add_argument("-t",nargs="+",type=str,metavar="to",
    help="recipient emails")
  up.add_argument("-v",action="store_true",
    help="get verbose/debug logging")
  up.add_argument("files",nargs="+",type=str,metavar="file",
    help="files to upload")
  args = ap.parse_args()
  if args.v: log.setLevel(logging.DEBUG)
  if args.action == "download":
    if args.g:
      for u in args.url: print(download_url(u))
    else:
      for u in args.url: download(u,args.o)
  if args.action == "upload":
    print(upload(args.files,args.n,args.m,args.f,args.t))
if __name__ == "__main__": sys.exit(main())
