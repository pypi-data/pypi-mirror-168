"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the common classes used in configuration file models.
"""

import json
import os
import yaml
from enum import Enum
from pathlib import Path
from pydantic import BaseModel as PydanticBaseModel
from semantic_version import Version as UnvalidatedVersion
from typing import Optional, Set, Union

from ..util import make_logger

logger = make_logger()


class StrEnum(str, Enum):
    """Represent a choice between a fixed set of strings.

    A mix-in of string and enum, representing itself as the string value.
    """

    @classmethod
    def list(cls) -> list:
        """Return a list of the available options in the Enum."""
        return [e.value for e in cls]

    def __str__(self) -> str:
        """Return only the value of the enum when cast to String."""
        return self.value


class Version(UnvalidatedVersion):
    """Validatable version for Pydantic."""

    def __init__(self, version_string: Union[str, float, int],
                 *args, **kwargs):
        """Initialize a (slightly) sanitized version."""
        if version_string is not None:
            version_string = str(version_string).lstrip("v")
        try:
            super().__init__(version_string, *args, **kwargs)
        except:  # noqa: E722 (literally be quiet)
            logger.warning(f'We have to modify {version_string} to attempt parsing.')
            super().__init__(self.sanitize(version_string), *args, **kwargs)

    @classmethod
    def sanitize(cls, version_string) -> str:
        """Try to sanitize the version down to the bare essentials."""
        valid_version_chars = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-')
        sanitized_version = ''
        remainder = ''
        # Krappa does this for some reason
        original_version_string = version_string[:]
        version_string = version_string.lstrip('Version ')
        if '.rc' in version_string:
            # Krappa why do you do this to me
            split_version = version_string.split('.rc')
            version_string = f'{split_version[0]}rc{split_version[1]}'
        for char in version_string:
            if remainder != '':
                remainder += char
                continue
            if char in valid_version_chars:
                sanitized_version += char
            else:
                # I really hate how Krappa does versioning
                if sanitized_version.count('.') == 1:
                    sanitized_version += '.0'
                sanitized_version += '-'
                remainder += char
                continue
        sanitized_version += remainder
        if sanitized_version.count('.') == 1:
            sanitized_version += '.0'
        logger.debug(f'Sanitized "{original_version_string}" to "{sanitized_version}"')
        return sanitized_version

    @classmethod
    def __get_validators__(cls):
        """Yield the validator for Version strings."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, float, int]):
        """Validate Version strings."""
        # This will raise TypeErrors for us 🎉
        return cls.coerce(str(v).lstrip("v"))


class BaseModel(PydanticBaseModel):
    """Gee Whiz 2 Base Model."""

    class PydanticEncoder(json.JSONEncoder):
        """Serialize Pydantic models.

        A JSONEncoder subclass that prepares Pydantic models for serialization.
        """

        def default(self, obj):
            """Encode model objects based on their type."""
            if isinstance(obj, BaseModel) and callable(obj.dict):
                return obj.dict(exclude_none=True)
            elif isinstance(obj, UnvalidatedVersion) or isinstance(obj, StrEnum):
                return str(obj)
            elif isinstance(obj, Path):
                return str(obj.resolve())
            elif isinstance(obj, set):
                return list(obj)
            elif getattr(obj, '__serialize__') is not None:
                return obj.__serialize__()

            return json.JSONEncoder.default(self, obj)  # pragma: nocover (I don't anticipate deserializing arbitrary
            # data types, but I see no reason to not be ready if we need to)

    class Config:
        """Configuration class for Pydantic models."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_assignment = True

    @classmethod
    def parse_obj(cls, obj) -> 'BaseModel':
        """Overload the parse_obj method to add a debug print."""
        logger.debug(f'Instantiating model from object: {obj}')
        return super().parse_obj(obj)

    @classmethod
    def from_yaml(cls, yaml_text: str) -> 'BaseModel':
        """Instantiate a BaseModel from a yaml string."""
        cleaned_text = yaml_text.strip().replace("\n", "\\n").replace("\"", "\\\"")
        logger.debug(f'Instantiating model from yaml: "{cleaned_text}"')
        return cls.parse_obj(yaml.safe_load(yaml_text))

    def json(self) -> str:
        """Serialize a BaseModel object to JSON text."""
        return json.dumps(self, cls=self.PydanticEncoder)

    def yaml(self, *args, **kwargs) -> str:
        """Seriealize a BaseModel object to YAML text."""
        if 'sort_keys' in kwargs:
            return yaml.dump(json.loads(self.json()), *args, **kwargs)
        else:
            return yaml.dump(json.loads(self.json()), *args, sort_keys=False, **kwargs)


class GeeWhiz2StateProfiles(BaseModel):
    """The state profile tracking model."""

    current: Optional[str]
    available: Set[str] = set()


class GeeWhiz2State(BaseModel):
    """The state tracking model."""

    # Addons we know need a version
    boontable: Optional[Version]
    mechanics: Optional[Version]
    killproof: Optional[Version]
    healing: Optional[Version]
    # Profile management
    profiles: GeeWhiz2StateProfiles = GeeWhiz2StateProfiles()

    @classmethod
    def path(cls) -> Path:
        """Return the path the state file should be at."""
        return Path(os.environ.get('HOME', '/home/fake')).joinpath('.config', 'gw2', 'state.yml')

    @classmethod
    def load(cls) -> 'GeeWhiz2State':
        """Load the gw2 state from the state file."""
        state_file = cls.path()
        if state_file.exists():
            logger.debug(f'Loading state from {state_file}')
            with open(state_file) as f:
                state_yml = f.read()
            return cls.from_yaml(state_yml)
        else:
            logger.debug(f'No state in {state_file}, creating new')
            return cls()

    def save(self) -> None:
        """Save the gw2 state to the state file."""
        state_file = self.path()
        state_file.parent.mkdir(exist_ok=True, parents=True)
        with open(state_file, 'w') as f:
            logger.debug(f'Saving state to {state_file}')
            f.write(self.yaml())
