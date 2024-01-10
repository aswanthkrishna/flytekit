import subprocess
from abc import ABC, abstractmethod
from typing import List, Union

from sky import check, global_user_state

from flytekit.core.context_manager import SecretsManager


class CloudProvider(ABC):
    @abstractmethod
    def login(self):
        pass


class AWS(CloudProvider):
    def login(self, aws_access_key_id: str, aws_secret_access_key: str):
        # Make a simple API call to check if the credentials are valid
        try:
            # Set AWS credentials and region
            subprocess.run(["aws", "configure", "set", "aws_access_key_id", aws_access_key_id])
            subprocess.run(["aws", "configure", "set", "aws_secret_access_key", aws_secret_access_key])

            # Perform AWS CLI login
            subprocess.run(["aws", "sts", "get-caller-identity"])
        except Exception as e:
            print(f"Error configuring AWS credentials: {e}")


class GCP(CloudProvider):
    def login(self):
        print("Deploying instance on GCP")


def get_cloud_provider(name: str = "aws"):
    if name == "aws":
        return AWS()
    elif name == "gcp":
        return GCP()
    else:
        raise NotImplementedError("provider not implemented")


class LoginManager(object):
    @classmethod
    def _get_enabled_clouds(cls) -> Union[List[str], None]:
        try:
            check.check()
            return global_user_state.get_enabled_clouds()
        except SystemExit:
            print("no clouds configured")
            return None

    @classmethod
    def _is_logged_in(cls) -> bool:
        print("checking logins")
        return cls._get_enabled_clouds() is not None

    @classmethod
    def login(cls, secrets: SecretsManager):
        if not cls._is_logged_in():
            print("trying to login")
            try:
                aws_access_key_id = secrets.get("aws", "AWS_ACCESS_KEY_ID")
                aws_secret_access_key = secrets.get("aws", "AWS_SECRET_ACCESS_KEY")

                if aws_access_key_id and aws_secret_access_key:
                    provider = get_cloud_provider("aws")
                    provider.login(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
            except ValueError:
                print("cant find aws credentials")

            ##TODO: login to all providers here
