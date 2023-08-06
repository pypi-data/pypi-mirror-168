import os
from conans.client.conan_api import (ConanApp as ConanApp_co, ConanAPIV1 as ConanAPIV1_co, api_method, _get_conanfile_path, 
                                    _make_abs_path, 
                                    default_manifest_folder as default_manifest_folder_co,
                                    ProfileData as ProfileData_co, get_graph_info, _parse_manifests_arguments
                                    )
from conans.errors import (ConanException, RecipeNotFoundException,
                           PackageNotFoundException, NoRestV2Available, NotFoundException)
from sense2.client.conanfile.deb import run_deb_method
from sense2.client.cache.cache import ClientCache
from conans.client.recorder.upload_recoder import UploadRecorder
from sense2.client.cmd.uploader import CmdUpload
from sense2.client.cmd.uploader_deb import CmdUploadDeb
from conans.client.recorder.action_recorder import ActionRecorder
from conans.client.cmd.export import cmd_export
from conans.model.ref import ConanFileReference
from conans.model.graph_lock import GraphLockFile
from sense2.client.cmd.create import create
from conans.client.graph.graph_manager import GraphManager
from conans.util.files import save_files
from sense2.client.cmd.export_pkg import export_pkg
from conans.model.graph_info import GraphInfo, GRAPH_INFO_FILE


default_manifest_folder = default_manifest_folder_co

class ProfileData(ProfileData_co):
    def __bool__(self):
        return super().__bool__()
    __nonzero__ = __bool__

class Sense2App(ConanApp_co):
    def __init__(self, cache_folder, user_io, http_requester=None, runner=None, quiet_output=None):
        super().__init__(cache_folder, user_io, http_requester, runner, quiet_output)
        
        self.cache = ClientCache(self.cache_folder, self.out)
        # self.loader = ConanFileLoader(self.runner, self.out, self.python_requires,
        #                               self.generator_manager, self.pyreq_loader, self.requester)

        # self.graph_manager = GraphManager(self.out, self.cache, self.remote_manager, self.loader,
        #                                   self.proxy, self.range_resolver, self.binaries_analyzer)


