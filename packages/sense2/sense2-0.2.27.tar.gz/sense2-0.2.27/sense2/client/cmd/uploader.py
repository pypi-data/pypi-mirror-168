import os
from conans.client.cmd.uploader import (_PackagePreparator as _PackagePreparator_co, 
                                        compress_files, CmdUpload as CmdUpload_co)
from conans.paths import (CONAN_MANIFEST, CONANFILE, EXPORT_SOURCES_TGZ_NAME,
                          EXPORT_TGZ_NAME, PACKAGE_TGZ_NAME, CONANINFO)
from conans.util.files import (load, clean_dirty, is_dirty,
                               gzopen_without_timestamps, set_dirty_context_manager)
from conans.model.manifest import gather_files
from conans.errors import ConanException


class _PackagePreparator(_PackagePreparator_co):
    
    def _compress_recipe_files(self, layout, ref):
        download_export_folder = layout.download_export()

        for f in (EXPORT_TGZ_NAME, EXPORT_SOURCES_TGZ_NAME):
            tgz_path = os.path.join(download_export_folder, f)
            if is_dirty(tgz_path):
                self._output.warn("%s: Removing %s, marked as dirty" % (str(ref), f))
                os.remove(tgz_path)
                clean_dirty(tgz_path)

        export_folder = layout.export()
        files, symlinks = gather_files(export_folder)
        if CONANFILE not in files or CONAN_MANIFEST not in files:
            raise ConanException("Cannot upload corrupted recipe '%s'" % str(ref))
        export_src_folder = layout.export_sources()
        src_files, src_symlinks = gather_files(export_src_folder)

        result = {CONANFILE: files.pop(CONANFILE),
                  CONAN_MANIFEST: files.pop(CONAN_MANIFEST)}

        def add_tgz(tgz_name, tgz_files, tgz_symlinks, msg):
            tgz = os.path.join(download_export_folder, tgz_name)
            if os.path.isfile(tgz):
                result[tgz_name] = tgz
            elif tgz_files:
                if self._output and not self._output.is_terminal:
                    self._output.writeln(msg)
                tgz = compress_files(tgz_files, tgz_symlinks, tgz_name, download_export_folder,
                                     self._output)
                result[tgz_name] = tgz

        add_tgz(EXPORT_TGZ_NAME, files, symlinks, "Compressing recipe...")
        # add_tgz(EXPORT_SOURCES_TGZ_NAME, src_files, src_symlinks, "Compressing recipe sources...")

        return result


class CmdUpload(CmdUpload_co):
    def __init__(self, cache, user_io, remote_manager, loader, hook_manager):
        super().__init__(cache, user_io, remote_manager, loader, hook_manager)
        self._preparator = _PackagePreparator(cache, remote_manager, hook_manager, self._output)