import os
import re

from conans.client.cmd.new_ci import ci_get_files
from conans.errors import ConanException
from conans.model.ref import ConanFileReference, get_reference_fields
from conans.util.files import load
from conans.client.cmd.new import (conanfile_bare, 
                                   conanfile_sources, conanfile_header,
                                   test_conanfile, test_cmake,
                                   test_cmake_pure_c, test_main,
                                   hello_c, hello_h,
                                   hello_cpp, cmake_pure_c,
                                   cmake, gitignore_template,
                                   _render_template, 
                                   _get_files_from_template_dir)

conanfile = """from conans import CMake, tools
from sense2 import Sense2File, parseRequires2Denpens
import os

class {package_name}Conan(Sense2File):
    name = "{name}"
    version = "{version}"
    # license = "<Put the package license here>"
    # author = "<Put your name here> <And your email here>"
    # url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of {package_name} here>"
    # topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {{"shared": [True, False], "fPIC": [True, False]}}
    default_options = {{"shared": False, "fPIC": True}}
    generators = "cmake"
    requires = ""
    # docker_version = "<dokcer version>"
    # sense_system_deb = "<debs>"
    
    ## make deb setting
    deb_control = {{
       "Package": name,
       "Version": version,
       "Maintainer": "tester",
       "Architecture": "amd64",
       "Description": "descriptionn",
       "Section": "custom",
       "Priority": "optional",
       "Essential": "no",
       "Depends": parseRequires2Denpens(requires),
       "Homepage": "www.example.com",
    }}
    changelog = "my changelog test"
    
    ### upload cpp package to artifactory
    # user="user"
    # channel="beta"

    ## upload deb setting
    apt_user = "qiuhai"
    apt_sever = "http://10.0.50.109:8081/repository/sense2-system-deb/"
    
    ## set source at the same folder with recipe
    exports_sources = "*"

#     def source(self):
#         # self.run("git clone http://10.0.50.109:9999/open_source/hello.git")
#         # self.run("cd hello")
#         # This small hack might be useful to guarantee proper /MT /MD linkage
#         # in MSVC if the packaged project doesn't have variables to set it
#         # properly
# #         tools.replace_in_file("CMakeLists.txt", "project(MD5Encrypter)",
# #                               '''project(MD5Encrypter)
# # include(${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake)
# # conan_basic_setup()''')
#         pass

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=".")
        cmake.build()
        pass

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*", dst="bin", src="bin")
        
"""


