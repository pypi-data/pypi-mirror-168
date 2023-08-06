import os

from conans.model.new_build_info import NewCppInfo
from conans.model.layout import Folders as Folders_co, Infos as Infos_co


class Infos(Infos_co):

    def __init__(self):
        super().__init__()
        self.deb = NewCppInfo(with_defaults=True)

class Folders(Folders_co):
    
    def __init__(self):
        super().__init__()
        self._base_deb = None
        self.deb = ""

    @property
    def base_deb(self):
        return self._base_deb

    def set_base_deb(self, folder):
        self._base_deb = folder

    @property
    def deb_folder(self):
        """For the cache, the package folder is only the base"""
        return self._base_deb
