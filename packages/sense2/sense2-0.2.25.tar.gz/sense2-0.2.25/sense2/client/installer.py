import os
import time
from conans.client.installer import _PackageBuilder as _PackageBuilder_co, BinaryInstaller as BinaryInstaller_co
from sense2.client.conanfile.deb import run_deb_method
from conans.util.files import clean_dirty, is_dirty, make_read_only, mkdir, rmdir, save, set_dirty
from conans.client.generators import TXTGenerator
from conans.paths import BUILD_INFO, CONANINFO, RUN_LOG_NAME
from conans.client.packager import update_package_metadata
from conans.errors import (ConanException, ConanExceptionInUserConanfileMethod,
                           conanfile_exception_formatter, ConanInvalidConfiguration)
from conans.util.env_reader import get_env
from conans.util.tracer import log_package_built, log_package_got_from_local_cache
from conans.client.recorder.action_recorder import INSTALL_ERROR_BUILDING, INSTALL_ERROR_MISSING, \
    INSTALL_ERROR_MISSING_BUILD_FOLDER
from conans.client.source import retrieve_exports_sources


class _PackageBuilder(_PackageBuilder_co):
    
    def _deb(self, conanfile, pref, package_layout, conanfile_path):
        # FIXME: Is weak to assign here the recipe_hash
        manifest = package_layout.recipe_manifest()
        conanfile.info.recipe_hash = manifest.summary_hash

        # Creating ***info.txt files
        save(os.path.join(conanfile.folders.base_build, CONANINFO), conanfile.info.dumps())
        self._output.info("Generated %s" % CONANINFO)
        save(os.path.join(conanfile.folders.base_build, BUILD_INFO),
             TXTGenerator(conanfile).content)
        self._output.info("Generated %s" % BUILD_INFO)

        deb_id = pref.id
        # Do the actual copy, call the conanfile.package() method
        # While installing, the infos goes to build folder
        conanfile.folders.set_base_install(conanfile.folders.base_build)
        prev = run_deb_method(conanfile, deb_id, self._hook_manager, conanfile_path,
                                  pref.ref)

        update_package_metadata(prev, package_layout, deb_id, pref.ref.revision)

        if get_env("CONAN_READ_ONLY_CACHE", False):
            make_read_only(conanfile.folders.base_package)
        # FIXME: Conan 2.0 Clear the registry entry (package ref)
        return prev

    def build_package(self, node, keep_build, recorder, remotes):
        t1 = time.time()

        conanfile = node.conanfile
        pref = node.pref

        package_layout = self._cache.package_layout(pref.ref, conanfile.short_paths)
        base_source = package_layout.source()
        conanfile_path = package_layout.conanfile()
        base_package = package_layout.package(pref)
        base_deb = package_layout.deb(pref)
        
        base_build, skip_build = self._get_build_folder(conanfile, package_layout,
                                                               pref, keep_build, recorder)
        # PREPARE SOURCES
        if not skip_build:
            with package_layout.conanfile_write_lock(self._output):
                set_dirty(base_build)
                self._prepare_sources(conanfile, pref, package_layout, remotes)
                self._copy_sources(conanfile, base_source, base_build)

        # BUILD & PACKAGE
        with package_layout.conanfile_read_lock(self._output):
            self._output.info('Building your package in %s' % base_build)
            try:
                if getattr(conanfile, 'no_copy_source', False):
                    conanfile.folders.set_base_source(base_source)
                else:
                    conanfile.folders.set_base_source(base_build)

                conanfile.folders.set_base_build(base_build)
                conanfile.folders.set_base_imports(base_build)
                conanfile.folders.set_base_package(base_package)
                conanfile.folders.set_base_deb(base_deb)
                # In local cache, generators folder always in build_folder
                conanfile.folders.set_base_generators(base_build)

                if not skip_build:
                    # In local cache, install folder always is build_folder
                    conanfile.folders.set_base_install(base_build)
                    self._build(conanfile, pref)
                    clean_dirty(base_build)

                prev = self._package(conanfile, pref, package_layout, conanfile_path)
                assert prev
                prev1 = self._deb(conanfile, pref, package_layout, conanfile_path)
                assert prev1
                node.prev = prev
                log_file = os.path.join(base_build, RUN_LOG_NAME)
                log_file = log_file if os.path.exists(log_file) else None
                log_package_built(pref, time.time() - t1, log_file)
                recorder.package_built(pref)
            except ConanException as exc:
                recorder.package_install_error(pref, INSTALL_ERROR_BUILDING, str(exc),
                                               remote_name=None)
                raise exc

            return node.pref
        
        
class BinaryInstaller(BinaryInstaller_co):
    def __init__(self, app, recorder):
        super().__init__(app, recorder)
    
    def _build_package(self, node, output, keep_build, remotes):
        conanfile = node.conanfile
        # It is necessary to complete the sources of python requires, which might be used
        # Only the legacy python_requires allow this
        python_requires = getattr(conanfile, "python_requires", None)
        if python_requires and isinstance(python_requires, dict):  # Old legacy python_requires
            for python_require in python_requires.values():
                assert python_require.ref.revision is not None, \
                    "Installer should receive python_require.ref always"
                retrieve_exports_sources(self._remote_manager, self._cache,
                                         python_require.conanfile, python_require.ref, remotes)

        builder = _PackageBuilder(self._cache, output, self._hook_manager, self._remote_manager,
                                  self._generator_manager)
        pref = builder.build_package(node, keep_build, self._recorder, remotes)
        if node.graph_lock_node:
            node.graph_lock_node.prev = pref.revision
        return pref
    
    

def call_system_requirements(conanfile, output):
    try:
        return conanfile.system_requirements()
    except Exception as e:
        output.error("while executing system_requirements(): %s" % str(e))
        raise ConanException("Error in system requirements")