def cmd_new(ref, header=False, pure_c=False, test=False, exports_sources=False, bare=False,
            visual_versions=None, linux_gcc_versions=None, linux_clang_versions=None,
            osx_clang_versions=None, shared=None, upload_url=None, gitignore=None,
            gitlab_gcc_versions=None, gitlab_clang_versions=None,
            circleci_gcc_versions=None, circleci_clang_versions=None, circleci_osx_versions=None,
            template=None, cache=None, defines=None):
    try:
        name, version, user, channel, revision = get_reference_fields(ref, user_channel_input=False)
        # convert "package_name" -> "PackageName"
        package_name = re.sub(r"(?:^|[\W_])(\w)", lambda x: x.group(1).upper(), name)
    except ValueError:
        raise ConanException("Bad parameter, please use full package name,"
                             "e.g.: MyLib/1.2.3@user/testing")

    # Validate it is a valid reference
    ConanFileReference(name, version, user, channel)

    if header and exports_sources:
        raise ConanException("'header' and 'sources' are incompatible options")
    if pure_c and header:
        raise ConanException("'pure_c' is incompatible with 'header'")
    if pure_c and not exports_sources:
        raise ConanException("'pure_c' requires the use of --source")
    if bare and (header or exports_sources):
        raise ConanException("'bare' is incompatible with 'header' and 'sources'")
    if template and (header or exports_sources or bare or pure_c):
        raise ConanException("'template' is incompatible with 'header', "
                             "'sources', 'pure-c' and 'bare'")

    defines = defines or dict()

    if header:
        files = {"conanfile.py": conanfile_header.format(name=name, version=version,
                                                         package_name=package_name)}
    elif exports_sources:
        if not pure_c:
            files = {"conanfile.py": conanfile_sources.format(name=name, version=version,
                                                              package_name=package_name,
                                                              configure=""),
                     "src/{}.cpp".format(name): hello_cpp.format(name=name, version=version),
                     "src/{}.h".format(name): hello_h.format(name=name, version=version),
                     "src/CMakeLists.txt": cmake.format(name=name, version=version)}
        else:
            config = ("\n    def configure(self):\n"
                      "        del self.settings.compiler.libcxx\n"
                      "        del self.settings.compiler.cppstd\n")
            files = {"conanfile.py": conanfile_sources.format(name=name, version=version,
                                                              package_name=package_name,
                                                              configure=config),
                     "src/{}.c".format(name): hello_c.format(name=name, version=version),
                     "src/{}.h".format(name): hello_h.format(name=name, version=version),
                     "src/CMakeLists.txt": cmake_pure_c.format(name=name, version=version)}
    elif bare:
        files = {"conanfile.py": conanfile_bare.format(name=name, version=version,
                                                       package_name=package_name)}
    elif template:
        is_file_template = os.path.basename(template).endswith('.py')
        if is_file_template:
            if not os.path.isabs(template):
                # FIXME: Conan 2.0. The old path should be removed
                old_path = os.path.join(cache.cache_folder, "templates", template)
                new_path = os.path.join(cache.cache_folder, "templates", "command/new", template)
                template = new_path if os.path.isfile(new_path) else old_path
            if not os.path.isfile(template):
                raise ConanException("Template doesn't exist: %s" % template)
            replaced = _render_template(load(template),
                                        name=name,
                                        version=version,
                                        package_name=package_name,
                                        defines=defines)
            files = {"conanfile.py": replaced}
        elif template == "cmake_lib":
            from conans.assets.templates.new_v2_cmake import get_cmake_lib_files
            files = get_cmake_lib_files(name, version, package_name)
        elif template == "cmake_exe":
            from conans.assets.templates.new_v2_cmake import get_cmake_exe_files
            files = get_cmake_exe_files(name, version, package_name)
        elif template == "meson_lib":
            from conans.assets.templates.new_v2_meson import get_meson_lib_files
            files = get_meson_lib_files(name, version, package_name)
        elif template == "meson_exe":
            from conans.assets.templates.new_v2_meson import get_meson_exe_files
            files = get_meson_exe_files(name, version, package_name)
        elif template == "msbuild_lib":
            from conans.assets.templates.new_v2_msbuild import get_msbuild_lib_files
            files = get_msbuild_lib_files(name, version, package_name)
        elif template == "msbuild_exe":
            from conans.assets.templates.new_v2_msbuild import get_msbuild_exe_files
            files = get_msbuild_exe_files(name, version, package_name)
        elif template == "bazel_lib":
            from conans.assets.templates.new_v2_bazel import get_bazel_lib_files
            files = get_bazel_lib_files(name, version, package_name)
        elif template == "bazel_exe":
            from conans.assets.templates.new_v2_bazel import get_bazel_exe_files
            files = get_bazel_exe_files(name, version, package_name)
        elif template == "autotools_lib":
            from conans.assets.templates.new_v2_autotools import get_autotools_lib_files
            files = get_autotools_lib_files(name, version, package_name)
        elif template == "autotools_exe":
            from conans.assets.templates.new_v2_autotools import get_autotools_exe_files
            files = get_autotools_exe_files(name, version, package_name)
        else:
            if not os.path.isabs(template):
                template = os.path.join(cache.cache_folder, "templates", "command/new", template)
            if not os.path.isdir(template):
                raise ConanException("Template doesn't exist: {}".format(template))
            template = os.path.normpath(template)
            files = _get_files_from_template_dir(template_dir=template,
                                                 name=name,
                                                 version=version,
                                                 package_name=package_name,
                                                 defines=defines)
    else:
        files = {"conanfile.py": conanfile.format(name=name, version=version,
                                                  package_name=package_name)}

    if test:
        files["test_package/conanfile.py"] = test_conanfile.format(name=name, version=version,
                                                                   user=user, channel=channel,
                                                                   package_name=package_name)
        if pure_c:
            files["test_package/example.c"] = test_main.format(name=name)
            files["test_package/CMakeLists.txt"] = test_cmake_pure_c
        else:
            include_name = name if exports_sources else "hello"
            files["test_package/example.cpp"] = test_main.format(name=include_name)
            files["test_package/CMakeLists.txt"] = test_cmake

    if gitignore:
        files[".gitignore"] = gitignore_template

    files.update(ci_get_files(name, version, user, channel, visual_versions,
                              linux_gcc_versions, linux_clang_versions,
                              osx_clang_versions, shared, upload_url,
                              gitlab_gcc_versions, gitlab_clang_versions,
                              circleci_gcc_versions, circleci_clang_versions,
                              circleci_osx_versions))
    return files

