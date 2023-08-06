import os
import json
import requests
import time
import threading
import pickle
import threadwrapper
from cloudscraper import create_scraper
from omnitools import def_template, b64e, b64d, randstr, sha256hd


class FO:
    limit = 8*1024*1024

    def __init__(self, fp, offset):
        self.max = Pixeldrain.max_size
        self.fo = open(fp, "rb")
        fs = os.path.getsize(fp)
        self.offset = offset
        self.ptell = offset or 0
        self.size = fs
        if offset is not None:
            self.size = self.max
            if offset+self.max>fs:
                self.size = fs-offset
            self.fo.seek(offset)
        self.red = 0
        self.spd = 0
        self.pts = time.time()

    def __iter__(self):
        while True:
            r = self.read(65536)
            if not r:
                return
            yield r
            if self.red+(self.offset or 0) >= self.size:
                return
            tell = self.fo.tell()
            spd = tell-self.ptell
            if spd >= self.limit:
                now = time.time()
                diff = now-self.pts
                if diff>1:
                    self.pts = now
                    self.ptell = tell
                    sleep = (spd/diff)/self.limit-diff
                    if sleep>0:
                        time.sleep(sleep)

    def read(self, *args):
        r = self.fo.read(*args)
        tbr = self.max-self.red
        if tbr>0:
            len_r = len(r)
            if len_r > tbr:
                r = r[:tbr]
            self.red += len_r
            return r
        return b""

    def _tell(self):
        if self.red<self.max:
            return self.fo.tell()
        return (self.offset or 0)+self.size


class FindResult:
    def __init__(self, v):
        self.file_id = v["id"]
        self.file_data = v

    def __format__(self, format_spec):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<pixeldrainuploader.utils.FindResult(file_id={}, file_data={{{} ...}})>".format(
            json.dumps(self.file_id),
            json.dumps(self.file_data)[1:31]
        )


class PathTranslator:
    def __init__(self, service_endpoint, identifier):
        self.s = create_scraper()
        identifier = {
            "branch": "PixeldrainPathTranslator",
            "name": identifier
        }
        self.identifier = lambda: identifier.copy()
        self.service_endpoint = service_endpoint.strip("/")
        self.get()

    def get(self):
        return True

    def atob(self, path):
        return path

    def btoa(self, id):
        return id

    def new(self, path, id=None):
        return path

    def update(self):
        return True

    def purge(self):
        return True


class PixeldrainPathTranslator(PathTranslator):
    def get(self):
        data = self.identifier()
        data["op"] = "get"
        r = self.s.post(self.service_endpoint, data=data)
        if r.status_code == 200:
            if r.content:
                self.cache = r.json()
            else:
                self.cache = dict()
        else:
            raise Exception("failed to get_cache", r.status_code, r.content.decode())
        return self.cache

    def atob(self, path):
        for k, v in self.cache.items():
            if v == path:
                return k
        return self.new(path)

    def btoa(self, id):
        return self.cache[id]

    def new(self, path, id=None):
        id = id or randstr(10)
        self.cache[id] = path
        self.update()
        return id

    def update(self):
        data = self.identifier()
        data["op"] = "set"
        data["data"] = json.dumps(self.cache)
        r = self.s.post(self.service_endpoint, data=data)
        if r.status_code != 200:
            raise Exception("failed to update", r.status_code, r.content.decode())
        return True

    def purge(self):
        data = self.identifier()
        data["op"] = "delete"
        r = self.s.post(self.service_endpoint, data=data)
        if r.status_code != 200:
            raise Exception("failed to update", r.status_code, r.content.decode())
        self.cache.clear()
        return True


