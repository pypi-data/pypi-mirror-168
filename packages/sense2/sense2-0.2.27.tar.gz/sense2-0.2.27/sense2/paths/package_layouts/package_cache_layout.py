import os
from conans.paths.package_layouts.package_cache_layout import short_path, PackageCacheLayout as PackageCacheLayout_co
from conans.model.ref import PackageReference
                                         
from conans.util.files import is_dirty
from sense2.paths import DEB_FOLDER

class PackageCacheLayout(PackageCacheLayout_co):
    
    def debs(self):
        return os.path.join(self._base_folder, DEB_FOLDER)

    @short_path
    def deb(self, pref):
        assert isinstance(pref, PackageReference)
        assert pref.ref == self._ref, "{!r} != {!r}".format(pref.ref, self._ref)
        return os.path.join(self._base_folder, DEB_FOLDER, pref.id)
    
    @short_path
    def deb(self, pref):
        assert isinstance(pref, PackageReference)
        assert pref.ref == self._ref, "{!r} != {!r}".format(pref.ref, self._ref)
        return os.path.join(self._base_folder, DEB_FOLDER, pref.id)
    
    def deb_is_dirty(self, pref):
        deb_folder = os.path.join(self._base_folder, DEB_FOLDER, pref.id)
        return is_dirty(deb_folder)
    
    def deb_id_exists(self, deb_id):
        # The package exists if the folder exists, also for short_paths case
        deb_folder = self.deb(PackageReference(self._ref, deb_id))
        return os.path.isdir(deb_folder)