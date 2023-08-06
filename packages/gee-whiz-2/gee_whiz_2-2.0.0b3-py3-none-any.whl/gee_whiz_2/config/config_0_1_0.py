"""Gee Whiz 2 - A command line for managing Guild Wars 2.

This module contains the configuration file model version 0.1.0.
"""

from .common import StrEnum, BaseModel, Version
from pathlib import Path
from pydantic import root_validator
from typing import Optional


class GW2Interface(StrEnum):
    """The available interface styles."""

    GUI = "gui"
    TUI = "tui"


class GW2DirectXSetting(StrEnum):
    """The ArcDPS DirectX Setting configuration styles."""

    DX9 = "dx9"
    DX11 = "dx11"


class GW2GameType(StrEnum):
    """The game launcher type."""

    LUTRIS = "lutris"
    STEAM = "steam"
    NONE = "none"


class GeeWhiz2ArcDPSExtrasItem(BaseModel):
    """The ArcDPS Extras item configuration model."""

    update: bool = False
    version: Optional[Version]
    prerelease: bool = False


class GeeWhiz2ArcDPSExtrasConfig(BaseModel):
    """The ArcDPS Extras configuration model."""

    boontable: GeeWhiz2ArcDPSExtrasItem = GeeWhiz2ArcDPSExtrasItem()
    mechanics: GeeWhiz2ArcDPSExtrasItem = GeeWhiz2ArcDPSExtrasItem()
    killproof: GeeWhiz2ArcDPSExtrasItem = GeeWhiz2ArcDPSExtrasItem()
    healing: GeeWhiz2ArcDPSExtrasItem = GeeWhiz2ArcDPSExtrasItem()


class GeeWhiz2ArcDPSConfig(BaseModel):
    """The ArcDPS configuration model."""

    update: bool = False
    directx: GW2DirectXSetting = GW2DirectXSetting("dx11")
    extras: GeeWhiz2ArcDPSExtrasConfig = GeeWhiz2ArcDPSExtrasConfig()


class GW2LutrisGameSettings(BaseModel):
    """The Lutris game type options model."""

    id: Optional[int]


class GW2SteamGameSettings(BaseModel):
    """The Steam game type options model."""

    dot_steam_folder: Optional[Path]


class GW2Game(BaseModel):
    """The Game configuration model."""

    type: GW2GameType = "steam"
    gamedir: Optional[Path]
    datdir: Optional[Path]
    lutris: Optional[GW2LutrisGameSettings]
    steam: Optional[GW2SteamGameSettings]

    @root_validator
    def _check_optionals(cls, values: dict):
        if values.get("type") != "lutris" and values.get("lutris") is not None:
            raise ValueError("lutris configuration is invalid if type is not 'lutris'")
        if values.get("type") != "steam" and values.get("steam") is not None:
            raise ValueError("steam configuration is invalid if type is not 'steam'")
        return values


class GeeWhiz2Config(BaseModel):
    """The configuration file model."""

    config_version: Version
    start_gw2: bool = False
    interface: GW2Interface = "tui"
    game: GW2Game = GW2Game()
    arcdps: GeeWhiz2ArcDPSConfig = GeeWhiz2ArcDPSConfig()
    profile_prompt: bool = True