class Pixeldrain:
    anonymous = True
    max_size = 10*1000*1000*1000-1
    domain = "https://pixeldrain.com"
    file_url = domain+"/u/{}"
    folder_url = domain+"/l/{}"
    clone_url = domain+"/api/file"
    upload_url = domain+"/api/file/{}"
    login_url = domain+"/login"
    logout_url = domain+"/logout"
    make_list_url = domain+"/api/list"
    update_list_url = domain+"/api/list/{}"
    get_lists_url = domain+"/api/user/lists"
    get_list_url = domain+"/api/list/{}"
    get_file_url = domain+"/api/file/{}/info"
    path_translator = PathTranslator

    def __init__(self, account: list):
        self.s = requests.Session()
        self.s.headers.update({
            "user-agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
        })
        self.files = {}
        self.folders = {}
        if account:
            self.anonymous = False
            self.login(account)
        self._path_translator = self.path_translator(
            service_endpoint="https://pixeldrain.exfiltrate.cf",
            identifier=sha256hd(account[0])+".json"
        )

    def __del__(self):
        self.logout()

    def login(self, account):
        r = self.s.post(self.login_url, data={
            "form": "login",
            "username": account[0],
            "password": account[1]
        }, allow_redirects=False)
        if r.status_code != 303:
            raise Exception(r.status_code, r.content.decode())
        if os.path.isfile("sessions.cache"):
            sessions = pickle.loads(b64d(open("sessions.cache", "rb").read().decode()))
            self.files = sessions[0]
            self.folders = sessions[1]

    def write_cache(self):
        open("sessions.cache", "wb").write(b64e(pickle.dumps([
            self.files,
            self.folders
        ])).encode())

    def clear_cache(self):
        self.files.clear()
        self.folders.clear()
        self._path_translator.purge()

    def update_cache(self, lists=None, verbose=False):
        lists = lists or self.get_lists(verbose=verbose)
        for _, v in lists.items():
            _ = json.loads(_)
            self.folders[_[0]] = _[1]
            self.files.update(v)

    def get_file(self, code):
        r = self.s.get(self.get_file_url.format(code))
        if r.status_code != 200 or not r.json()["success"]:
            raise Exception(r.status_code, r.content.decode())
        r = r.json()
        r["name"] = self._path_translator.btoa(r["name"])
        return r

    def get_lists(self, verbose=False):
        r = self.s.get(self.get_lists_url)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content.decode())
        lists = r.json()["lists"]
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**3))
        result = {}
        for _ in lists:
            tw.add(
                job=def_template(self.get_list, _["id"]),
                result=result,
                key=json.dumps([self._path_translator.btoa(_["title"]), _["id"]])
            )
        if verbose:
            while tw.alive_threads_ct:
                print("\rfetching list got", len(result), "/", len(lists), end="", flush=True)
        tw.wait()
        return result

    def get_list(self, id, verbose=False):
        if verbose:
            print("\rfetching list", id, end="", flush=True)
        r = self.s.get(self.get_list_url.format(id))
        if r.status_code != 200 or not r.json()["success"]:
            raise Exception(r.status_code, r.content.decode())
        path = self._path_translator.btoa(r.json()["title"])
        return {
            _["id"]: {
                "id": _["id"],
                "name": self._path_translator.btoa(_["name"]),
                "size": _["size"],
                "hash_sha256": _["hash_sha256"],
                "path": path
            } for _ in r.json()["files"]
        }

    def logout(self):
        self.s.post(self.logout_url)

    def find(self, path, strict=True) -> dict:
        opath = path
        path = path.strip("/")
        dir = "/"+os.path.dirname(path)
        name = os.path.basename(path)
        for _, v in self.files.items():
            if opath != path:
                if v["path"] == dir and v["name"] == name:
                    return v
            else:
                if v["name"] == name:
                    if strict and v["path"] != dir:
                        continue
                    return v

    def find_path_descriptor(self, path) -> str:
        try:
            return self.folders[path]
        except:
            pass

    def findall(self, path, strict=True) -> list:
        r = []
        opath = path
        path = path.strip("/")
        dir = "/"+os.path.dirname(path)
        name = os.path.basename(path)
        for _, v in self.files.items():
            if opath != path:
                if v["path"] == dir and v["name"] == name:
                    r.append(v)
            else:
                if v["name"] == name:
                    if strict and v["path"] != dir:
                        continue
                    r.append(v)
        return r

    def upload(self, root, path, overwrite=False, offset=None, verbose=False, limit=None):
        fp = os.path.join(root, path)
        fs = os.path.getsize(fp)
        fn = os.path.basename(path)
        remote_fp = fn
        dest = ("/"+os.path.dirname(path)).strip("/")
        if dest:
            remote_fp = "/".join([dest, remote_fp])
        remote_fp = "/"+remote_fp
        remote_path = os.path.dirname(remote_fp)
        # print("\r", fp, dest, remote_fp, remote_path)
        # return []
        r0 = self.find(remote_fp)
        if not fs and not r0:
            r0 = [v for _, v in self.files if (v["path"]+"/"+v["name"]).startswith(remote_fp+".pixeldrain_part")]
        else:
            if r0:
                r0 = [r0]
        if r0:
            if overwrite:
                [self.delete(_) for _ in r0]
            else:
                if verbose:
                    print("\rupload remote file exists ({})".format([fp, remote_fp]))
                return r0
        codes = []
        if offset is None and fs>self.max_size:
            for i in range(0, fs, self.max_size):
                codes.extend(self.upload(root, path, offset=i, verbose=verbose))
            return codes
        if offset is not None:
            fn += ".pixeldrain_part{:0>5}".format(offset//self.max_size)
        if len(fn.encode()) > 255:
            raise OverflowError("file name exceeds 255 characters ({})".format(len(fn.encode())))
        upload_url = self.upload_url.format(self._path_translator.atob(fn))
        fo = FO(fp, offset)
        if limit is None:
            fo.limit *= 99
        r = None
        def progress():
            while True:
                tell = fo._tell()
                if offset is not None:
                    tell -= offset
                print("\rprogress: {: >6.2f}/{: >6.2f} MB ({: >6.2f}%)".format(
                    tell/1024/1024,
                    fo.size/1024/1024,
                    tell/fo.size*100
                ), end="", flush=True)
                if r is not None:
                    return
                time.sleep(1)
        def job():
            nonlocal r
            try:
                r = self.s.put(upload_url, data=fo)
            except Exception as e:
                r = e
        p = threading.Thread(target=job)
        p.daemon = True
        p.start()
        if verbose:
            p = threading.Thread(target=progress)
            p.daemon = True
            p.start()
        if verbose:
            print("\ruploading file", fp, upload_url, end="", flush=True)
        stime = time.time()
        while not r:
            time.sleep(1)
        if isinstance(r, Exception):
            raise r
        code = r.json()["id"]
        if not self.anonymous:
            if verbose:
                print("\ruploading file", fp, "add to folder", remote_path, end="", flush=True)
            info = self.get_file(code)
            self.files[info["id"]] = {
                "id": info["id"],
                "name": info["name"],
                "size": info["size"],
                "hash_sha256": info["hash_sha256"],
                "path": remote_path
            }
            self.add_file_to_folder(code, remote_path)
        if verbose:
            print("\ruploaded file", fp, "==>", remote_fp, "elapsed", time.time()-stime, end="", flush=True)
        codes.append(self.file_url.format(code))
        return codes

    def add_file_to_folder(self, code, path):
        if path not in self.folders:
            id = self.make_list(path, code)
        else:
            id = self.folders[path]
            ids = self.get_files_in_folder(path)
            ids = [_["id"] for _ in ids]
            ids += [code]
            self.update_list(id, path, ids)
        return id

    def get_files_in_folder(self, path):
        r = []
        for _, v in self.files.items():
            if v["path"] == path:
                r.append(v)
        return r

    def make_list(self, name, id):
        name = self._path_translator.atob(name)
        if len(name.encode()) > 300:
            raise OverflowError("path exceeds 300 character ({})".format(len(name.encode())))
        r = self.s.post(self.make_list_url, json={
            "title": name,
            "files": [{"id": id}]
        })
        if r.status_code != 201 or not r.json()["success"]:
            raise Exception(r.status_code, r.content.decode())
        id = r.json()["id"]
        self.folders[self._path_translator.btoa(name)] = id
        return id

    def update_list(self, id, name, ids):
        name = self._path_translator.atob(name)
        if len(name.encode()) > 300:
            raise OverflowError("path exceeds 300 character ({})".format(len(name.encode())))
        if len(ids) > 10000:
            raise OverflowError("folder exceeds 10000 files ({})".format(len(ids)))
        r = self.s.put(self.update_list_url.format(id), json={
            "title": name,
            "files": [{"id": id} for id in ids]
        })
        if r.status_code != 200 or not r.json()["success"]:
            raise Exception(r.status_code, r.content.decode())
        return True

    def clone(self, code):
        r = self.s.post(self.clone_url, files={"grab_file": code})
        if r.status_code != 201 or "id" not in r.json():
            raise Exception(r.status_code, r.content.decode())
        return r.json()["id"]

    def export(self, path):
        r = [self.find(path), self.find_path_descriptor(path)]
        if all(r):
            raise Exception("cannot determine file or folder for path:", path)
        if not any(r):
            raise Exception("cannot find path:", path)
        if r[0]:
            return [self.file_url.format(r[0]["id"])]
        if r[1]:
            return {k: self.folder_url.format(v) for k, v in self.folders.items() if k.startswith(path)}

    def delete(self, code):
        r = self.s.delete(self.upload_url.format(code))
        if r.status_code != 200 or not r.json()["success"]:
            raise Exception(r.status_code, r.content.decode())
        self.files.pop(code)
        return True

