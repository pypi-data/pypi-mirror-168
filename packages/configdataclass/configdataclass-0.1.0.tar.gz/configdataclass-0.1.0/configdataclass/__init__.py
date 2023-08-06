"""Represent a config as a dataclass.

Example:
    ```python
    from configdataclass import dataclass, ConfigReader
    from ipaddress import IPv4Address

    @dataclass
    class Default(ConfigReader):
      interval: int
      timeout: int

    @dataclass
    class Network(ConfigReader):
      ip: IPv4Address
      port: int

    @dataclass
    class Config(ConfigReader):
      default: Default
      network: Network

    config = Config.from_path("/tmp/conf.ini")
    connect(config.network.ip, config.default.timeout) # e.g
    ```
"""
__version__ = "0.1.0"
import dataclasses
from pathlib import Path
from configparser import ConfigParser
from typing import get_type_hints, Any, Generic, Optional, Mapping, TypeVar, Type
import inspect

T = TypeVar("T", bound="ConfigReader")


@dataclasses.dataclass
class ConfigReader:
    """Metaclass to subclass the config dataclasses from.

    Example:
        ```python
        @dataclass
        class Addr(ConfigReader):
            ip: str
            port: int
        ```
    """

    @classmethod
    def from_dict(cls: Type[T], data: Mapping[str, Any]) -> T:
        """Serialize the dataclass from a dictionary."""
        kwargs: dict[str, Any] = {}

        for field in dataclasses.fields(cls):

            if issubclass(field.type, ConfigReader):
                kwargs[field.name] = field.type.from_dict(data[field.name.capitalize()])
            elif field.default != dataclasses.MISSING and field.name not in data:
                # Field can be default in dataclass
                # -> if not present use default, else overwrite from file.
                # If field has no default it must be specified in the config file
                kwargs[field.name] = field.default
            else:
                # Field needs to be configured in file
                # Fields in file that are not defined will be thrown away
                try:
                    kwargs[field.name] = field.type(data[field.name])
                except KeyError as kerr:
                    raise KeyError(f"Field {field.name} must be configured") from kerr
                except ValueError as verr:
                    raise ValueError(f"Field {field.name} type, must be {field.type}") from verr
        return cls(**kwargs)

    @classmethod
    def from_path(cls: Type[T], path: Path | str) -> T:
        """Serialize the dataclass from a filepath of an *.ini-file."""
        assert Path(path).exists(), f"{path} is not a file!"
        conf = ConfigParser()
        conf.read(path)
        return cls.from_dict(conf)

    def to_path(self, path: Path | str) -> None:
        """Write the config as an *.ini file to the path."""
        parser = ConfigParser()
        parser.read_dict(dataclasses.asdict(self))
        with Path(path).open("w", encoding="utf8") as file:
            parser.write(file, True)

    def __getitem__(self, key: str) -> Any:
        return dataclasses.asdict(self)[key]
