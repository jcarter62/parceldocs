from .parcelfolder import ParcelFolder
import os
from pathlib import Path


class FileList:

    def __init__(self, parcel: str = ''):
        self.parcel = parcel
        self.path = ParcelFolder(parcel=parcel).path
        self.files = []

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        folder = os.listdir(self.path)
        for item in folder:
            name = item
            full_path = os.path.join(self.path, name)
            info = os.stat(os.path.join(self.path, name))
            file = {'name': name, 'fullpath': full_path, 'info': info}
            self.files.append(file)
        return

    #
    # Determine how many files, and total size
    #
    def file_sys_details(self):
        fcount = 0
        fsize = 0
        for f in self.files:
            fcount += 1
            fsize += f['info'].st_size

        result = {
            'filecount': fcount,
            'size': fsize
        }
        return result
