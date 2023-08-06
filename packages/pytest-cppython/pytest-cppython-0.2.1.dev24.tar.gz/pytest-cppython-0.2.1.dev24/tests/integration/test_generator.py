"""Tests the integration test plugin
"""

import pytest

from pytest_cppython.mock import MockGenerator
from pytest_cppython.plugin import GeneratorIntegrationTests


class TestCPPythonGenerator(GeneratorIntegrationTests[MockGenerator]):
    """The tests for the Mock generator"""

    @pytest.fixture(name="generator_type", scope="session")
    def fixture_generator_type(self) -> type[MockGenerator]:
        """A required testing hook that allows type generation

        Returns:
            An overridden generator type
        """
        return MockGenerator
