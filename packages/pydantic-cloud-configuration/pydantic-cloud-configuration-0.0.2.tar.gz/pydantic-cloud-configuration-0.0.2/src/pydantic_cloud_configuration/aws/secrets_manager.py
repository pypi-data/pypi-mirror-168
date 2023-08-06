"""AWS Secret Manager."""
# import json
# from typing import Any
# from typing import Dict
#
# from pydantic import BaseModel
# from pydantic import BaseSettings
#
#
# class SecretsManager(BaseModel):
#     prefix_location: str
#     location: str
#     output_prefix: str
#     output_value_type: str = "str"
#
#
# def get_secrets(settings: BaseSettings) -> Dict[str, Any]:
#     try:
#         import boto3
#     except ImportError as e:
#         raise ImportError("Boto3 is not installed!") from e
#
#     result = {}
#
#     try:
#         secrets_manager_locations = settings.__config__.secrets_manager_locations
#     except Exception as e:
#         print(e)
#         return result
#
#     if len(secrets_manager_locations) == 0:
#         return result
#
#     try:
#         secrets_manager_client = boto3.client(service_name="secretsmanager")
#     except Exception as e:
#         print(e)
#         return result
#
#     if len(secrets_manager_locations) >= 1:
#         for secret_manager_location in secrets_manager_locations:
#             try:
#                 secrets_dict = secrets_manager_client.get_secret_value(
#                     SecretId=secret_manager_location.location
#                 )["SecretString"]
#
#                 secrets_dict_json = json.loads(secrets_dict)
#
#                 prefix_secrets_dict = {
#                     f"{secret_manager_location.output_prefix}_{key}": val
#                     for key, val in secrets_dict_json.items()
#                 }
#                 result.update(prefix_secrets_dict)
#             except Exception as e:
#                 print(e)
#
#     return result
