import os

from conans.client.cmd.test import install_build_and_test
from sense2.client.manager import deps_install
from conans.errors import ConanException
from conans.model.ref import ConanFileReference
from conans.client.cmd.create import _get_test_conanfile_path


def create(app, ref, graph_info, remotes, update, build_modes,
           manifest_folder, manifest_verify, manifest_interactive, keep_build, test_build_folder,
           test_folder, conanfile_path, recorder, is_build_require=False, require_overrides=None):
    assert isinstance(ref, ConanFileReference), "ref needed"
    test_conanfile_path = _get_test_conanfile_path(test_folder, conanfile_path)

    if test_conanfile_path:
        if graph_info.graph_lock:
            # If we have a lockfile, then we are first going to make sure the lockfile is used
            # correctly to build the package in the cache, and only later will try to run
            # test_package
            out = app.out
            out.info("Installing and building %s" % repr(ref))
            deps_install(app=app,
                         ref_or_path=ref,
                         create_reference=ref,
                         install_folder=None,  # Not output conaninfo etc
                         base_folder=None,  # Not output generators
                         manifest_folder=manifest_folder,
                         manifest_verify=manifest_verify,
                         manifest_interactive=manifest_interactive,
                         remotes=remotes,
                         graph_info=graph_info,
                         build_modes=build_modes,
                         update=update,
                         keep_build=keep_build,
                         recorder=recorder,
                         conanfile_path=os.path.dirname(test_conanfile_path))
            out.info("Executing test_package %s" % repr(ref))
            try:
                graph_info.graph_lock.relax()
                # FIXME: It needs to clear the cache, otherwise it fails
                app.binaries_analyzer._evaluated = {}
                # FIXME: Forcing now not building test dependencies, binaries should be there
                install_build_and_test(app, test_conanfile_path, ref, graph_info, remotes,
                                       update, build_modes=None,
                                       test_build_folder=test_build_folder, recorder=recorder)
            except Exception as e:
                raise ConanException("Something failed while testing '%s' test_package after "
                                     "it was built using the lockfile. Please report this error: %s"
                                     % (str(ref), str(e)))

        else:
            install_build_and_test(app, test_conanfile_path,
                                   ref, graph_info, remotes, update,
                                   build_modes=build_modes,
                                   manifest_folder=manifest_folder,
                                   manifest_verify=manifest_verify,
                                   manifest_interactive=manifest_interactive,
                                   keep_build=keep_build,
                                   test_build_folder=test_build_folder,
                                   recorder=recorder,
                                   require_overrides=require_overrides
                                   )
    else:
        deps_install(app=app,
                     ref_or_path=ref,
                     create_reference=ref,
                     install_folder=None,  # Not output infos etc
                     base_folder=None,  # Not output generators
                     manifest_folder=manifest_folder,
                     manifest_verify=manifest_verify,
                     manifest_interactive=manifest_interactive,
                     remotes=remotes,
                     graph_info=graph_info,
                     build_modes=build_modes,
                     update=update,
                     keep_build=keep_build,
                     recorder=recorder,
                     is_build_require=is_build_require,
                     require_overrides=require_overrides)