class Sense2APIV1(ConanAPIV1_co):
    
    def create_app(self, quiet_output=None):
        self.app = Sense2App(self.cache_folder, self.user_io, self.http_requester,
                            self.runner, quiet_output=quiet_output)
    
    @api_method
    def create(self, conanfile_path, name=None, version=None, user=None, channel=None,
               profile_names=None, settings=None,
               options=None, env=None, test_folder=None, not_export=False,
               build_modes=None,
               keep_source=False, keep_build=False, verify=None,
               manifests=None, manifests_interactive=None,
               remote_name=None, update=False, cwd=None, test_build_folder=None,
               lockfile=None, lockfile_out=None, ignore_dirty=False, profile_build=None,
               is_build_require=False, conf=None, require_overrides=None):
        """
        API method to create a conan package

        test_folder default None   - looks for default 'test' or 'test_package' folder),
                                    string - test_folder path
                                    False  - disabling tests
        """
        profile_host = ProfileData(profiles=profile_names, settings=settings, options=options,
                                   env=env, conf=conf)
        cwd = cwd or os.getcwd()
        recorder = ActionRecorder()
        try:
            conanfile_path = _get_conanfile_path(conanfile_path, cwd, py=True)

            remotes = self.app.load_remotes(remote_name=remote_name, update=update)
            lockfile = _make_abs_path(lockfile, cwd) if lockfile else None
            graph_info = get_graph_info(profile_host, profile_build, cwd, None,
                                        self.app.cache, self.app.out, lockfile=lockfile)

            # Make sure keep_source is set for keep_build
            keep_source = keep_source or keep_build
            new_ref = cmd_export(self.app, conanfile_path, name, version, user, channel, keep_source,
                                 not not_export, graph_lock=graph_info.graph_lock,
                                 ignore_dirty=ignore_dirty)

            self.app.range_resolver.clear_output()  # invalidate version range output

            # The new_ref contains the revision
            # To not break existing things, that they used this ref without revision
            ref = new_ref.copy_clear_rev()
            recorder.recipe_exported(new_ref)

            if build_modes is None:  # Not specified, force build the tested library
                build_modes = [ref.name]

            manifests = _parse_manifests_arguments(verify, manifests, manifests_interactive, cwd)
            manifest_folder, manifest_interactive, manifest_verify = manifests

            # FIXME: Dirty hack: remove the root for the test_package/conanfile.py consumer
            graph_info.root = ConanFileReference(None, None, None, None, validate=False)
            recorder.add_recipe_being_developed(ref)
            create(self.app, ref, graph_info, remotes, update, build_modes,
                   manifest_folder, manifest_verify, manifest_interactive, keep_build,
                   test_build_folder, test_folder, conanfile_path, recorder=recorder,
                   is_build_require=is_build_require, require_overrides=require_overrides)

            if lockfile_out:
                lockfile_out = _make_abs_path(lockfile_out, cwd)
                graph_lock_file = GraphLockFile(graph_info.profile_host, graph_info.profile_build,
                                                graph_info.graph_lock)
                graph_lock_file.save(lockfile_out)
            return recorder.get_info(self.app.config.revisions_enabled)

        except ConanException as exc:
            recorder.error = True
            exc.info = recorder.get_info(self.app.config.revisions_enabled)
            raise
    
    @api_method
    def upload(self, pattern, package=None, remote_name=None, all_packages=False, confirm=False,
               retry=None, retry_wait=None, integrity_check=False, policy=None, query=None,
               parallel_upload=False):
        """ Uploads a package recipe and the generated binary packages to a specified remote
        """
        upload_recorder = UploadRecorder()
        uploader = CmdUpload(self.app.cache, self.app.user_io, self.app.remote_manager,
                             self.app.loader, self.app.hook_manager)
        remotes = self.app.load_remotes(remote_name=remote_name)
        try:
            uploader.upload(pattern, remotes, upload_recorder, package, all_packages, confirm,
                            retry, retry_wait, integrity_check, policy, query=query,
                            parallel_upload=parallel_upload)
            return upload_recorder.get_info()
        except ConanException as exc:
            upload_recorder.error = True
            exc.info = upload_recorder.get_info()
            raise
    
    @api_method
    def install_deb(self, conanfile_path, info_folder=None, cwd=None):
        cwd = cwd or os.getcwd()
        conanfile_path = _get_conanfile_path(conanfile_path, cwd, py=True)
        info_folder = _make_abs_path(info_folder, cwd)

        if not os.path.exists(info_folder):
            raise ConanException("Specified info-folder doesn't exist")
        print("conan_api install_deb")
        # only infos if exist
        conanfile = self.app.graph_manager.load_consumer_conanfile(conanfile_path, info_folder)
        conanfile.install_deb()


    @api_method
    def install_docker(self, conanfile_path, info_folder=None, cwd=None):
        cwd = cwd or os.getcwd()
        conanfile_path = _get_conanfile_path(conanfile_path, cwd, py=True)
        info_folder = _make_abs_path(info_folder, cwd)

        if not os.path.exists(info_folder):
            raise ConanException("Specified info-folder doesn't exist")
        print("conan_api install_docker")
        # only infos if exist
        conanfile = self.app.graph_manager.load_consumer_conanfile(conanfile_path, info_folder)
        conanfile.install_docker()

    @api_method
    def install_sense_system(self, conanfile_path, info_folder=None, cwd=None):
        cwd = cwd or os.getcwd()
        conanfile_path = _get_conanfile_path(conanfile_path, cwd, py=True)
        info_folder = _make_abs_path(info_folder, cwd)

        if not os.path.exists(info_folder):
            raise ConanException("Specified info-folder doesn't exist")
        print("conan_api install_sense_system")
        # only infos if exist
        conanfile = self.app.graph_manager.load_consumer_conanfile(conanfile_path, info_folder)
        conanfile.install_sense_system()
        
        
    @api_method
    def deb(self, path, build_folder, deb_folder, source_folder=None, install_folder=None,
                cwd=None):
        self.app.load_remotes()

        cwd = cwd or os.getcwd()
        conanfile_path = _get_conanfile_path(path, cwd, py=True)
        build_folder = _make_abs_path(build_folder, cwd)
        source_folder = _make_abs_path(source_folder, cwd, default=os.path.dirname(conanfile_path))
        install_folder = _make_abs_path(install_folder, cwd, default=build_folder)

        conanfile = self.app.graph_manager.load_consumer_conanfile(conanfile_path, install_folder,
                                                                   deps_info_required=True)
        
        default_deb_folder = os.path.join(build_folder, "deb")
        deb_folder = _make_abs_path(deb_folder, cwd, default=default_deb_folder)

        if hasattr(conanfile, "layout"):
            raise ConanException("The usage of the 'conan package' local method is disabled when "
                                 "using layout(). Use 'export-pkg' to test if the recipe is "
                                 "packaging the files correctly or use the cpp.info.local object "
                                 "if you are going to use this package as editable package.")
        else:
            conanfile.folders.set_base_build(build_folder)
            conanfile.folders.set_base_source(source_folder)
            conanfile.folders.set_base_deb(deb_folder)
            conanfile.folders.set_base_install(install_folder)

        run_deb_method(conanfile, None, self.app.hook_manager, conanfile_path, None,
                           copy_info=True)
        
    @api_method
    def upload_deb(self, pattern, package=None, remote_name=None, all_packages=False, confirm=False,
               retry=None, retry_wait=None, integrity_check=False, policy=None, query=None,
               parallel_upload=False):
        """ Uploads a package recipe and the generated binary packages to a specified remote
        """
        upload_recorder = UploadRecorder()
        uploader = CmdUploadDeb(self.app.cache, self.app.user_io, self.app.remote_manager,
                             self.app.loader, self.app.hook_manager, self.app.graph_manager)
        remotes = self.app.load_remotes(remote_name=remote_name)
        try:
            uploader.upload(pattern, remotes, upload_recorder, package, all_packages, confirm,
                            retry, retry_wait, integrity_check, policy, query=query,
                            parallel_upload=parallel_upload)
            return upload_recorder.get_info()
        except ConanException as exc:
            upload_recorder.error = True
            exc.info = upload_recorder.get_info()
            raise

    # @api_method
    # def set_source(self, conanfile_path, source_folder=None, info_folder=None, cwd=None):
    #     cwd = cwd or os.getcwd()
    #     conanfile_path = _get_conanfile_path(conanfile_path, cwd, py=True)
    #     source_folder = _make_abs_path(source_folder, cwd)
    #     info_folder = _make_abs_path(info_folder, cwd)


    #     if not os.path.exists(info_folder):
    #         raise ConanException("Specified info-folder doesn't exist")
    #     print("conan_api set_source")
    #     # only infos if exist
    #     conanfile = self.app.graph_manager.load_consumer_conanfile(conanfile_path, info_folder)
    #     conanfile.exports_sources = os.path.join(source_folder, "*")
    #     print("set exports_sources: ", conanfile.exports_sources)

    @api_method
    def new(self, name, header=False, pure_c=False, test=False, exports_sources=False, bare=False,
            cwd=None, visual_versions=None, linux_gcc_versions=None, linux_clang_versions=None,
            osx_clang_versions=None, shared=None, upload_url=None, gitignore=None,
            gitlab_gcc_versions=None, gitlab_clang_versions=None,
            circleci_gcc_versions=None, circleci_clang_versions=None, circleci_osx_versions=None,
            template=None, defines=None):
        from sense2.client.cmd.new import cmd_new
        cwd = os.path.abspath(cwd or os.getcwd())
        files = cmd_new(name, header=header, pure_c=pure_c, test=test,
                        exports_sources=exports_sources, bare=bare,
                        visual_versions=visual_versions,
                        linux_gcc_versions=linux_gcc_versions,
                        linux_clang_versions=linux_clang_versions,
                        osx_clang_versions=osx_clang_versions, shared=shared,
                        upload_url=upload_url, gitignore=gitignore,
                        gitlab_gcc_versions=gitlab_gcc_versions,
                        gitlab_clang_versions=gitlab_clang_versions,
                        circleci_gcc_versions=circleci_gcc_versions,
                        circleci_clang_versions=circleci_clang_versions,
                        circleci_osx_versions=circleci_osx_versions,
                        template=template, cache=self.app.cache, defines=defines)

        save_files(cwd, files)
        for f in sorted(files):
            self.app.out.success("File saved: %s" % f)
        

    @api_method
    def export_pkg(self, conanfile_path, name, channel, source_folder=None, build_folder=None,
                   package_folder=None, install_folder=None, profile_names=None, settings=None,
                   options=None, env=None, force=False, user=None, version=None, cwd=None,
                   lockfile=None, lockfile_out=None, ignore_dirty=False, profile_build=None,
                   conf=None):
        profile_host = ProfileData(profiles=profile_names, settings=settings, options=options,
                                   env=env, conf=conf)
        remotes = self.app.load_remotes()
        cwd = cwd or os.getcwd()

        recorder = ActionRecorder()
        try:
            conanfile_path = _get_conanfile_path(conanfile_path, cwd, py=True)

            if package_folder:
                if build_folder or source_folder:
                    raise ConanException("package folder definition incompatible with build "
                                         "and source folders")
                package_folder = _make_abs_path(package_folder, cwd)

            build_folder = _make_abs_path(build_folder, cwd)
            if install_folder:
                install_folder = _make_abs_path(install_folder, cwd)
            else:
                # FIXME: This is a hack for old UI, need to be fixed in Conan 2.0
                if os.path.exists(os.path.join(build_folder, GRAPH_INFO_FILE)):
                    install_folder = build_folder
            source_folder = _make_abs_path(source_folder, cwd,
                                           default=os.path.dirname(conanfile_path))

            for folder, path in {"source": source_folder, "build": build_folder,
                                 "package": package_folder}.items():
                if path and not os.path.exists(path):
                    raise ConanException("The {} folder '{}' does not exist."
                                         .format(folder, path))

            lockfile = _make_abs_path(lockfile, cwd) if lockfile else None
            # Checks that no both settings and info files are specified
            graph_info = get_graph_info(profile_host, profile_build, cwd, install_folder,
                                        self.app.cache, self.app.out, lockfile=lockfile)

            new_ref = cmd_export(self.app, conanfile_path, name, version, user, channel, True,
                                 graph_lock=graph_info.graph_lock, ignore_dirty=ignore_dirty)
            ref = new_ref.copy_clear_rev()
            # new_ref has revision
            recorder.recipe_exported(new_ref)
            recorder.add_recipe_being_developed(ref)
            export_pkg(self.app, recorder, new_ref, source_folder=source_folder,
                       build_folder=build_folder, package_folder=package_folder,
                       install_folder=install_folder, graph_info=graph_info, force=force,
                       remotes=remotes, source_conanfile_path=conanfile_path)
            if lockfile_out:
                lockfile_out = _make_abs_path(lockfile_out, cwd)
                graph_lock_file = GraphLockFile(graph_info.profile_host, graph_info.profile_build,
                                                graph_info.graph_lock)
                graph_lock_file.save(lockfile_out)
            return recorder.get_info(self.app.config.revisions_enabled)
        except ConanException as exc:
            recorder.error = True
            exc.info = recorder.get_info(self.app.config.revisions_enabled)
            raise

Sense2 = Sense2APIV1
