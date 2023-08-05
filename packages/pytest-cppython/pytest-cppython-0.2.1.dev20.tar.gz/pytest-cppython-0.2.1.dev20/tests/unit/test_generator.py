"""Test the functions related to the internal generator implementation and the 'Generator' interface itself
"""

import pytest

from pytest_cppython.mock import MockGenerator, MockGeneratorData
from pytest_cppython.plugin import GeneratorUnitTests


class TestMockGenerator(GeneratorUnitTests[MockGenerator, MockGeneratorData]):
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
            An overridden generator type
        """
        return MockGenerator

    def test_plugin_registration(self, generator: MockGenerator) -> None:
        """Override the base class 'GeneratorIntegrationTests' preventing a registration check for the Mock

        Args:
            generator: Required to override base argument
        """
