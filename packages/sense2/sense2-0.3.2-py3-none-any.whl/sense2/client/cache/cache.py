import os

from conans.client.cache.editable import EditablePackages
from conans.errors import ConanException
from conans.model.ref import ConanFileReference
from sense2.paths.package_layouts.package_cache_layout import PackageCacheLayout
from conans.paths.package_layouts.package_editable_layout import PackageEditableLayout
from conans.util.files import list_folder_subdirs, load, normalize, save, remove
from conans.util.locks import Lock
from conans.client.cache.cache import (ClientCache as ClientCache_co, _is_case_insensitive_os, )

CONAN_CONF = 'conan.conf'
CONAN_SETTINGS = "settings.yml"
LOCALDB = ".conan.db"
REMOTES = "remotes.json"
PROFILES_FOLDER = "profiles"
HOOKS_FOLDER = "hooks"
TEMPLATES_FOLDER = "templates"
GENERATORS_FOLDER = "generators"



if _is_case_insensitive_os():
    def _check_ref_case(ref, store_folder):
        if not os.path.exists(store_folder):
            return

        tmp = store_folder
        for part in ref.dir_repr().split("/"):
            items = os.listdir(tmp)
            try:
                idx = [item.lower() for item in items].index(part.lower())
                if part != items[idx]:
                    raise ConanException("Requested '{requested}', but found case incompatible"
                                         " recipe with name '{existing}' in the cache. Case"
                                         " insensitive filesystem can't manage this.\n Remove"
                                         " existing recipe '{existing}' and try again.".format(
                        requested=str(ref), existing=items[idx]
                    ))
                tmp = os.path.normpath(tmp + os.sep + part)
            except ValueError:
                return
else:
    def _check_ref_case(ref, store_folder):  # @UnusedVariable
        pass


class ClientCache(ClientCache_co):
    """ Class to represent/store/compute all the paths involved in the execution
    of conans commands. Accesses to real disk and reads/write things. (OLD client ConanPaths)
    """

    def package_layout(self, ref, short_paths=None):
        assert isinstance(ref, ConanFileReference), "It is a {}".format(type(ref))
        edited_ref = self.editable_packages.get(ref.copy_clear_rev())
        if edited_ref:
            conanfile_path = edited_ref["path"]
            layout_file = edited_ref["layout"]
            return PackageEditableLayout(os.path.dirname(conanfile_path), layout_file, ref,
                                         conanfile_path, edited_ref.get("output_folder"))
        else:
            _check_ref_case(ref, self.store)
            base_folder = os.path.normpath(os.path.join(self.store, ref.dir_repr()))
            return PackageCacheLayout(base_folder=base_folder, ref=ref,
                                      short_paths=short_paths, no_lock=self._no_locks())

    