import os
import argparse
import sys
import signal
from argparse import ArgumentError
from conans.client.command import (Command as Command_co, SmartFormatter, OnceArgument, 
                                    _add_profile_arguments,
                                   _PATH_HELP, _INSTALL_FOLDER_HELP, 
                                   _SOURCE_FOLDER_HELP, _BUILD_FOLDER_HELP, 
                                   _PATTERN_REF_OR_PREF_HELP, _QUERY_HELP)
from sense2 import __version__ as client_version
from conans.client.conf.config_installer import is_config_install_scheduled
from conans.util.log import logger
from conans.util.files import exception_message_safe
from sense2.client.sense2_api import Sense2, default_manifest_folder, _make_abs_path, ProfileData
from conans.errors import ConanException, ConanInvalidConfiguration, NoRemoteAvailable, \
    ConanMigrationError, ConanInvalidSystemRequirements
from conans.cli.exit_codes import SUCCESS, ERROR_MIGRATION, ERROR_GENERAL, USER_CTRL_C, \
    ERROR_SIGTERM, USER_CTRL_BREAK, ERROR_INVALID_CONFIGURATION, ERROR_INVALID_SYSTEM_REQUIREMENTS
from conans.model.ref import ConanFileReference, PackageReference, get_reference_fields, \
    check_valid_ref
from conans.client.output import Color
from conans.client.cmd.uploader import UPLOAD_POLICY_FORCE, \
    UPLOAD_POLICY_NO_OVERWRITE, UPLOAD_POLICY_NO_OVERWRITE_RECIPE, UPLOAD_POLICY_SKIP

