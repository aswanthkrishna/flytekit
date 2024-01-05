from abc import ABC, abstractmethod
from flytekit.core.context_manager import SecretsManager
from typing import List, Union

import sky
from sky import global_user_state, check
from flytekit.loggers import logger

import boto3


class CloudProvider(ABC):
    @abstractmethod
    def login(self):
        pass

class AWS(CloudProvider):
    def login(self, aws_access_key_id: str, aws_secret_access_key: str):
        
            # Create a session using the provided credentials and region
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        # Create a client using the configured session
        s3_client = session.client('s3')

        # Make a simple API call to check if the credentials are valid
            # Create a client using the configured session
        sts_client = session.client('sts')

        # Make a simple API call to check if the credentials are valid
        try:
            response = sts_client.get_caller_identity()
            account_id = response['Account']
            user_id = response['UserId']
            arn = response['Arn']

            print(f"AWS credentials configured successfully!\n"
                f"Account ID: {account_id}\n"
                f"User ID: {user_id}\n"
                f"ARN: {arn}")
        except Exception as e:
            print(f"Error configuring AWS credentials: {e}")


class GCP(CloudProvider):
    def login(self):
        print("Deploying instance on GCP")


def get_cloud_provider(name: str = 'aws'):
    if name == 'aws' : return AWS()
    elif name == 'gcp': return GCP()
    else: raise NotImplementedError('provider not implemented')

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
    def login(cls, secrets : SecretsManager):
        if not cls._is_logged_in():
            print("trying to login")
            try:
                aws_access_key_id=secrets.get("aws", "aws_access_key_id")
                aws_secret_access_key=secrets.get("aws", "aws_secret_access_key")

                if aws_access_key_id and aws_secret_access_key:
                    provider = get_cloud_provider("aws")
                    provider.login(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
            except ValueError:
                print("cant find aws credentials")

            ##TODO: login to all providers here