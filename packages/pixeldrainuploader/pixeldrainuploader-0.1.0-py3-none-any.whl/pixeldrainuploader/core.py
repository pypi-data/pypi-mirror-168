from .utils import *
import json
from typing import List


class PixeldrainUploader:
    def __init__(self, account: list, path_translator = PixeldrainPathTranslator, verbose: bool = False):
        self.verbose = verbose
        if verbose:
            print("\rlogging in", end="", flush=True)
        Pixeldrain.path_translator = path_translator or PathTranslator
        self.client = Pixeldrain(account)
        if verbose:
            print("\rlogged in", end="", flush=True)
        if not self.client.anonymous:
            if not self.client.files or not self.client.folders:
                self.client.update_cache()
                self.client.write_cache()

    def upload(self, root, path):
        urls = []
        fp = os.path.join(root, path)
        if os.path.isfile(fp):
            if self.verbose:
                print("\ruploading", fp, end="", flush=True)
            path = path.replace("\\", "/").strip("/")
            urls.extend(self.client.upload(root, path, verbose=self.verbose))
            if self.verbose:
                print("\ruploaded", fp, end="", flush=True)
        elif os.path.isdir(fp):
            for a, b, c in os.walk(fp):
                for d in c:
                    e = os.path.join(a, d)
                    _path = e.replace(root, "")[1:]
                    urls.extend(self.upload(root, _path))
        self.client.write_cache()
        return urls

    def get_files_in_folder(self, *args, **kwargs):
        return [FindResult(_) for _ in self.client.get_files_in_folder(*args, **kwargs)]

    def find(self, *args, **kwargs):
        return [FindResult(self.client.find(*args, **kwargs))]

    def findall(self, *args, **kwargs):
        return [FindResult(_) for _ in self.client.findall(*args, **kwargs)]

    def add_file_to_folder(self, code, path):
        code = self.client.clone(code)
        info = self.client.get_file(code)
        self.client.files[info["id"]] = {
            "id": info["id"],
            "name": info["name"],
            "size": info["size"],
            "hash_sha256": info["hash_sha256"],
            "path": path
        }
        r = self.client.add_file_to_folder(code, path)
        self.client.write_cache()
        return r

    def add_list_to_folder(self, code, path):
        codes = self.client.get_list(code)
        r = []
        print()
        for i, code in enumerate(codes.keys()):
            print("\rimporting {} out of {} files ({})".format(i+1, len(codes), code), end="", flush=True)
            r.append(self.add_file_to_folder(code, path))
        print()
        return r

    def import_url(self, url, path):
        if "/l/" in url:
            return self.add_list_to_folder(url.split("/")[-1], path)
        elif "/u/" in url:
            return [self.add_file_to_folder(url.split("/")[-1], path)]
        raise ValueError("{} is not a valid url")

    def import_urls(self, urls, path):
        r = []
        for i, (k, url) in enumerate(urls.items()):
            print("\rimporting {} out of {} urls ({})".format(i+1, len(urls), url), end="", flush=True)
            r.extend(self.import_url(url, path+k))
        print("\r", end="")
        return r

    def export(self, path):
        return self.client.export(path)

    def export_to_universal(self, urls):
        urls = {k: url.replace(self.client.domain+"/", "") for k, url in urls.items()}
        return b64e(json.dumps(urls))

    def export_universal(self, path):
        return self.export_to_universal(self.export(path))

    def import_universal(self, base64_string, path):
        urls = json.loads(b64d(base64_string).decode())
        urls = {k: self.client.domain+"/{}".format(url) for k, url in urls.items()}
        return self.import_urls(urls, path)

    def destroy(self, rs: List[FindResult]):
        r = []
        for _r in rs:
            r.append(self.client.delete(_r.file_id))
        self.client.write_cache()
        return r