class Command(Command_co):
    """A single command of the conan application, with all the first level commands. Manages the
    parsing of parameters and delegates functionality in collaborators. It can also show the
    help of the tool.
    """
    def __init__(self, sense2_api):
        assert isinstance(sense2_api, Sense2)
        self._conan = sense2_api
        self._out = sense2_api.out


    def install_deb(self, *args):
        """
        Calls your local conanfile.py 'install_deb()' method.
        """

        parser = argparse.ArgumentParser(description=self.build.__doc__,
                                         prog="sense2 install_deb",
                                         formatter_class=SmartFormatter)
        parser.add_argument("conanfile_path", help=_PATH_HELP)
        args = parser.parse_args(*args)
        self._warn_python_version()
        
        return self._conan.install_deb(conanfile_path=args.conanfile_path)

    def install_docker(self, *args):
        """
        Calls your local conanfile.py 'install_docker()' method.
        """

        parser = argparse.ArgumentParser(description=self.build.__doc__,
                                         prog="sense2 install_docker",
                                         formatter_class=SmartFormatter)
        parser.add_argument("conanfile_path", help=_PATH_HELP)

        args = parser.parse_args(*args)

        self._warn_python_version()
        
        return self._conan.install_docker(conanfile_path=args.conanfile_path)

    def install_sense_system(self, *args):
        """
        Calls your local conanfile.py 'install_sense_system()' method.
        """

        parser = argparse.ArgumentParser(description=self.build.__doc__,
                                         prog="sense2 install_sense_system",
                                         formatter_class=SmartFormatter)
        parser.add_argument("conanfile_path", help=_PATH_HELP)

        args = parser.parse_args(*args)

        self._warn_python_version()
        
        return self._conan.install_sense_system(conanfile_path=args.conanfile_path)
    
    def deb(self, *args):
        """
        Calls your local conanfile.py 'deb()' method.

        This command works in the user space and it will copy artifacts from
        the --build-folder and --source-folder folder to the --package-folder
        one.  It won't create a new package in the local cache, if you want to
        do it, use 'conan create' or 'conan export-pkg' after a 'conan build'
        command.
        """
        parser = argparse.ArgumentParser(description=self.package.__doc__,
                                         prog="sense2 deb",
                                         formatter_class=SmartFormatter)
        parser.add_argument("path", help=_PATH_HELP)
        parser.add_argument("-bf", "--build-folder", action=OnceArgument, help=_BUILD_FOLDER_HELP)
        parser.add_argument("-pf", "--deb-folder", action=OnceArgument,
                            help="folder to install the package. Defaulted to the "
                                 "'{build_folder}/package' folder. A relative path can be specified"
                                 " (relative to the current directory). Also an absolute path"
                                 " is allowed.")
        parser.add_argument("-sf", "--source-folder", action=OnceArgument, help=_SOURCE_FOLDER_HELP)
        parser.add_argument("-if", "--install-folder", action=OnceArgument,
                            help=_INSTALL_FOLDER_HELP)
        
        args = parser.parse_args(*args)
        try:
            if "@" in args.path and ConanFileReference.loads(args.path):
                raise ArgumentError(None,
                                    "'sense2 deb' doesn't accept a reference anymore. "
                                    "The path parameter should be a conanfile.py or a folder "
                                    "containing one. If you were using the 'conan package' "
                                    "command for development purposes we recommend to use "
                                    "the local development commands: 'conan build' + "
                                    "'conan package' and finally 'conan create' to regenerate the "
                                    "package, or 'conan export_package' to store the already built "
                                    "binaries in the local cache without rebuilding them.")
        except ConanException:
            pass

        self._warn_python_version()
        return self._conan.deb(path=args.path,
                                build_folder=args.build_folder,
                                deb_folder=args.deb_folder,
                                source_folder=args.source_folder,
                                install_folder=args.install_folder)
    
    def upload_deb(self, *args):
        """
        Uploads a recipe and binary packages to a remote.

        If no remote is specified, the first configured remote (by default conan-center, use
        'conan remote list' to list the remotes) will be used.
        """
        parser = argparse.ArgumentParser(description=self.upload.__doc__,
                                         prog="sense2 upload_deb",
                                         formatter_class=SmartFormatter)
        parser.add_argument('pattern_or_reference', help=_PATTERN_REF_OR_PREF_HELP)
        parser.add_argument("-p", "--package", default=None,
                            help="Package ID [DEPRECATED: use full reference instead]",
                            action=OnceArgument)
        parser.add_argument('-q', '--query', default=None, action=OnceArgument,
                            help="Only upload packages matching a specific query. " + _QUERY_HELP)
        parser.add_argument("-r", "--remote", action=OnceArgument,
                            help='upload to this specific remote')
        parser.add_argument("--all", action='store_true', default=True,
                            help='Upload both package recipe and packages')
        parser.add_argument("--skip-upload", action='store_true', default=False,
                            help='Do not upload anything, just run the checks and the compression')
        parser.add_argument("--force", action='store_true', default=False,
                            help='Ignore checks before uploading the recipe: it will bypass missing'
                                 ' fields in the scm attribute and it will override remote recipe'
                                 ' with local regardless of recipe date')
        parser.add_argument("--check", action='store_true', default=False,
                            help='Perform an integrity check, using the manifests, before upload')
        parser.add_argument('-c', '--confirm', default=False, action='store_true',
                            help='Upload all matching recipes without confirmation')
        parser.add_argument('--retry', default=None, type=int, action=OnceArgument,
                            help="In case of fail retries to upload again the specified times.")
        parser.add_argument('--retry-wait', default=None, type=int, action=OnceArgument,
                            help='Waits specified seconds before retry again')
        parser.add_argument("-no", "--no-overwrite", nargs="?", type=str, choices=["all", "recipe"],
                            action=OnceArgument, const="all",
                            help="Uploads package only if recipe is the same as the remote one")
        parser.add_argument("-j", "--json", default=None, action=OnceArgument,
                            help='json file path where the upload information will be written to')
        parser.add_argument("--parallel", action='store_true', default=False,
                            help='Upload files in parallel using multiple threads. '
                                 'The default number of launched threads is set to the value of '
                                 'cpu_count and can be configured using the CONAN_CPU_COUNT '
                                 'environment variable or defining cpu_count in conan.conf')

        args = parser.parse_args(*args)

        try:
            pref = PackageReference.loads(args.pattern_or_reference, validate=True)
        except ConanException:
            reference = args.pattern_or_reference
            package_id = args.package

            if package_id:
                self._out.warn("Usage of `--package` argument is deprecated."
                               " Use a full reference instead: "
                               "`sense2 upload_deb [...] {}:{}`".format(reference, package_id))

            if args.query and package_id:
                raise ConanException("'--query' argument cannot be used together with '--package'")
        else:
            reference = repr(pref.ref)
            package_id = "{}#{}".format(pref.id, pref.revision) if pref.revision else pref.id

            if args.package:
                raise ConanException("Use a full package reference (preferred) or the `--package`"
                                     " command argument, but not both.")
            if args.query:
                raise ConanException("'--query' argument cannot be used together with "
                                     "full reference")

        if args.force and args.no_overwrite:
            raise ConanException("'--no-overwrite' argument cannot be used together with '--force'")
        if args.force and args.skip_upload:
            raise ConanException("'--skip-upload' argument cannot be used together with '--force'")
        if args.no_overwrite and args.skip_upload:
            raise ConanException("'--skip-upload' argument cannot be used together "
                                 "with '--no-overwrite'")

        self._warn_python_version()

        if args.force:
            policy = UPLOAD_POLICY_FORCE
        elif args.no_overwrite == "all":
            policy = UPLOAD_POLICY_NO_OVERWRITE
        elif args.no_overwrite == "recipe":
            policy = UPLOAD_POLICY_NO_OVERWRITE_RECIPE
        elif args.skip_upload:
            policy = UPLOAD_POLICY_SKIP
        else:
            policy = None

        info = None
        try:
            info = self._conan.upload_deb(pattern=reference, package=package_id,
                                      query=args.query, remote_name=args.remote,
                                      all_packages=args.all, policy=policy,
                                      confirm=args.confirm, retry=args.retry,
                                      retry_wait=args.retry_wait, integrity_check=args.check,
                                      parallel_upload=args.parallel)

        except ConanException as exc:
            info = exc.info
            raise
        finally:
            if args.json and info:
                self._outputer.json_output(info, args.json, os.getcwd())

      
    # def deploy_deb(self, *args):
    #     """
    #     Calls your local conanfile.py 'install_sense_system()' method.
    #     """
    #     parser = argparse.ArgumentParser(description=self.build.__doc__,
    #                                      prog="sense2 install_sense_system",
    #                                      formatter_class=SmartFormatter)
    #     parser.add_argument("conanfile_path", help=_PATH_HELP)
    #     args = parser.parse_args(*args)
    #     self._warn_python_version()
        
    #     return self._conan.deploy_deb(conanfile_path=args.conanfile_path)

    # def set_source(self, *args):
    #     """
    #     Calls your local conanfile.py 'set_source()' method.
    #     """

    #     parser = argparse.ArgumentParser(description=self.build.__doc__,
    #                                      prog="sense2 set_source",
    #                                      formatter_class=SmartFormatter)
    #     parser.add_argument("path", help=_PATH_HELP)
    #     parser.add_argument("-sf", "--source-folder", action=OnceArgument, help=_SOURCE_FOLDER_HELP)

    #     args = parser.parse_args(*args)

    #     self._warn_python_version()
        
    #     return self._conan.set_source(conanfile_path=args.path, source_folder=args.source_folder)
 
    def _show_help(self):
        """
        Prints a summary of all commands.
        """
        grps = [("Consumer commands", ("install", "config", "get", "info", "search")),
                ("Creator commands", ("new", "create", "upload", "export", "export-pkg", "test")),
                ("Package development commands", ("source", "build", "package", "editable",
                                                  "workspace")),
                ("deb development commands", ("install_sense_system", "deb", 
                                              "install_deb", "install_docker",
                                              "upload_deb")),
                ("Misc commands", ("profile", "remote", "user", "imports", "copy", "remove",
                                   "alias", "download", "inspect", "help", "lock", "frogarian"))]

        def check_all_commands_listed():
            """Keep updated the main directory, raise if don't"""
            all_commands = self._commands()
            all_in_grps = [command for _, command_list in grps for command in command_list]
            if set(all_in_grps) != set(all_commands):
                diff = set(all_commands) - set(all_in_grps)
                raise Exception("Some command is missing in the main help: %s" % ",".join(diff))
            return all_commands

        commands = check_all_commands_listed()
        max_len = max((len(c) for c in commands)) + 1
        fmt = '  %-{}s'.format(max_len)

        for group_name, comm_names in grps:
            self._out.writeln(group_name, Color.BRIGHT_MAGENTA)
            for name in comm_names:
                # future-proof way to ensure tabular formatting
                self._out.write(fmt % name, Color.GREEN)

                # Help will be all the lines up to the first empty one
                docstring_lines = commands[name].__doc__.split('\n')
                start = False
                data = []
                for line in docstring_lines:
                    line = line.strip()
                    if not line:
                        if start:
                            break
                        start = True
                        continue
                    data.append(line)

                import textwrap
                txt = textwrap.fill(' '.join(data), 80, subsequent_indent=" "*(max_len+2))
                self._out.writeln(txt)

        self._out.writeln("")
        self._out.writeln('Sense2 commands. Type "sense2 <command> -h" for help', Color.BRIGHT_YELLOW)   
    

    def upload(self, *args):
        """
        Uploads a recipe and binary packages to a remote.

        If no remote is specified, the first configured remote (by default conan-center, use
        'conan remote list' to list the remotes) will be used.
        """
        parser = argparse.ArgumentParser(description=self.upload.__doc__,
                                         prog="sense2 upload",
                                         formatter_class=SmartFormatter)
        parser.add_argument('pattern_or_reference', help=_PATTERN_REF_OR_PREF_HELP)
        parser.add_argument("-p", "--package", default=None,
                            help="Package ID [DEPRECATED: use full reference instead]",
                            action=OnceArgument)
        parser.add_argument('-q', '--query', default=None, action=OnceArgument,
                            help="Only upload packages matching a specific query. " + _QUERY_HELP)
        parser.add_argument("-r", "--remote", action=OnceArgument,
                            help='upload to this specific remote')
        parser.add_argument("--all", action='store_true', default=True,
                            help='Upload both package recipe and packages')
        parser.add_argument("--skip-upload", action='store_true', default=False,
                            help='Do not upload anything, just run the checks and the compression')
        parser.add_argument("--force", action='store_true', default=False,
                            help='Ignore checks before uploading the recipe: it will bypass missing'
                                 ' fields in the scm attribute and it will override remote recipe'
                                 ' with local regardless of recipe date')
        parser.add_argument("--check", action='store_true', default=False,
                            help='Perform an integrity check, using the manifests, before upload')
        parser.add_argument('-c', '--confirm', default=False, action='store_true',
                            help='Upload all matching recipes without confirmation')
        parser.add_argument('--retry', default=None, type=int, action=OnceArgument,
                            help="In case of fail retries to upload again the specified times.")
        parser.add_argument('--retry-wait', default=None, type=int, action=OnceArgument,
                            help='Waits specified seconds before retry again')
        parser.add_argument("-no", "--no-overwrite", nargs="?", type=str, choices=["all", "recipe"],
                            action=OnceArgument, const="all",
                            help="Uploads package only if recipe is the same as the remote one")
        parser.add_argument("-j", "--json", default=None, action=OnceArgument,
                            help='json file path where the upload information will be written to')
        parser.add_argument("--parallel", action='store_true', default=False,
                            help='Upload files in parallel using multiple threads. '
                                 'The default number of launched threads is set to the value of '
                                 'cpu_count and can be configured using the CONAN_CPU_COUNT '
                                 'environment variable or defining cpu_count in conan.conf')

        args = parser.parse_args(*args)

        try:
            pref = PackageReference.loads(args.pattern_or_reference, validate=True)
        except ConanException:
            reference = args.pattern_or_reference
            package_id = args.package

            if package_id:
                self._out.warn("Usage of `--package` argument is deprecated."
                               " Use a full reference instead: "
                               "`conan upload [...] {}:{}`".format(reference, package_id))

            if args.query and package_id:
                raise ConanException("'--query' argument cannot be used together with '--package'")
        else:
            reference = repr(pref.ref)
            package_id = "{}#{}".format(pref.id, pref.revision) if pref.revision else pref.id

            if args.package:
                raise ConanException("Use a full package reference (preferred) or the `--package`"
                                     " command argument, but not both.")
            if args.query:
                raise ConanException("'--query' argument cannot be used together with "
                                     "full reference")

        if args.force and args.no_overwrite:
            raise ConanException("'--no-overwrite' argument cannot be used together with '--force'")
        if args.force and args.skip_upload:
            raise ConanException("'--skip-upload' argument cannot be used together with '--force'")
        if args.no_overwrite and args.skip_upload:
            raise ConanException("'--skip-upload' argument cannot be used together "
                                 "with '--no-overwrite'")

        self._warn_python_version()

        if args.force:
            policy = UPLOAD_POLICY_FORCE
        elif args.no_overwrite == "all":
            policy = UPLOAD_POLICY_NO_OVERWRITE
        elif args.no_overwrite == "recipe":
            policy = UPLOAD_POLICY_NO_OVERWRITE_RECIPE
        elif args.skip_upload:
            policy = UPLOAD_POLICY_SKIP
        else:
            policy = None

        info = None
        try:
            info = self._conan.upload(pattern=reference, package=package_id,
                                      query=args.query, remote_name=args.remote,
                                      all_packages=args.all, policy=policy,
                                      confirm=args.confirm, retry=args.retry,
                                      retry_wait=args.retry_wait, integrity_check=args.check,
                                      parallel_upload=args.parallel)

        except ConanException as exc:
            info = exc.info
            raise
        finally:
            if args.json and info:
                self._outputer.json_output(info, args.json, os.getcwd())

    def export_pkg(self, *args):
        """
        Exports a recipe, then creates a package from local source and build folders.

        If '--package-folder' is provided it will copy the files from there, otherwise, it
        will execute package() method over '--source-folder' and '--build-folder' to create
        the binary package.
        """

        parser = argparse.ArgumentParser(description=self.export_pkg.__doc__,
                                         prog="sense2 export-pkg",
                                         formatter_class=SmartFormatter)
        parser.add_argument("path", help=_PATH_HELP)
        parser.add_argument("reference", nargs='?', default=None,
                            help="user/channel or pkg/version@user/channel "
                                 "(if name and version are not declared in the "
                                 "conanfile.py)")

        parser.add_argument("-bf", "--build-folder", action=OnceArgument, help=_BUILD_FOLDER_HELP)
        parser.add_argument('-f', '--force', default=False, action='store_true',
                            help='Overwrite existing package if existing')
        parser.add_argument("-if", "--install-folder", action=OnceArgument,
                            help=_INSTALL_FOLDER_HELP + " If these files are found in the specified"
                            " folder and any of '-e', '-o', '-pr' or '-s' arguments are used, it "
                            "will raise an error.")
        parser.add_argument("-pf", "--package-folder", action=OnceArgument,
                            help="folder containing a locally created package. If a value is given,"
                                 " it won't call the recipe 'package()' method, and will run a copy"
                                 " of the provided folder.")
        parser.add_argument("-sf", "--source-folder", action=OnceArgument, help=_SOURCE_FOLDER_HELP)
        parser.add_argument("-j", "--json", default=None, action=OnceArgument,
                            help='Path to a json file where the install information will be '
                            'written')
        parser.add_argument("-l", "--lockfile", action=OnceArgument,
                            help="Path to a lockfile.")
        parser.add_argument("--lockfile-out", action=OnceArgument,
                            help="Filename of the updated lockfile")
        parser.add_argument("--ignore-dirty", default=False, action='store_true',
                            help='When using the "scm" feature with "auto" values, capture the'
                                 ' revision and url even if there are uncommitted changes')
        _add_profile_arguments(parser)

        args = parser.parse_args(*args)
        self._warn_python_version()
        self._check_lockfile_args(args)

        name, version, user, channel, _ = get_reference_fields(args.reference,
                                                               user_channel_input=True)
        cwd = os.getcwd()
        info = None

        try:
            profile_build = ProfileData(profiles=args.profile_build, settings=args.settings_build,
                                        options=args.options_build, env=args.env_build,
                                        conf=args.conf_build)
            # TODO: 2.0 create profile_host object here to avoid passing a lot of arguments
            #       to the API

            info = self._conan.export_pkg(conanfile_path=args.path,
                                          name=name,
                                          version=version,
                                          source_folder=args.source_folder,
                                          build_folder=args.build_folder,
                                          package_folder=args.package_folder,
                                          install_folder=args.install_folder,
                                          profile_names=args.profile_host,
                                          env=args.env_host,
                                          settings=args.settings_host,
                                          options=args.options_host,
                                          conf=args.conf_host,
                                          profile_build=profile_build,
                                          force=args.force,
                                          user=user,
                                          channel=channel,
                                          lockfile=args.lockfile,
                                          lockfile_out=args.lockfile_out,
                                          ignore_dirty=args.ignore_dirty)
        except ConanException as exc:
            info = exc.info
            raise
        finally:
            if args.json and info:
                self._outputer.json_output(info, args.json, cwd)

    def run(self, *args):
        """HIDDEN: entry point for executing commands, dispatcher to class
        methods
        """
        ret_code = SUCCESS
        try:
            try:
                command = args[0][0]
            except IndexError:  # No parameters
                self._show_help()
                return False
            try:
                commands = self._commands()
                method = commands[command]
            except KeyError as exc:
                if command in ["-v", "--version"]:
                    self._out.success("Sense2 version %s" % client_version)
                    return False

                self._warn_python_version()

                if command in ["-h", "--help"]:
                    self._show_help()
                    return False

                self._out.writeln(
                    "'%s' is not a Sense2 command. See 'sense2 --help'." % command)
                self._out.writeln("")
                self._print_similar(command)
                raise ConanException("Unknown command %s" % str(exc))

            if (command != "config" or
               (command == "config" and len(args[0]) > 1 and args[0][1] != "install")) and \
               is_config_install_scheduled(self._conan):
                self._conan.config_install(None, None)

            method(args[0][1:])
        except KeyboardInterrupt as exc:
            logger.error(exc)
            ret_code = SUCCESS
        except SystemExit as exc:
            if exc.code != 0:
                logger.error(exc)
                self._out.error("Exiting with code: %d" % exc.code)
            ret_code = exc.code
        except ConanInvalidConfiguration as exc:
            ret_code = ERROR_INVALID_CONFIGURATION
            self._out.error(exc)
        except ConanInvalidSystemRequirements as exc:
            ret_code = ERROR_INVALID_SYSTEM_REQUIREMENTS
            self._out.error(exc)
        except ConanException as exc:
            ret_code = ERROR_GENERAL
            self._out.error(exc)
        except Exception as exc:
            import traceback
            print(traceback.format_exc())
            ret_code = ERROR_GENERAL
            msg = exception_message_safe(exc)
            self._out.error(msg)

        return ret_code

def main(args):
    """ main entry point of the conan application, using a Command to
    parse parameters

    Exit codes for conan command:

        0: Success (done)
        1: General ConanException error (done)
        2: Migration error
        3: Ctrl+C
        4: Ctrl+Break
        5: SIGTERM
        6: Invalid configuration (done)
    """
    try:
        sense2_api, _, _ = Sense2.factory()
    except ConanMigrationError:  # Error migrating
        sys.exit(ERROR_MIGRATION)
    except ConanException as e:
        sys.stderr.write("Error in Conan initialization: {}".format(e))
        sys.exit(ERROR_GENERAL)

    def ctrl_c_handler(_, __):
        print('You pressed Ctrl+C!')
        sys.exit(USER_CTRL_C)

    def sigterm_handler(_, __):
        print('Received SIGTERM!')
        sys.exit(ERROR_SIGTERM)

    def ctrl_break_handler(_, __):
        print('You pressed Ctrl+Break!')
        sys.exit(USER_CTRL_BREAK)

    signal.signal(signal.SIGINT, ctrl_c_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    if sys.platform == 'win32':
        signal.signal(signal.SIGBREAK, ctrl_break_handler)

    command = Command(sense2_api)
    error = command.run(args)
    sys.exit(error)
