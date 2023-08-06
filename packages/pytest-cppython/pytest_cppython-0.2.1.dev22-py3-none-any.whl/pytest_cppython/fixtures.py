"""Direct Fixtures
"""

from pathlib import Path
from typing import cast

import pytest
from cppython_core.schema import (
    PEP621,
    CPPythonData,
    InterfaceConfiguration,
    ProjectConfiguration,
    ProviderConfiguration,
)

from pytest_cppython.fixture_data.configuration import (
    interface_config_test_list,
    provider_config_test_list,
)
from pytest_cppython.fixture_data.cppython import cppython_test_list
from pytest_cppython.fixture_data.pep621 import pep621_test_list


class CPPythonFixtures:
    """Fixtures available to CPPython test classes"""

    @pytest.fixture(name="workspace")
    def fixture_workspace(self, tmp_path_factory: pytest.TempPathFactory) -> ProjectConfiguration:
        """Fixture that creates a project configuration at 'workspace/test_project/pyproject.toml'

        Args:
            tmp_path_factory: Factory for centralized temporary directories

        Returns:
            A project configuration that has populated a function level temporary directory
        """
        tmp_path = tmp_path_factory.mktemp("workspace-")

        pyproject_path = tmp_path / "test_project"
        pyproject_path.mkdir(parents=True)
        pyproject_file = pyproject_path / "pyproject.toml"
        pyproject_file.write_text("Test Project File", encoding="utf-8")

        configuration = ProjectConfiguration(pyproject_file=pyproject_file, version="0.1.0")
        return configuration

    @pytest.fixture(
        name="pep621",
        scope="session",
        params=pep621_test_list,
    )
    def fixture_pep621(self, request: pytest.FixtureRequest) -> PEP621:
        """Fixture defining all testable variations of PEP621

        Args:
            request: Parameterization list

        Returns:
            PEP621 variant
        """

        return cast(PEP621, request.param)

    @pytest.fixture(
        name="install_path",
        scope="session",
    )
    def fixture_install_path(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        """Creates temporary install location

        Args:
            tmp_path_factory: Factory for centralized temporary directories

        Returns:
            A temporary directory
        """
        path = tmp_path_factory.getbasetemp()
        path.mkdir(parents=True, exist_ok=True)

        return path

    @pytest.fixture(
        name="cppython",
        scope="session",
        params=cppython_test_list,
    )
    def fixture_cppython(self, request: pytest.FixtureRequest, install_path: Path) -> CPPythonData:
        """Fixture defining all testable variations of CPPythonData

        Args:
            request: Parameterization list
            install_path: The temporary install directory

        Returns:
            Variation of CPPython data
        """
        cppython_data = cast(CPPythonData, request.param)

        # Pin the install location to the base temporary directory
        cppython_data.install_path = install_path

        return cppython_data

    @pytest.fixture(
        name="static_pyproject_data",
        scope="session",
    )
    def fixture_static_pyproject_data(self, pep621: PEP621, cppython: CPPythonData) -> tuple[PEP621, CPPythonData]:
        """Collects the static pyproject data as a tuple

        Args:
            pep621: PEP621 variant
            cppython: Variation of CPPython data

        Returns:
            Tuple containing the pep621 and cppython fixture results
        """

        return pep621, cppython

    @pytest.fixture(
        name="provider_configuration",
        scope="session",
        params=provider_config_test_list,
    )
    def fixture_provider_config(self, request: pytest.FixtureRequest) -> ProviderConfiguration:
        """Fixture defining all testable variations of ProviderConfiguration

        Args:
            request: Parameterization list

        Returns:
            Variation of provider configuration data
        """

        return cast(ProviderConfiguration, request.param)

    @pytest.fixture(
        name="interface_configuration",
        scope="session",
        params=interface_config_test_list,
    )
    def fixture_interface_config(self, request: pytest.FixtureRequest) -> InterfaceConfiguration:
        """Fixture defining all testable variations of InterfaceConfiguration

        Args:
            request: Parameterization list

        Returns:
            Variation of interface configuration data
        """

        return cast(InterfaceConfiguration, request.param)
