import os
import shutil

from conans.client.file_copier import FileCopier
from conans.client.output import ScopedOutput
from conans.client.packager import report_files_from_manifest
from conans.errors import ConanException, conanfile_exception_formatter
from conans.model.conan_file import get_env_context_manager
from conans.model.manifest import FileTreeManifest
from conans.paths import CONANINFO
from conans.tools import chdir, mkdir
from conans.util.conan_v2_mode import conan_v2_property
from conans.util.files import save, mkdir
from conans.util.log import logger


def run_deb_method(conanfile, deb_id, hook_manager, conanfile_path, ref, copy_info=False):
    """ calls the recipe "deb()" method
    - Assigns folders to conanfile.deb_folder, source_folder, install_folder, build_folder
    - Calls pre-post deb hook
    - Prepares FileCopier helper for self.copy
    """

    if conanfile.deb_folder == conanfile.build_folder:
        raise ConanException("Cannot 'conan deb' to the build folder. "
                             "--build-folder and deb folder can't be the same")

    mkdir(conanfile.deb_folder)
    output = conanfile.output
    # Make the copy of all the patterns
    output.info("Generating the deb")
    output.info("deb folder %s" % conanfile.deb_folder)

    with get_env_context_manager(conanfile):
        return _call_deb(conanfile, deb_id, hook_manager, conanfile_path, ref, copy_info)


def _call_deb(conanfile, deb_id, hook_manager, conanfile_path, ref, copy_info):
    output = conanfile.output

    # hook_manager.execute("pre_deb", conanfile=conanfile, conanfile_path=conanfile_path,
    #                      reference=ref, deb_id=deb_id)

    output.highlight("Calling deb()")
    folders = [conanfile.source_folder, conanfile.package_folder] \
        if conanfile.source_folder != conanfile.package_folder else [conanfile.package_folder]
    conanfile.copy = FileCopier(folders, conanfile.deb_folder)
    with conanfile_exception_formatter(str(conanfile), "deb"):
        with chdir(conanfile.package_folder):
            with conan_v2_property(conanfile, 'info',
                                   "'self.info' access in deb() method is deprecated"):
                _create_deb_file(conanfile)
                conanfile.deb()

    # hook_manager.execute("post_deb", conanfile=conanfile, conanfile_path=conanfile_path,
    #                      reference=ref, deb_id=deb_id)

    manifest = _create_aux_files(conanfile, copy_info)
    deb_output = ScopedOutput("%s deb()" % output.scope, output)
    report_files_from_manifest(deb_output, manifest)
    deb_id = deb_id or os.path.basename(conanfile.deb_folder)

    output.success("Deb '%s' created" % deb_id)

    prev = manifest.summary_hash
    output.info("Created deb revision %s" % prev)
    return prev


def _create_aux_files(conanfile, copy_info):
    """ auxiliary method that creates CONANINFO and manifest in
    the deb_folder
    """
    logger.debug("DEB: Creating config files to %s" % conanfile.deb_folder)
    if copy_info:
        try:
            shutil.copy(os.path.join(conanfile.install_folder, CONANINFO),
                        conanfile.deb_folder)
        except IOError:
            raise ConanException("%s does not exist inside of your %s folder. "
                                 "Try to re-build it again to solve it."
                                 % (CONANINFO, conanfile.install_folder))
    else:
        save(os.path.join(conanfile.deb_folder, CONANINFO), conanfile.info.dumps())

    # Create the digest for the deb
    manifest = FileTreeManifest.create(conanfile.deb_folder)
    manifest.save(conanfile.deb_folder)
    return manifest

def _create_deb_file(conanfile):
    output = conanfile.output
    #### set folder name
    package_name = conanfile.name
    package_version = conanfile.version
    deb_folder = package_name
    deb_file = package_name + "_" + package_version + ".deb"
    debian_folder = deb_folder + "/DEBIAN"
    app_folder = deb_folder + "/sense2"
        
    #### generate package in build
    mkdir(debian_folder)
    mkdir(app_folder)
    
    ## add control file
    assert (not(not conanfile.deb_control)), "deb_control is not defined or empty in conanfile.py."
    
    control_file = debian_folder + "/control"
    if os.path.exists(control_file):
        conanfile.run("rm " + control_file)
    add_control_cmd = "echo Package: " + conanfile.deb_control["Package"] + " >> " + control_file + " && " \
                        "echo Version: " + conanfile.deb_control["Version"] + " >> " + control_file + " && "  \
                        "echo Maintainer: " + conanfile.deb_control["Maintainer"] + " >> " + control_file + " && "  \
                        "echo Architecture: " + conanfile.deb_control["Architecture"] + " >> " + control_file + " && "  \
                        "echo Description: " + conanfile.deb_control["Description"] + " >> " + control_file + " && "  \
                        "echo 'Depends: " + conanfile.deb_control["Depends"] + "' >> " + control_file + " && "  \
                        "echo Essential: " + conanfile.deb_control["Essential"] + " >> " + control_file + " "
    conanfile.run(add_control_cmd)

    ## add changelog file
    assert (not(not conanfile.deb_control)), "deb_changelog is not defined or empty in conanfile.py."
    
    changelog_file = debian_folder + "/changelog"
    if os.path.exists(changelog_file):
        conanfile.run("rm " + changelog_file)
    add_changelog_cmd = "echo " + conanfile.deb_changelog + " >> " + changelog_file
    conanfile.run(add_changelog_cmd)

    ## add lib | bin
    add_lib_cmd = "cp -r lib " + app_folder + "/lib "
    if os.path.exists("lib"):
        conanfile.run(add_lib_cmd)
    
    add_bin_cmd = "cp -r bin " + app_folder + "/bin "
    if os.path.exists("bin"):
        conanfile.run(add_bin_cmd)

    ## generate deb package in build
    build_package_cmd = "dpkg-deb --build " + deb_folder + " " + deb_file
    conanfile.run(build_package_cmd)

    ## copy *.deb in package folder to deb folder
    conanfile.copy(deb_file, dst=".", keep_path=False)
    output.success("copy deb_file '%s' to deb folder" % deb_file)
    
    ## clean package folder
    if os.path.exists(deb_folder):
        conanfile.run("rm -rf " + deb_folder)
        output.info("clean deb_folder in package.")
    else:
        msg = "deb_folde '%s' is not existed. \
                Check deb_folder is generated correctly." % (deb_folder)
        output.warn(msg)       

    if os.path.exists(deb_file):
        conanfile.run("rm -rf " + deb_file)
        output.info("clean deb_file in package.")
    else:
        msg = "deb_file '%s' is not existed. \
                Check deb_file is generated correctly." % (deb_file)
        output.warn(msg)
