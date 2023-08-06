import os
import sys
import tidevice
from pathlib import Path
from tidevice._utils import ProgressReader
from evatidevice.wrapper import retry_wrapper


class EvaTidevice:
    def __init__(self, udid: str, bundle_id: str, command: str = "VendDocuments"):
        t = tidevice.Device(udid=udid)
        self.fsync = t.app_sync(bundle_id, command)

    @retry_wrapper()
    def exists(self, dstname):
        self.fsync.exists(dstname)

    @retry_wrapper()
    def mkdir(self, dstname):
        self.fsync.mkdir(dstname)

    @retry_wrapper()
    def push_content(self, dstname, preader):
        self.fsync.push_content(dstname, preader)

    def _pushtree(self, entries, src, dst):
        if not self.exists(dst):
            self.mkdir(dst)
        for srcentry in entries:
            srcname = os.path.join(src, srcentry.name)
            dstname = Path(os.path.join(dst, srcentry.name)).as_posix()
            if srcentry.is_dir():
                if not self.exists(dstname):
                    self.mkdir(dstname)
                self.pushtree(srcname, dstname)
                continue
            print("Copying {!r} to device...".format(srcname), end=" ")
            sys.stdout.flush()
            filesize = os.path.getsize(srcname)
            with open(srcname, 'rb') as f:
                preader = ProgressReader(f, filesize)
                self.push_content(dstname, preader)
            preader.finish()
            print("DONE.")
        return dst

    def pushtree(self, src, dst):
        with os.scandir(src) as itr:
            entries = list(itr)
        return self._pushtree(entries=entries, src=src, dst=dst)

    def pulltree(self,  src, dst):
        self.fsync.pull(src, dst)
