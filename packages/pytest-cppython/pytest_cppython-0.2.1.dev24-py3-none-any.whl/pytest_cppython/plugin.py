"""Helper fixtures and plugin definitions for pytest
"""

import asyncio
from abc import ABC
from importlib.metadata import entry_points
from pathlib import Path
from typing import Generic

import pytest
from cppython_core.schema import (
    PEP621,
    CPPythonData,
    CPPythonDataResolved,
    GeneratorT,
    InterfaceConfiguration,
    InterfaceT,
    ProjectConfiguration,
    ProviderConfiguration,
    ProviderDataT,
    ProviderT,
    VersionControlT,
)

from pytest_cppython.fixtures import CPPythonFixtures


class PluginTests(CPPythonFixtures):
    """Shared testing information for all plugin test classes"""


class ProviderTests(PluginTests, ABC, Generic[ProviderT, ProviderDataT]):
    """Shared functionality between the different Provider testing categories"""

    @pytest.fixture(name="provider_data", scope="session")
    def fixture_provider_data(self) -> ProviderDataT:
        """A required testing hook that allows ProviderData generation"""
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="provider_type", scope="session")
    def fixture_provider_type(self) -> type[ProviderT]:
        """A required testing hook that allows type generation"""
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="provider_construction_data", scope="session")
    def fixture_provider_construction_data(
        self, provider_type: type[ProviderT], provider_data: ProviderDataT
    ) -> tuple[type[ProviderT], ProviderDataT]:
        """Collects the provider type construction data as a tuple

        Args:
            provider_type: Overridden provider type
            provider_data: Overridden provider data

        Returns:
            Tuple containing the overridden fixture results
        """
        return provider_type, provider_data

    @pytest.fixture(autouse=True, scope="session")
    def _fixture_install_dependency(self, provider_type: type[ProviderT], install_path: Path) -> None:
        """Forces the download to only happen once per test session"""

        path = install_path / provider_type.name()
        path.mkdir(parents=True, exist_ok=True)

        asyncio.run(provider_type.download_tooling(path))

    @pytest.fixture(name="provider")
    def fixture_provider(
        self,
        provider_construction_data: tuple[type[ProviderT], ProviderDataT],
        provider_configuration: ProviderConfiguration,
        static_pyproject_data: tuple[PEP621, CPPythonData],
        workspace: ProjectConfiguration,
    ) -> ProviderT:
        """A hook allowing implementations to override the fixture

        Args:
            provider_construction_data: Provider construction data
            provider_configuration: Provider configuration data
            static_pyproject_data: Generated static project definition
            workspace: Temporary directory defined by a configuration object

        Returns:
            A newly constructed provider
        """

        pep621, cppython = static_pyproject_data
        provider_type, provider_data = provider_construction_data

        modified_project_data = pep621.resolve(workspace)
        modified_cppython_data = cppython.resolve(CPPythonDataResolved, workspace)
        modified_cppython_data = modified_cppython_data.provider_resolve(provider_type)
        modified_provider_data = provider_data.resolve(workspace)

        return provider_type(
            provider_configuration, modified_project_data, modified_cppython_data, modified_provider_data
        )


class ProviderIntegrationTests(ProviderTests[ProviderT, ProviderDataT]):
    """Base class for all provider integration tests that test plugin agnostic behavior"""

    def test_is_downloaded(self, provider: ProviderT) -> None:
        """Verify the provider is downloaded from fixture

        Args:
            provider: A newly constructed provider
        """

        assert provider.tooling_downloaded(provider.cppython.install_path)

    def test_not_downloaded(self, provider_type: type[ProviderT], tmp_path: Path) -> None:
        """Verify the provider can identify an empty tool

        Args:
            provider_type: An input provider type
            tmp_path: A temporary path for the lifetime of the function
        """

        assert not provider_type.tooling_downloaded(tmp_path)

    def test_install(self, provider: ProviderT) -> None:
        """Ensure that the vanilla install command functions

        Args:
            provider: A newly constructed provider
        """
        provider.install()

    def test_update(self, provider: ProviderT) -> None:
        """Ensure that the vanilla update command functions

        Args:
            provider: A newly constructed provider
        """
        provider.update()


class ProviderUnitTests(ProviderTests[ProviderT, ProviderDataT]):
    """Custom implementations of the Provider class should inherit from this class for its tests.
    Base class for all provider unit tests that test plugin agnostic behavior
    """

    def test_plugin_registration(self, provider: ProviderT) -> None:
        """Test the registration with setuptools entry_points

        Args:
            provider: A newly constructed provider
        """
        plugin_entries = entry_points(group=f"cppython.{provider.group()}")
        assert len(plugin_entries) > 0


class InterfaceTests(PluginTests, ABC, Generic[InterfaceT]):
    """Shared functionality between the different Interface testing categories"""

    @pytest.fixture(name="interface_type", scope="session")
    def fixture_interface_type(self) -> type[InterfaceT]:
        """A required testing hook that allows type generation"""
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="interface")
    def fixture_interface(
        self, interface_type: type[InterfaceT], interface_configuration: InterfaceConfiguration
    ) -> InterfaceT:
        """A hook allowing implementations to override the fixture

        Args:
            interface_type: An input interface type
            interface_configuration: Interface configuration data

        Returns:
            A newly constructed interface
        """
        return interface_type(interface_configuration)


class InterfaceIntegrationTests(InterfaceTests[InterfaceT]):
    """Base class for all interface integration tests that test plugin agnostic behavior"""


class InterfaceUnitTests(InterfaceTests[InterfaceT]):
    """Custom implementations of the Interface class should inherit from this class for its tests.
    Base class for all interface unit tests that test plugin agnostic behavior
    """


class GeneratorTests(PluginTests, ABC, Generic[GeneratorT]):
    """Shared functionality between the different Generator testing categories"""

    @pytest.fixture(name="generator_type", scope="session")
    def fixture_generator_type(self) -> type[GeneratorT]:
        """A required testing hook that allows type generation"""
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="generator")
    def fixture_generator(self, generator_type: type[GeneratorT]) -> GeneratorT:
        """A hook allowing implementations to override the fixture

        Args:
            generator_type: An input generator type

        Returns:
            A newly constructed generator
        """
        return generator_type()


class GeneratorIntegrationTests(GeneratorTests[GeneratorT]):
    """Base class for all vcs integration tests that test plugin agnostic behavior"""


class GeneratorUnitTests(GeneratorTests[GeneratorT]):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all Generator unit tests that test plugin agnostic behavior"""


class VersionControlTests(PluginTests, ABC, Generic[VersionControlT]):
    """Shared functionality between the different VersionControl testing categories"""

    @pytest.fixture(name="version_control_type", scope="session")
    def fixture_version_control_type(self) -> type[VersionControlT]:
        """A required testing hook that allows type generation"""
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="version_control")
    def fixture_version_control(self, version_control_type: type[VersionControlT]) -> VersionControlT:
        """A hook allowing implementations to override the fixture

        Args:
            version_control_type: An input version_control type

        Returns:
            A newly constructed version_control
        """
        return version_control_type()


class VersionControlIntegrationTests(VersionControlTests[VersionControlT]):
    """Base class for all generator integration tests that test plugin agnostic behavior"""


class VersionControlUnitTests(VersionControlTests[VersionControlT]):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all Generator unit tests that test plugin agnostic behavior
    """

    def test_not_repository(self, version_control: VersionControlT, tmp_path: Path) -> None:
        """Tests that the temporary directory path will not be registered as a repository

        Args:
            version_control: The VCS constructed type
            tmp_path: Temporary directory
        """

        assert not version_control.is_repository(tmp_path)
