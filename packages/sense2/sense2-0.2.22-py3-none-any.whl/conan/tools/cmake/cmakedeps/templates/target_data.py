import os
import textwrap

from conan.tools.cmake.cmakedeps import FIND_MODE_NONE, FIND_MODE_CONFIG, FIND_MODE_MODULE, \
    FIND_MODE_BOTH
from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate
from conan.tools.cmake.utils import get_cmake_package_name, get_find_mode
"""

foo-release-x86_64-data.cmake

"""


class ConfigDataTemplate(CMakeDepsFileTemplate):

    @property
    def filename(self):
        data_fname = "" if not self.generating_module else "module-"
        data_fname += "{}-{}".format(self.file_name, self.configuration.lower())
        if self.arch:
            data_fname += "-{}".format(self.arch)
        data_fname += "-data.cmake"
        return data_fname

    @property
    def context(self):
        global_cpp = self._get_global_cpp_cmake()
        if not self.build_modules_activated:
            global_cpp.build_modules_paths = ""

        components = self._get_required_components_cpp()
        # using the target names to name components, may change in the future?
        components_names = " ".join([components_target_name for components_target_name, _ in
                                    reversed(components)])

        components_cpp = [(cmake_target_name.replace("::", "_"), cmake_target_name, cpp)
                          for cmake_target_name, cpp in components]

        # For the build requires, we don't care about the transitive (only runtime for the br)
        # so as the xxx-conf.cmake files won't be generated, don't include them as find_dependency
        # This is because in Conan 2.0 model, only the pure tools like CMake will be build_requires
        # for example a framework test won't be a build require but a "test/not public" require.
        dependency_filenames = self._get_dependency_filenames()
        # Get the nodes that have the property cmake_find_mode=None (no files to generate)
        dependency_find_modes = self._get_dependencies_find_modes()
        # package_folder might not be defined if Editable and layout()
        package_folder = self.conanfile.package_folder or ""
        package_folder = package_folder.replace('\\', '/').replace('$', '\\$').replace('"', '\\"')

        return {"global_cpp": global_cpp,
                "has_components": self.conanfile.cpp_info.has_components,
                "pkg_name": self.pkg_name,
                "file_name": self.file_name,
                "package_folder": package_folder,
                "config_suffix": self.config_suffix,
                "components_names": components_names,
                "components_cpp": components_cpp,
                "dependency_filenames": " ".join(dependency_filenames),
                "dependency_find_modes": dependency_find_modes}

    @property
    def template(self):
        # This will be at: XXX-release-data.cmake
        ret = textwrap.dedent("""\
              ########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
              #############################################################################################

              {% if components_names %}
              list(APPEND {{ pkg_name }}_COMPONENT_NAMES {{ components_names }})
              list(REMOVE_DUPLICATES {{ pkg_name }}_COMPONENT_NAMES)
              {% else %}
              set({{ pkg_name }}_COMPONENT_NAMES "")
              {% endif %}
              {% if dependency_filenames %}
              list(APPEND {{ pkg_name }}_FIND_DEPENDENCY_NAMES {{ dependency_filenames }})
              list(REMOVE_DUPLICATES {{ pkg_name }}_FIND_DEPENDENCY_NAMES)
              {% else %}
              set({{ pkg_name }}_FIND_DEPENDENCY_NAMES "")
              {% endif %}
              {% for dep_name, mode in dependency_find_modes.items() %}
              set({{ dep_name }}_FIND_MODE "{{ mode }}")
              {% endfor %}

              ########### VARIABLES #######################################################################
              #############################################################################################
              set({{ pkg_name }}_PACKAGE_FOLDER{{ config_suffix }} "{{ package_folder }}")
              set({{ pkg_name }}_BUILD_MODULES_PATHS{{ config_suffix }} {{ global_cpp.build_modules_paths }})


              set({{ pkg_name }}_INCLUDE_DIRS{{ config_suffix }} {{ global_cpp.include_paths }})
              set({{ pkg_name }}_RES_DIRS{{ config_suffix }} {{ global_cpp.res_paths }})
              set({{ pkg_name }}_DEFINITIONS{{ config_suffix }} {{ global_cpp.defines }})
              set({{ pkg_name }}_SHARED_LINK_FLAGS{{ config_suffix }} {{ global_cpp.sharedlinkflags_list }})
              set({{ pkg_name }}_EXE_LINK_FLAGS{{ config_suffix }} {{ global_cpp.exelinkflags_list }})
              set({{ pkg_name }}_OBJECTS{{ config_suffix }} {{ global_cpp.objects_list }})
              set({{ pkg_name }}_COMPILE_DEFINITIONS{{ config_suffix }} {{ global_cpp.compile_definitions }})
              set({{ pkg_name }}_COMPILE_OPTIONS_C{{ config_suffix }} {{ global_cpp.cflags_list }})
              set({{ pkg_name }}_COMPILE_OPTIONS_CXX{{ config_suffix }} {{ global_cpp.cxxflags_list}})
              set({{ pkg_name }}_LIB_DIRS{{ config_suffix }} {{ global_cpp.lib_paths }})
              set({{ pkg_name }}_LIBS{{ config_suffix }} {{ global_cpp.libs }})
              set({{ pkg_name }}_SYSTEM_LIBS{{ config_suffix }} {{ global_cpp.system_libs }})
              set({{ pkg_name }}_FRAMEWORK_DIRS{{ config_suffix }} {{ global_cpp.framework_paths }})
              set({{ pkg_name }}_FRAMEWORKS{{ config_suffix }} {{ global_cpp.frameworks }})
              set({{ pkg_name }}_BUILD_DIRS{{ config_suffix }} {{ global_cpp.build_paths }})


              set({{ pkg_name }}_COMPONENTS{{ config_suffix }} {{ components_names }})
              {%- for comp_variable_name, comp_target_name, cpp in components_cpp %}

              ########### COMPONENT {{ comp_target_name }} VARIABLES ############################################

              set({{ pkg_name }}_{{ comp_variable_name }}_INCLUDE_DIRS{{ config_suffix }} {{ cpp.include_paths }})
              set({{ pkg_name }}_{{ comp_variable_name }}_LIB_DIRS{{ config_suffix }} {{ cpp.lib_paths }})
              set({{ pkg_name }}_{{ comp_variable_name }}_RES_DIRS{{ config_suffix }} {{ cpp.res_paths }})
              set({{ pkg_name }}_{{ comp_variable_name }}_DEFINITIONS{{ config_suffix }} {{ cpp.defines }})
              set({{ pkg_name }}_{{ comp_variable_name }}_OBJECTS{{ config_suffix }} {{ cpp.objects_list }})
              set({{ pkg_name }}_{{ comp_variable_name }}_COMPILE_DEFINITIONS{{ config_suffix }} {{ cpp.compile_definitions }})
              set({{ pkg_name }}_{{ comp_variable_name }}_COMPILE_OPTIONS_C{{ config_suffix }} "{{ cpp.cflags_list }}")
              set({{ pkg_name }}_{{ comp_variable_name }}_COMPILE_OPTIONS_CXX{{ config_suffix }} "{{ cpp.cxxflags_list }}")
              set({{ pkg_name }}_{{ comp_variable_name }}_LIBS{{ config_suffix }} {{ cpp.libs }})
              set({{ pkg_name }}_{{ comp_variable_name }}_SYSTEM_LIBS{{ config_suffix }} {{ cpp.system_libs }})
              set({{ pkg_name }}_{{ comp_variable_name }}_FRAMEWORK_DIRS{{ config_suffix }} {{ cpp.framework_paths }})
              set({{ pkg_name }}_{{ comp_variable_name }}_FRAMEWORKS{{ config_suffix }} {{ cpp.frameworks }})
              set({{ pkg_name }}_{{ comp_variable_name }}_DEPENDENCIES{{ config_suffix }} {{ cpp.public_deps }})
              set({{ pkg_name }}_{{ comp_variable_name }}_SHARED_LINK_FLAGS{{ config_suffix }} {{ cpp.sharedlinkflags_list }})
              set({{ pkg_name }}_{{ comp_variable_name }}_EXE_LINK_FLAGS{{ config_suffix }} {{ cpp.exelinkflags_list }})
              set({{ pkg_name }}_{{ comp_variable_name }}_LINKER_FLAGS{{ config_suffix }}
                      $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>{{ ':${' }}{{ pkg_name }}_{{ comp_variable_name }}_SHARED_LINK_FLAGS{{ config_suffix }}}>
                      $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>{{ ':${' }}{{ pkg_name }}_{{ comp_variable_name }}_SHARED_LINK_FLAGS{{ config_suffix }}}>
                      $<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>{{ ':${' }}{{ pkg_name }}_{{ comp_variable_name }}_EXE_LINK_FLAGS{{ config_suffix }}}>
              )


              {%- endfor %}
          """)
        return ret

    def _get_global_cpp_cmake(self):
        global_cppinfo = self.conanfile.cpp_info.aggregated_components()
        pfolder_var_name = "{}_PACKAGE_FOLDER{}".format(self.pkg_name, self.config_suffix)
        return _TargetDataContext(global_cppinfo, pfolder_var_name, self.conanfile.package_folder)

    def _get_required_components_cpp(self):
        """Returns a list of (component_name, DepsCppCMake)"""
        ret = []
        sorted_comps = self.conanfile.cpp_info.get_sorted_components()
        pfolder_var_name = "{}_PACKAGE_FOLDER{}".format(self.pkg_name, self.config_suffix)
        direct_visible_host = self.conanfile.dependencies.filter({"build": False, "visible": True,
                                                                  "direct": True})
        for comp_name, comp in sorted_comps.items():
            deps_cpp_cmake = _TargetDataContext(comp, pfolder_var_name,
                                                self.conanfile.package_folder)
            public_comp_deps = []
            for require in comp.requires:
                if "::" in require:  # Points to a component of a different package
                    pkg, cmp_name = require.split("::")
                    req = direct_visible_host[pkg]
                    public_comp_deps.append(self.get_component_alias(req, cmp_name))
                else:  # Points to a component of same package
                    public_comp_deps.append(self.get_component_alias(self.conanfile, require))
            deps_cpp_cmake.public_deps = " ".join(public_comp_deps)
            component_target_name = self.get_component_alias(self.conanfile, comp_name)
            ret.append((component_target_name, deps_cpp_cmake))
        ret.reverse()
        return ret

    def _get_dependency_filenames(self):
        if self.conanfile.is_build_context:
            return []
        ret = []
        direct_host = self.conanfile.dependencies.filter({"build": False, "visible": True,
                                                          "direct": True})
        if self.conanfile.cpp_info.required_components:
            for dep_name, _ in self.conanfile.cpp_info.required_components:
                if dep_name and dep_name not in ret:  # External dep
                    req = direct_host[dep_name]
                    ret.append(get_cmake_package_name(req))
        elif direct_host:
            ret = [get_cmake_package_name(r, self.generating_module) for r in direct_host.values()]

        return ret

    def _get_dependencies_find_modes(self):
        ret = {}
        if self.conanfile.is_build_context:
            return ret
        deps = self.conanfile.dependencies.filter({"build": False, "visible": True, "direct": True})
        for dep in deps.values():
            dep_file_name = get_cmake_package_name(dep, self.generating_module)
            find_mode = get_find_mode(dep)
            default_value = "NO_MODULE" if not self.generating_module else "MODULE"
            values = {
                FIND_MODE_NONE: "",
                FIND_MODE_CONFIG: "NO_MODULE",
                FIND_MODE_MODULE: "MODULE",
                # When the dependency is "both" or not defined, we use the one is forced
                # by self.find_module_mode (creating modules files-> modules, config -> config)
                FIND_MODE_BOTH: default_value,
                None: default_value}
            ret[dep_file_name] = values[find_mode]
        return ret


