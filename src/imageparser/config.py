"""Load screenshot-analysis settings from YAML configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml

CONFIG_ENV_VAR = "IMAGEPARSER_CONFIG"
LEGACY_CONFIG_ENV_VAR = "APPAUTOMATION_CONFIG"
DEFAULT_CONFIG_NAME = "config.yaml"


@dataclass
class PhoneConfig:
    """Screen profile plus legacy device serial from the preserved config schema."""
    serial: str                 # retained for configuration compatibility
    profile: str = "hd720"      # key of constants.SCREEN_PROFILES


@dataclass
class EmailConfig:
    """Legacy Gmail notification settings retained for configuration compatibility."""
    sender: str
    recipient: str
    credentials_file: str = "credentials.json"
    token_file: str = "token.json"


@dataclass
class Config:
    """Application configuration."""
    work_base: Path
    phones: Dict[str, PhoneConfig]
    adb_path: str = "adb"
    tesseract_cmd: Optional[str] = None
    ocr_engine: str = "auto"    # auto | easyocr | paddleocr | tesseract
    ocr_gpu: bool = True
    partial_routes: List[int] = field(default_factory=list)
    email: Optional[EmailConfig] = None

    def phone(self, alias: str) -> PhoneConfig:
        try:
            return self.phones[alias]
        except KeyError:
            known = ", ".join(sorted(self.phones)) or "<none>"
            raise KeyError(f"Unknown phone '{alias}'. Configured phones: {known}") from None


def find_config(explicit: Optional[str] = None) -> Path:
    """Locate explicit config, environment config, local config, then the bundled example."""
    environment_config = (
        os.environ.get(CONFIG_ENV_VAR) or os.environ.get(LEGACY_CONFIG_ENV_VAR)
    )
    candidate = explicit or environment_config or DEFAULT_CONFIG_NAME
    path = Path(candidate).expanduser()
    if not explicit and not environment_config and not path.is_file():
        example_config = Path(__file__).resolve().parents[2] / "config.example.yaml"
        if example_config.is_file():
            return example_config
    if not path.is_file():
        raise FileNotFoundError(
            f"Config file '{path}' not found. Pass --config or set "
            f"${CONFIG_ENV_VAR} (legacy: ${LEGACY_CONFIG_ENV_VAR})."
        )
    return path


def load_config(explicit: Optional[str] = None) -> Config:
    """Read and validate the YAML configuration."""
    with open(find_config(explicit), encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    phones = {
        alias.lower(): PhoneConfig(serial=str(p["serial"]), profile=p.get("profile", "hd720"))
        for alias, p in (raw.get("phones") or {}).items()
    }
    email_raw = raw.get("email")
    email = EmailConfig(**email_raw) if email_raw else None

    return Config(
        work_base=Path(raw.get("work_base", "workspace")).expanduser(),
        phones=phones,
        adb_path=raw.get("adb_path", "adb"),
        tesseract_cmd=raw.get("tesseract_cmd"),
        ocr_engine=raw.get("ocr_engine", "auto"),
        ocr_gpu=bool(raw.get("ocr_gpu", True)),
        partial_routes=[int(i) for i in raw.get("partial_routes", [])],
        email=email,
    )
