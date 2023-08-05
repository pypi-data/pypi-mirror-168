import pytest
from conans.test.assets.genconanfile import GenConanfile
from conans.test.utils.tools import TestClient


@pytest.fixture(scope="module")
def build_all():
    """ Build a simple graph to test --build option

        foobar <- bar <- foo
               <--------|

        All packages are built from sources to keep a cache.
    :return: TestClient instance
    """
    client = TestClient()
    client.save({"conanfile.py": GenConanfile().with_setting("build_type")})
    client.run("export . foo/1.0@user/testing")
    client.save({"conanfile.py": GenConanfile().with_require("foo/1.0@user/testing")
                .with_setting("build_type")})
    client.run("export . bar/1.0@user/testing")
    client.save({"conanfile.py": GenConanfile().with_require("foo/1.0@user/testing")
                .with_require("bar/1.0@user/testing")
                .with_setting("build_type")})
    client.run("export . foobar/1.0@user/testing")
    client.run("install foobar/1.0@user/testing --build")

    return client


def check_if_build_from_sources(refs_modes, output):
    for ref, mode in refs_modes.items():
        if mode == "Build":
            assert "{}/1.0@user/testing: Forced build from source".format(ref) in output
        else:
            assert "{}/1.0@user/testing: Forced build from source".format(ref) not in output


def test_install_build_single(build_all):
    """ When only --build=<ref> is passed, only <ref> must be built
    """
    build_all.run("install foobar/1.0@user/testing --build=foo")

    assert "bar/1.0@user/testing:7839863d5a059fc6579f28026763e1021268c55e - Cache" in build_all.out
    assert "foo/1.0@user/testing:4024617540c4f240a6a5e8911b0de9ef38a11a72 - Build" in build_all.out
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - Cache" in build_all.out
    assert "foo/1.0@user/testing: Forced build from source" in build_all.out
    assert "bar/1.0@user/testing: Forced build from source" not in build_all.out
    assert "foobar/1.0@user/testing: Forced build from source" not in build_all.out
    assert "No package matching" not in build_all.out


def test_install_build_double(build_all):
    """ When both --build=<ref1> and --build=<ref2> are passed, only both should be built
    """
    build_all.run("install foobar/1.0@user/testing --build=foo --build=bar")

    assert "bar/1.0@user/testing:7839863d5a059fc6579f28026763e1021268c55e - Build" in build_all.out
    assert "foo/1.0@user/testing:4024617540c4f240a6a5e8911b0de9ef38a11a72 - Build" in build_all.out
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - Cache" in build_all.out
    assert "foo/1.0@user/testing: Forced build from source" in build_all.out
    assert "bar/1.0@user/testing: Forced build from source" in build_all.out
    assert "foobar/1.0@user/testing: Forced build from source" not in build_all.out
    assert "No package matching" not in build_all.out


@pytest.mark.parametrize("build_arg,mode", [("--build", "Build"),
                                            ("--build=", "Cache"),
                                            ("--build=*", "Build")])
def test_install_build_only(build_arg, mode, build_all):
    """ When only --build is passed, all packages must be built from sources
        When only --build= is passed, it's considered an error
        When only --build=* is passed, all packages must be built from sources
    """
    build_all.run("install foobar/1.0@user/testing {}".format(build_arg))

    assert "bar/1.0@user/testing:7839863d5a059fc6579f28026763e1021268c55e - {}".format(mode) in build_all.out
    assert "foo/1.0@user/testing:4024617540c4f240a6a5e8911b0de9ef38a11a72 - {}".format(mode) in build_all.out
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - {}".format(mode) in build_all.out

    if "Build" == mode:
        assert "foo/1.0@user/testing: Forced build from source" in build_all.out
        assert "bar/1.0@user/testing: Forced build from source" in build_all.out
        assert "foobar/1.0@user/testing: Forced build from source" in build_all.out
        assert "No package matching" not in build_all.out
    else:
        assert "foo/1.0@user/testing: Forced build from source" not in build_all.out
        assert "bar/1.0@user/testing: Forced build from source" not in build_all.out
        assert "foobar/1.0@user/testing: Forced build from source" not in build_all.out
        assert "No package matching" in build_all.out


@pytest.mark.parametrize("build_arg,bar,foo,foobar", [("--build", "Cache", "Build", "Cache"),
                                                      ("--build=", "Cache", "Build", "Cache"),
                                                      ("--build=*", "Build", "Build", "Build")])
