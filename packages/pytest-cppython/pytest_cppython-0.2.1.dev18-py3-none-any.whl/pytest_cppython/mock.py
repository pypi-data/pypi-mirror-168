"""Shared definitions for testing.
"""

import logging
from pathlib import Path

from cppython_core.schema import (
    ConfigurePreset,
    CPPythonDataResolved,
    Generator,
    GeneratorConfiguration,
    GeneratorData,
    GeneratorDataResolved,
    GeneratorDataT,
    Interface,
    PEP621Resolved,
    ProjectConfiguration,
)

test_logger = logging.getLogger(__name__)
test_configuration = GeneratorConfiguration(root_directory=Path())


class MockInterface(Interface):
    """A mock interface class for behavior testing"""

    @staticmethod
    def name() -> str:
        """_summary_

        Returns:
            _description_
        """
        return "mock"

    def read_generator_data(self, generator_data_type: type[GeneratorDataT]) -> GeneratorDataT:
        """Implementation of Interface function

        Args:
            generator_data_type: _description_

        Returns:
            _description_
        """

        return generator_data_type()

    def write_pyproject(self) -> None:
        """Implementation of Interface function"""


class MockGeneratorDataResolved(GeneratorDataResolved):
    """Mock resolved generator data class"""


class MockGeneratorData(GeneratorData[MockGeneratorDataResolved]):
    """Mock generator data class"""

    def resolve(self, project_configuration: ProjectConfiguration) -> MockGeneratorDataResolved:
        """_summary_

        Args:
            project_configuration: _description_

        Returns:
            _description_
        """
        return MockGeneratorDataResolved()


test_generator = MockGeneratorData()


class MockGenerator(Generator[MockGeneratorData, MockGeneratorDataResolved]):
    """A mock generator class for behavior testing"""

    downloaded: Path | None = None

    def __init__(
        self,
        configuration: GeneratorConfiguration,
        project: PEP621Resolved,
        cppython: CPPythonDataResolved,
        generator: MockGeneratorDataResolved,
    ) -> None:
        super().__init__(configuration, project, cppython, generator)

    @staticmethod
    def name() -> str:
        """_summary_

        Returns:
            _description_
        """
        return "mock"

    @staticmethod
    def data_type() -> type[MockGeneratorData]:
        """_summary_

        Returns:
            _description_
        """
        return MockGeneratorData

    @staticmethod
    def resolved_data_type() -> type[MockGeneratorDataResolved]:
        """_summary_

        Returns:
            _description_
        """
        return MockGeneratorDataResolved

    @classmethod
    def tooling_downloaded(cls, path: Path) -> bool:
        """_summary_

        Args:
            path: _description_

        Returns:
            _description_
        """
        return cls.downloaded == path

    @classmethod
    async def download_tooling(cls, path: Path) -> None:
        cls.downloaded = path

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass

    def generate_cmake_config(self) -> ConfigurePreset:
        """_summary_

        Returns:
            _description_
        """

        return ConfigurePreset(name="mock-config")
