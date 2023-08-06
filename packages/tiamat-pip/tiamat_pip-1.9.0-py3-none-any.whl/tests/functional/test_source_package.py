import os
import logging
import pytest
from tests.support.helpers import TiamatPipProject
from tests.conftest import CODE_ROOT

log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def project(request, tmp_path_factory):
    name = "tiamat-install-from-dir"
    requirements = []
    instance = TiamatPipProject(
        name=name,
        path=tmp_path_factory.mktemp(name, numbered=False),
        one_dir=request.config.getoption("--singlebin") is False,
        requirements=requirements,
    )
    with instance:
        if os.environ.get("CI_RUN", "0") == "0":
            instance.copy_generated_project_to_temp()
        try:
            log.info("Using built Project: %s", instance)
            yield instance
        finally:
            instance.delete_pypath()


def test_source_checkout_path_install(project):
    ret = project.run("pip", "install", str(CODE_ROOT))
    assert ret.exitcode == 0


def test_git_source_install(project):
    installed_packages = project.get_installed_packages(include_frozen=True)
    assert "istr" not in installed_packages
    ret = project.run("pip", "install", "git+https://github.com/saltstack/istr.git")
    assert ret.exitcode == 0
    installed_packages = project.get_installed_packages(include_frozen=True)
    assert "istr" in installed_packages
