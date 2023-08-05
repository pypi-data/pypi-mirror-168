"""Test the integrations related to the internal generator implementation and the 'Generator' interface itself
"""

import pytest

from pytest_cppython.mock import MockGenerator, MockGeneratorData
from pytest_cppython.plugin import GeneratorIntegrationTests


class TestMockGenerator(GeneratorIntegrationTests[MockGenerator, MockGeneratorData]):
    """The tests for our Mock generator"""

    @pytest.fixture(name="generator_data", scope="session")
    def fixture_generator_data(self) -> MockGeneratorData:
        """A required testing hook that allows GeneratorData generation

        Returns:
            An overridden data instance
        """
        return MockGeneratorData()

    @pytest.fixture(name="generator_type", scope="session")
    def fixture_generator_type(self) -> type[MockGenerator]:
        """A required testing hook that allows type generation

        Returns:
            The overridden generator type
        """
        return MockGenerator
