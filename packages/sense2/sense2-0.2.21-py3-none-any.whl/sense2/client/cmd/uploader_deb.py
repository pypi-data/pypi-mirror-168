import os
import time
import traceback
from conans.client.cmd.uploader import CmdUpload, _UploadCollecter
from multiprocessing.pool import ThreadPool
from conans.util.progress_bar import left_justify_message
from conans.tools import cpu_count
from conans.model.ref import ConanFileReference, PackageReference, check_valid_ref
from conans.util.log import logger
from conans.errors import ConanException, NotFoundException
from conans.util.env_reader import get_env


class CmdUploadDeb(CmdUpload):
    def __init__(self, cache, user_io, remote_manager, loader, hook_manager, graph_manager):
        super().__init__(cache, user_io, remote_manager, loader, hook_manager)
        self._graph_manager = graph_manager
    
    
    def upload(self, reference_or_pattern, remotes, upload_recorder, package_id=None,
               all_packages=None, confirm=False, retry=None, retry_wait=None, integrity_check=False,
               policy=None, query=None, parallel_upload=False):
        t1 = time.time()
        
        collecter = _UploadCollecter(self._cache, self._user_io, self._output, self._loader)
        refs_by_remote = collecter.collect(package_id, reference_or_pattern, confirm, remotes,
                                           all_packages, query)
        
        if parallel_upload:
            self._user_io.disable_input()
        self._upload_thread_pool = ThreadPool(
            cpu_count() if parallel_upload else 1)

        for remote, refs in refs_by_remote.items():
            self._output.info("Uploading to remote '{}':".format(remote.name))

            def upload_ref(ref_conanfile_prefs):
                _ref, _conanfile, _prefs = ref_conanfile_prefs
                try:
                    self._upload_ref(_conanfile, _ref, _prefs, retry, retry_wait,
                                     integrity_check, policy, remote, upload_recorder, remotes)
                except BaseException as base_exception:
                    base_trace = traceback.format_exc()
                    self._exceptions_list.append((base_exception, _ref, base_trace, remote))

            self._upload_thread_pool.map(upload_ref,
                                         [(ref, conanfile, prefs) for (ref, conanfile, prefs) in
                                          refs])

        self._upload_thread_pool.close()
        self._upload_thread_pool.join()

        if len(self._exceptions_list) > 0:
            for exc, ref, trace, remote in self._exceptions_list:
                t = "recipe" if isinstance(ref, ConanFileReference) else "package"
                msg = "%s: Upload %s to '%s' failed: %s\n" % (str(ref), t, remote.name, str(exc))
                if get_env("CONAN_VERBOSE_TRACEBACK", False):
                    msg += trace
                self._output.error(msg)
            raise ConanException("Errors uploading some packages")

        logger.debug("UPLOAD: Time manager upload: %f" % (time.time() - t1))


    def _upload_ref(self, conanfile, ref, prefs, retry, retry_wait, integrity_check, policy,
                    recipe_remote, upload_recorder, remotes):
        """ Uploads the recipes and binaries identified by ref
        """
        assert (ref.revision is not None), "Cannot upload a recipe without RREV"
        conanfile_path = self._cache.package_layout(ref).conanfile()
        # FIXME: I think it makes no sense to specify a remote to "pre_upload"
        # FIXME: because the recipe can have one and the package a different one
        self._hook_manager.execute("pre_upload", conanfile_path=conanfile_path,
                                   reference=ref, remote=recipe_remote)
        msg = "\rUploading %s to remote '%s'" % (str(ref), recipe_remote.name)
        self._output.info(left_justify_message(msg))
       
        # Now the binaries
        if prefs:
            total = len(prefs)
            p_remote = recipe_remote

            def upload_package_index(index_pref):
                index, pref = index_pref
                try:
                    up_msg = "\rUploading package %d/%d: %s to '%s'" % (index + 1, total,
                                                                        str(pref.id),
                                                                        p_remote.name)
                    self._output.info(left_justify_message(up_msg))
                    self._upload_deb(pref, retry, retry_wait, integrity_check, policy, p_remote)
                    # upload_recorder.add_package(pref, p_remote.name, p_remote.url)
                except BaseException as pkg_exc:
                    trace = traceback.format_exc()
                    return pkg_exc, pref, trace, p_remote

            def upload_package_callback(ret):
                package_exceptions = [r for r in ret if r is not None]
                self._exceptions_list.extend(package_exceptions)
                if not package_exceptions:
                    # FIXME: I think it makes no sense to specify a remote to "post_upload"
                    # FIXME: because the recipe can have one and the package a different one
                    self._hook_manager.execute("post_upload", conanfile_path=conanfile_path,
                                               reference=ref, remote=recipe_remote)

            # This doesn't wait for the packages to end, so the function returns
            # and the "pool entry" for the recipe is released
            self._upload_thread_pool.map_async(upload_package_index,
                                               [(index, pref) for index, pref
                                                in enumerate(prefs)],
                                               callback=upload_package_callback)
        else:
            # FIXME: I think it makes no sense to specify a remote to "post_upload"
            # FIXME: because the recipe can have one and the package a different one
            self._hook_manager.execute("post_upload", conanfile_path=conanfile_path, reference=ref,
                                       remote=recipe_remote)

    def _upload_deb(self, pref, retry=None, retry_wait=None, integrity_check=False,
                        policy=None, p_remote=None):

        assert (pref.revision is not None), "Cannot upload a package without PREV"
        assert (pref.ref.revision is not None), "Cannot upload a package without RREV"

        pkg_layout = self._cache.package_layout(pref.ref)
        conanfile_path = pkg_layout.conanfile()
        package_fold = pkg_layout.package(pref)
        conanfile = self._graph_manager.load_consumer_conanfile(conanfile_path, package_fold)
        
        deb_folder = pkg_layout.deb(pref)
        deb_file = os.path.join(deb_folder, conanfile.name + "_" + conanfile.version + ".deb")
        
        if os.path.exists(deb_file):
            # upload deb file
            upload_deb_cmd = 'ret=$(curl -u "'+ conanfile.apt_user +'" -H "Content-Type: multipart/form-data" --data-binary "@' \
                                + deb_file + '" "' + conanfile.apt_sever + '" -f)'
            conanfile.run(upload_deb_cmd)
        else:
            print("Warning: deb file is not exist")

        return pref

