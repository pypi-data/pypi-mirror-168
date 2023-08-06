"""Tests the integration test plugin
"""

import pytest

from pytest_cppython.mock import MockVersionControl
from pytest_cppython.plugin import VersionControlIntegrationTests


class TestCPPythonGenerator(VersionControlIntegrationTests[MockVersionControl]):
    """The tests for the Mock version control"""

    @pytest.fixture(name="version_control_type", scope="session")
    def fixture_version_control_type(self) -> type[MockVersionControl]:
        """A required testing hook that allows type generation

        Returns:
            An overridden version control type
        """
        return MockVersionControl
