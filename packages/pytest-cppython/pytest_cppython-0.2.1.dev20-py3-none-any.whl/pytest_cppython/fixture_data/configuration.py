"""Defines variations of Interface/Generator data
"""

from pathlib import Path

from cppython_core.schema import GeneratorConfiguration, InterfaceConfiguration

generator_config_test_list: list[GeneratorConfiguration] = [GeneratorConfiguration(root_directory=Path("."))]

interface_config_test_list: list[InterfaceConfiguration] = [InterfaceConfiguration()]
