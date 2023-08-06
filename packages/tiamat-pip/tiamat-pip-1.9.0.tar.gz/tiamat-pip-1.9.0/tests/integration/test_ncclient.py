import pytest

from tests.conftest import Package
from tests.conftest import package_ids


@pytest.fixture(
    scope="module",
    params=[
        Package(name="ncclient", version="0.6.4", upgrade="0.6.13"),
    ],
    ids=package_ids,
)
def package(request):
    return request.param


def test_package(project, package, package_type):
    installed_packages = project.get_installed_packages(
        include_frozen=package_type == "builtin"
    )
    assert package.name in installed_packages
    assert installed_packages[package.name] == package.version

    if package_type == "pypath":
        store = project.get_store()
        assert package.name in store
        assert store[package.name].version == package.version

    ret = project.run(
        "pip",
        "install",
        f"--no-binary={package.name}",
        f"{package.name}=={package.upgrade}",
    )
    assert ret.exitcode == 0
    installed_packages = project.get_installed_packages()
    assert package.name in installed_packages
    assert installed_packages[package.name] == package.upgrade
    store = project.get_store()
    assert package.name in store
    assert store[package.name].version == package.upgrade

    ret = project.run("pip", "uninstall", "-y", package.name)
    assert ret.exitcode == 0
    assert "as it is not installed" not in ret.stderr

    installed_packages = project.get_installed_packages()
    assert package.name not in installed_packages

    if package_type == "builtin":
        # We can uninstall the upgrade, but not the builtin
        installed_packages = project.get_installed_packages(
            include_frozen=package_type == "builtin"
        )
        assert package.name in installed_packages

        ret = project.run("pip", "uninstall", "-y", package.name)
        assert "as it is not installed" in ret.stderr
    else:
        store = project.get_store()
        assert package.name not in store
        if package.altname:
            assert package.altname not in store