def test_install_build_all_with_single(build_arg, bar, foo, foobar, build_all):
    """ When --build is passed with another package, only the package must be built from sources.
        When --build= is passed with another package, only the package must be built from sources.
        When --build=* is passed with another package, all packages must be built from sources.
    """
    build_all.run("install foobar/1.0@user/testing --build=foo {}".format(build_arg))

    assert "bar/1.0@user/testing:7839863d5a059fc6579f28026763e1021268c55e - {}".format(bar) in build_all.out
    assert "foo/1.0@user/testing:4024617540c4f240a6a5e8911b0de9ef38a11a72 - {}".format(foo) in build_all.out
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - {}".format(foobar) in build_all.out
    check_if_build_from_sources({"foo": foo, "bar": bar, "foobar": foobar}, build_all.out)


@pytest.mark.parametrize("build_arg,bar,foo,foobar", [("--build", "Cache", "Cache", "Cache"),
                                                      ("--build=", "Cache", "Cache", "Cache"),
                                                      ("--build=*", "Build", "Cache", "Build")])
def test_install_build_all_with_single_skip(build_arg, bar, foo, foobar, build_all):
    """ When --build is passed with a skipped package, not all packages must be built from sources.
        When --build= is passed with another package, only the package must be built from sources.
        When --build=* is passed with another package, not all packages must be built from sources.

        The arguments order matter, that's why we need to run twice.
    """
    for argument in ["--build=!foo {}".format(build_arg),
                     "{} --build=!foo".format(build_arg)]:
        build_all.run("install foobar/1.0@user/testing {}".format(argument))
        assert "bar/1.0@user/testing:7839863d5a059fc6579f28026763e1021268c55e - {}".format(bar) in build_all.out
        assert "foo/1.0@user/testing:4024617540c4f240a6a5e8911b0de9ef38a11a72 - {}".format(foo) in build_all.out
        assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - {}".format(foobar) in build_all.out
        check_if_build_from_sources({"foo": foo, "bar": bar, "foobar": foobar}, build_all.out)


@pytest.mark.parametrize("build_arg,bar,foo,foobar", [("--build", "Cache", "Cache", "Cache"),
                                                      ("--build=", "Cache", "Cache", "Cache"),
                                                      ("--build=*", "Cache", "Cache", "Build")])
def test_install_build_all_with_double_skip(build_arg, bar, foo, foobar, build_all):
    """ When --build is passed with a skipped package, not all packages must be built from sources.
        When --build= is passed with another package, only the package must be built from sources.
        When --build=* is passed with another package, not all packages must be built from sources.

        The arguments order matter, that's why we need to run twice.
    """
    for argument in ["--build=!foo --build=!bar {}".format(build_arg),
                     "{} --build=!foo --build=!bar".format(build_arg)]:
        build_all.run("install foobar/1.0@user/testing {}".format(argument))

        assert "bar/1.0@user/testing:7839863d5a059fc6579f28026763e1021268c55e - {}".format(bar) in build_all.out
        assert "foo/1.0@user/testing:4024617540c4f240a6a5e8911b0de9ef38a11a72 - {}".format(foo) in build_all.out
        assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - {}".format(foobar) in build_all.out


def test_report_matches(build_all):
    """ When a wrong reference is passed to be build, an error message should be shown
    """
    build_all.run("install foobar/1.0@user/testing --build=* --build=baz")
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - Build" in build_all.out
    assert "No package matching 'baz' pattern found." in build_all.out

    build_all.run("install foobar/1.0@user/testing --build=* --build=!baz")
    assert "No package matching 'baz' pattern found." in build_all.out
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - Build" in build_all.out

    build_all.run("install foobar/1.0@user/testing --build=* --build=!baz --build=blah")
    assert "No package matching 'blah' pattern found." in build_all.out
    assert "No package matching 'baz' pattern found." in build_all.out
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - Build" in build_all.out

    build_all.run("install foobar/1.0@user/testing --build=* --build=!baz --build=!blah")
    assert "No package matching 'blah' pattern found." in build_all.out
    assert "No package matching 'baz' pattern found." in build_all.out
    assert "foobar/1.0@user/testing:89636fbae346e3983af2dd63f2c5246505e74be7 - Build" in build_all.out
