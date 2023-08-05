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
    GeneratorConfiguration,
    GeneratorDataT,
    GeneratorT,
    InterfaceConfiguration,
    InterfaceT,
    ProjectConfiguration,
)

from pytest_cppython.fixtures import CPPythonFixtures


class PluginTests(CPPythonFixtures):
    """Shared testing information for all plugin test classes"""


class GeneratorTests(PluginTests, ABC, Generic[GeneratorT, GeneratorDataT]):
    """Shared functionality between the different Generator testing categories"""

    @pytest.fixture(name="generator_data", scope="session")
    def fixture_generator_data(self) -> GeneratorDataT:
        """A required testing hook that allows GeneratorData generation"""
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="generator_type", scope="session")
    def fixture_generator_type(self) -> type[GeneratorT]:
        """A required testing hook that allows type generation"""
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="generator_construction_data", scope="session")
    def fixture_generator_construction_data(
        self, generator_type: type[GeneratorT], generator_data: GeneratorDataT
    ) -> tuple[type[GeneratorT], GeneratorDataT]:
        """Collects the generator type construction data as a tuple

        Args:
            generator_type: Overridden generator type
            generator_data: Overridden generator data

        Returns:
            Tuple containing the overridden fixture results
        """
        return generator_type, generator_data

    @pytest.fixture(autouse=True, scope="session")
    def _fixture_install_dependency(self, generator_type: type[GeneratorT], install_path: Path) -> None:
        """Forces the download to only happen once per test session"""

        path = install_path / generator_type.name()
        path.mkdir(parents=True, exist_ok=True)

        asyncio.run(generator_type.download_tooling(path))

    @pytest.fixture(name="generator")
    def fixture_generator(
        self,
        generator_construction_data: tuple[type[GeneratorT], GeneratorDataT],
        generator_configuration: GeneratorConfiguration,
        static_pyproject_data: tuple[PEP621, CPPythonData],
        workspace: ProjectConfiguration,
    ) -> GeneratorT:
        """A hook allowing implementations to override the fixture

        Args:
            generator_construction_data: Generator construction data
            generator_configuration: Generator configuration data
            static_pyproject_data: Generated static project definition
            workspace: Temporary directory defined by a configuration object

        Returns:
            A newly constructed generator
        """

        pep621, cppython = static_pyproject_data
        generator_type, generator_data = generator_construction_data

        modified_project_data = pep621.resolve(workspace)
        modified_cppython_data = cppython.resolve(CPPythonDataResolved, workspace)
        modified_cppython_data = modified_cppython_data.generator_resolve(generator_type)
        modified_generator_data = generator_data.resolve(workspace)

        return generator_type(
            generator_configuration, modified_project_data, modified_cppython_data, modified_generator_data
        )


class GeneratorIntegrationTests(GeneratorTests[GeneratorT, GeneratorDataT]):
    """Base class for all generator integration tests that test plugin agnostic behavior"""

    def test_is_downloaded(self, generator: GeneratorT) -> None:
        """Verify the generator is downloaded from fixture

        Args:
            generator: A newly constructed generator
        """

        assert generator.tooling_downloaded(generator.cppython.install_path)

    def test_not_downloaded(self, generator_type: type[GeneratorT], tmp_path: Path) -> None:
        """Verify the generator can identify an empty tool

        Args:
            generator_type: An input generator type
            tmp_path: A temporary path for the lifetime of the function
        """

        assert not generator_type.tooling_downloaded(tmp_path)

    def test_install(self, generator: GeneratorT) -> None:
        """Ensure that the vanilla install command functions

        Args:
            generator: A newly constructed generator
        """
        generator.install()

    def test_update(self, generator: GeneratorT) -> None:
        """Ensure that the vanilla update command functions

        Args:
            generator: A newly constructed generator
        """
        generator.update()


class GeneratorUnitTests(GeneratorTests[GeneratorT, GeneratorDataT]):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all generator unit tests that test plugin agnostic behavior
    """

    def test_plugin_registration(self, generator: GeneratorT) -> None:
        """Test the registration with setuptools entry_points

        Args:
            generator: A newly constructed generator
        """
        plugin_entries = entry_points(group=f"cppython.{generator.group()}")
        assert len(plugin_entries) > 0

    def test_preset_generation(self, generator: GeneratorT) -> None:
        """Tests the generation of the cmake configuration preset

        Args:
            generator: A newly constructed generator
        """
        generator.generate_cmake_config()


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
