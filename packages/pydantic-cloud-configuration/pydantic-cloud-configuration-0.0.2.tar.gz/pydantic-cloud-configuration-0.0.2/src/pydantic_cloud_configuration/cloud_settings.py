"""Main settings file."""
from functools import partial
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import cast

from pydantic_cloud_configuration.aws.parameter_store import AwsParameterStore
from pydantic_cloud_configuration.aws.parameter_store import (  # noqa: F401
    aws_parameter_settings,
)
from pydantic_cloud_configuration.cloud_base_settings import CloudBaseSettings


def customise_sources(  # type: ignore
    cls, init_settings, env_settings, file_secret_settings, settings_order
):
    """Customised sources for retrieving settings from the cloud."""
    order: Tuple[Any, ...] = ()
    for setting in settings_order:
        current_setting_local = locals().get(setting)
        if current_setting_local:
            order = order + (current_setting_local,)
            continue
        current_setting_global = globals().get(setting)
        if current_setting_global:
            order = order + (current_setting_global,)

    return order


class CloudSettings:
    """Main cloud configuration class."""

    def __new__(
        cls,
        aws_parameter_locations: Optional[List[AwsParameterStore]] = None,
        class_type: str = "Config",
        config_class: Optional[Dict[str, Any]] = None,
        class_name: str = "CloudSettings",
        env_file: str = ".env",
        extra: str = "ignore",
        settings_order: Optional[List[str]] = None,
    ) -> "CloudSettings":
        """Creation of a new Cloud Settings Class.

        Args:
            aws_parameter_locations: List of AwsParameterStore objects
            class_type: Type of class to use, default Config
            config_class: The configured class to use, default empty
            class_name: Name of the class to generate, default CloudSettings
            env_file: Location of the env file to use
            extra: How to handle extra parameters, default ignore
            settings_order: The order of settings to parse

        Returns:
            CloudSettingsClass

        """
        config_class = config_class or {}
        if settings_order is None:
            settings_order = ["init_settings", "env_settings", "file_secret_settings"]
        if aws_parameter_locations:
            config_class["aws_parameter_locations"] = aws_parameter_locations
            settings_order.append("aws_parameter_settings")

        customise_source_partial = partial(
            customise_sources, settings_order=settings_order
        )

        config_class["customise_sources"] = classmethod(customise_source_partial)
        config_class["application_base_settings"] = CloudBaseSettings()
        config_class["env_file"] = env_file
        config_class["extra"] = extra

        return cast(
            CloudSettings,
            type(
                class_name,
                (CloudBaseSettings,),
                {"Config": type(f"{class_name}.Config", (), config_class)},
            ),
        )
