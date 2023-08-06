"""Shared definitions for testing.
"""

import logging
from pathlib import Path

from cppython_core.schema import (
    CPPythonDataResolved,
    Generator,
    Interface,
    PEP621Resolved,
    ProjectConfiguration,
    Provider,
    ProviderConfiguration,
    ProviderData,
    ProviderDataResolved,
    ProviderDataT,
    VersionControl,
)

test_logger = logging.getLogger(__name__)
test_configuration = ProviderConfiguration(root_directory=Path())


class MockInterface(Interface):
    """A mock interface class for behavior testing"""

    @staticmethod
    def name() -> str:
        """_summary_

        Returns:
            _description_
        """
        return "mock"

    def read_provider_data(self, provider_data_type: type[ProviderDataT]) -> ProviderDataT:
        """Implementation of Interface function

        Args:
            provider_data_type: _description_

        Returns:
            _description_
        """

        return provider_data_type()

    def write_pyproject(self) -> None:
        """Implementation of Interface function"""


class MockProviderDataResolved(ProviderDataResolved):
    """Mock resolved provider data class"""


class MockProviderData(ProviderData[MockProviderDataResolved]):
    """Mock provider data class"""

    def resolve(self, project_configuration: ProjectConfiguration) -> MockProviderDataResolved:
        """_summary_

        Args:
            project_configuration: _description_

        Returns:
            _description_
        """
        return MockProviderDataResolved()


test_provider = MockProviderData()


class MockProvider(Provider[MockProviderData, MockProviderDataResolved]):
    """A mock provider class for behavior testing"""

    downloaded: Path | None = None

    def __init__(
        self,
        configuration: ProviderConfiguration,
        project: PEP621Resolved,
        cppython: CPPythonDataResolved,
        provider: MockProviderDataResolved,
    ) -> None:
        super().__init__(configuration, project, cppython, provider)

    @staticmethod
    def name() -> str:
        """_summary_

        Returns:
            _description_
        """
        return "mock"

    @staticmethod
    def data_type() -> type[MockProviderData]:
        """_summary_

        Returns:
            _description_
        """
        return MockProviderData

    @staticmethod
    def resolved_data_type() -> type[MockProviderDataResolved]:
        """_summary_

        Returns:
            _description_
        """
        return MockProviderDataResolved

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


class MockGenerator(Generator):
    """A mock generator class for behavior testing"""

    @staticmethod
    def name() -> str:
        """_summary_

        Returns:
            _description_
        """
        return "mock"


class MockVersionControl(VersionControl):
    """A mock generator class for behavior testing"""

    @staticmethod
    def name() -> str:
        """_summary_

        Returns:
            _description_
        """
        return "mock"

    def extract_version(self, path: Path) -> str:
        """_summary_

        Args:
            path: _description_

        Returns:
            _description_
        """
        return "1.0.0"

    def is_repository(self, path: Path) -> bool:
        """_summary_

        Args:
            path: _description_

        Returns:
            _description_
        """
        return False
