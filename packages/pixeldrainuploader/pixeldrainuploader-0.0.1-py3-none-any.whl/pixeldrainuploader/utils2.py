import os
import copy
import json
import re
import random
import requests
import tempfile
import shutil
import time
import threading
import traceback
import pickle
import threadwrapper
from omnitools import def_template, b64e, b64d, encodeURIComponent, decodeURIComponent


class PixeldrainException(Exception):
    pass


class Pixeldrain:
    sep = "\uFDFA"
    domain = "https://pixeldrain.com"
    api_key = None
    file_url = domain+"/u/{}"
    upload_url = domain+"/api/file/{}"
    login_url = domain+"/login"
    logout_url = domain+"/logout"
    api_url = domain+"/api/user/session"
    make_list_url = domain+"/api/list"
    update_list_url = domain+"/api/list/{}"
    get_lists_url = domain+"/api/user/lists"
    get_list_url = domain+"/api/list/{}"

    def __init__(self, account: list):
        self.s = requests.Session()
        self.s.headers.update({
            "user-agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
        })
        self.files = {}
        self.folders = {}
        self.login(account)

    def __del__(self):
        self.logout()

    def login(self, account):
        if account[1]:
            r = self.s.post(self.login_url, data={
                "form": "login",
                "username": account[0],
                "password": account[1]
            }, allow_redirects=False)
            if r.status_code != 303:
                raise Exception(r.status_code, r.content.decode())
            r = self.s.get(self.api_url)
            if r.status_code != 200:
                raise Exception(r.status_code, r.content.decode())
            self.api_key = r.json()[0]["auth_key"]
        else:
            self.s.cookies.update(account[0])
        if len(account) == 4:
            self.files = account[2]
            self.folders = account[3]

    def write_cache(self):
        open("sessions.cache", "wb").write(b64e(pickle.dumps([
            dict(self.s.cookies),
            None,
            self.files,
            self.folders
        ])).encode())

    def get_files(self):
        ...

    def logout(self):
        self.s.get(self.logout_url)

    def upload(self, root, path):
        fp = os.path.join(root, path)
        if self.sep in fp:
            raise ValueError("upload aborted. reserved modifier ({}) is found in path name".format(self.sep))
        fn = (os.path.sep+path.strip(os.path.sep)).replace(os.path.sep, self.sep)
        fn = encodeURIComponent(fn)
        if len(fn) >= 268:
            raise OverflowError("remote filename ({}) too long".format(fn))
        upload_url = self.upload_url.format(fn)
        fs = os.path.getsize(fp)
        fo = open(fp, "rb")
        r = None
        def job():
            nonlocal r
            try:
                r = self.s.put(upload_url, data=fo)
            except Exception as e:
                r = e
        p = threading.Thread(target=job)
        p.daemon = True
        p.start()
        prev_tell = fo.tell()
        while not r:
            time.sleep(1)
            tell = fo.tell()
            print("progress: {:.2f}MB/s {}/{}MB ({:.2f}%)".format(
                (tell - prev_tell)/1024/1024,
                tell/1024/1024,
                fs/1024/1024,
                tell/fs*100
            ))
        if isinstance(r, Exception):
            raise r
        return self.file_url.format(r.json()["id"])


