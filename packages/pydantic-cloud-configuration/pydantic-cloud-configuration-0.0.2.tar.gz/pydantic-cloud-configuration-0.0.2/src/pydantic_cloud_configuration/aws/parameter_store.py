"""AWS Parameter Store."""
import os
from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseSettings


class AwsParameterStore(BaseModel):
    """AWS Parameter Store model."""

    name: str

    location: str = ""
    location_path: str = ""

    settings_name: Optional[str] = ""
    settings_environment: Optional[str] = ""

    output_prefix: str = ""
    output_value_type: str = "str"
    lower_key: bool = False

    settings_name_constant = "SETTINGS_NAME"
    settings_environment_constant = "SETTINGS_ENVIRONMENT"
    settings_path_constant = "environments"

    check_settings: bool = False

    def __init__(self, **data: Any):
        """Init for AWS Parameter Store."""
        super().__init__(**data)
        self._get_environment_settings()
        if self.check_settings:
            self._check_settings()
        self._create_location()

    def _get_environment_settings(self) -> None:
        self.settings_name = os.environ.get(self.settings_name_constant)
        self.settings_environment = os.environ.get(self.settings_environment_constant)

    def _check_settings(self) -> None:
        if not self.settings_name or not self.settings_environment:
            raise ValueError("Check your settings!")

    def _create_location(self) -> None:
        if not self.location_path:
            if self.settings_name and self.settings_environment:
                self.location_path = f"/{self.settings_path_constant}/{self.settings_environment}/{self.settings_name}"  # noqa: B950
            else:
                self.location_path = f"/{self.settings_path_constant}"
        if not self.location:
            self.location = f"{self.location_path}/{self.name}"


def aws_parameter_settings(settings: BaseSettings) -> Dict[str, Any]:  # noqa: C901
    """Get parameters from Parameter Store."""
    try:
        import boto3  # type: ignore
    except ImportError as e:
        raise ModuleNotFoundError("Boto3 is not installed!") from e

    parameter_dict: Dict[Any, Any] = {}

    parameter_store_locations = settings.__config__.aws_parameter_locations  # type: ignore # noqa: B950

    try:
        parameter_store_client = boto3.client(service_name="ssm")
    except Exception as e:
        print(e)
        return parameter_dict

    for parameter_store_location in parameter_store_locations:
        try:
            parameter_text = parameter_store_client.get_parameter(
                Name=parameter_store_location.location, WithDecryption=True
            )["Parameter"]["Value"]

            if parameter_store_location.output_prefix == "":
                parameter_key = parameter_store_location.name
            else:
                parameter_key = f"{parameter_store_location.output_prefix}_{parameter_store_location.name}"  # noqa: B950

            if parameter_store_location.lower_key:
                parameter_key = parameter_key.lower()

            result_dict = {parameter_key: parameter_text}

            parameter_dict.update(result_dict)
        except Exception as e:
            print(e)

    return parameter_dict
