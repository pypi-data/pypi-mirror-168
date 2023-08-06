"""Default Cloud Base Settings."""

from pydantic import BaseSettings


class CloudBaseSettings(BaseSettings):
    """Default Cloud Base Settings."""

    settings_name: str
    settings_environment: str
