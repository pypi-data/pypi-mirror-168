"""Test the integrations related to the internal provider implementation and the 'Provider' interface itself
"""

import pytest

from pytest_cppython.mock import MockProvider, MockProviderData
from pytest_cppython.plugin import ProviderIntegrationTests


class TestMockProvider(ProviderIntegrationTests[MockProvider, MockProviderData]):
    """The tests for our Mock provider"""

    @pytest.fixture(name="provider_data", scope="session")
    def fixture_provider_data(self) -> MockProviderData:
        """A required testing hook that allows ProviderData generation

        Returns:
            An overridden data instance
        """
        return MockProviderData()

    @pytest.fixture(name="provider_type", scope="session")
    def fixture_provider_type(self) -> type[MockProvider]:
        """A required testing hook that allows type generation

        Returns:
            The overridden provider type
        """
        return MockProvider