class _TargetDataContext(object):

    def __init__(self, cpp_info, pfolder_var_name, package_folder):

        def join_paths(paths):
            """
            Paths are doubled quoted, and escaped (but spaces)
            e.g: set(LIBFOO_INCLUDE_DIRS "/path/to/included/dir" "/path/to/included/dir2")
            """
            ret = []
            for p in paths:
                assert os.path.isabs(p), "{} is not absolute".format(p)

                # Trying to use a ${mypkg_PACKAGE_FOLDER}/include path instead of full
                # TODO: We could do something similar for some build_folder for editables
                # package_folder can be None if editable and layout()
                if package_folder is not None and p.startswith(package_folder):
                    # Prepend the {{ pkg_name }}_PACKAGE_FOLDER{{ config_suffix }}
                    rel = p[len(package_folder):]
                    rel = rel.replace('\\', '/').replace('$', '\\$').replace('"', '\\"').lstrip("/")
                    norm_path = ("${%s}/%s" % (pfolder_var_name, rel))
                else:
                    norm_path = p.replace('\\', '/').replace('$', '\\$').replace('"', '\\"')
                ret.append('"{}"'.format(norm_path))

            return "\n\t\t\t".join(ret)

        def join_flags(separator, values):
            # Flags have to be escaped
            ret = separator.join(v.replace('\\', '\\\\').replace('$', '\\$').replace('"', '\\"')
                                 for v in values)
            return ret

        def join_defines(values, prefix=""):
            # Defines have to be escaped, included spaces
            return "\n\t\t\t".join('"%s%s"' % (prefix, v.replace('\\', '\\\\').replace('$', '\\$').
                                   replace('"', '\\"'))
                                   for v in values)

        def join_paths_single_var(values):
            """
            semicolon-separated list of dirs:
            e.g: set(LIBFOO_INCLUDE_DIR "/path/to/included/dir;/path/to/included/dir2")
            """
            return '"%s"' % ";".join(p.replace('\\', '/').replace('$', '\\$') for p in values)

        self.include_paths = join_paths(cpp_info.includedirs)
        self.lib_paths = join_paths(cpp_info.libdirs)
        self.res_paths = join_paths(cpp_info.resdirs)
        self.bin_paths = join_paths(cpp_info.bindirs)
        self.build_paths = join_paths(cpp_info.builddirs)
        self.src_paths = join_paths(cpp_info.srcdirs)
        self.framework_paths = join_paths(cpp_info.frameworkdirs)
        self.libs = join_flags(" ", cpp_info.libs)
        self.system_libs = join_flags(" ", cpp_info.system_libs)
        self.frameworks = join_flags(" ", cpp_info.frameworks)
        self.defines = join_defines(cpp_info.defines, "-D")
        self.compile_definitions = join_defines(cpp_info.defines)

        # For modern CMake targets we need to prepare a list to not
        # loose the elements in the list by replacing " " with ";". Example "-framework Foundation"
        # Issue: #1251
        self.cxxflags_list = join_flags(";", cpp_info.cxxflags)
        self.cflags_list = join_flags(";", cpp_info.cflags)

        # linker flags without magic: trying to mess with - and / =>
        # https://github.com/conan-io/conan/issues/8811
        # frameworks should be declared with cppinfo.frameworks not "-framework Foundation"
        self.sharedlinkflags_list = '"{}"'.format(join_flags(";", cpp_info.sharedlinkflags)) \
            if cpp_info.sharedlinkflags else ''
        self.exelinkflags_list = '"{}"'.format(join_flags(";", cpp_info.exelinkflags)) \
            if cpp_info.exelinkflags else ''

        self.objects_list = join_paths(cpp_info.objects)

        build_modules = cpp_info.get_property("cmake_build_modules") or []
        self.build_modules_paths = join_paths(build_modules)
