import base64
from contextlib import contextmanager
from typing import Dict, Iterator

from laituri.docker.credential_manager.docker_v1 import docker_v1_credential_manager
from laituri.docker.credential_manager.errors import ECRLoginFailed
from laituri.types import LogStatusCallable, RegistryCredentialsDict


@contextmanager
def ecr_with_role_v1_credential_manager(
    *,
    image: str,
    registry_credentials: RegistryCredentialsDict,
    log_status: LogStatusCallable,
) -> Iterator[None]:
    from boto3 import Session
    role_name = registry_credentials['role_name']
    creds = get_role_credentials_from_instance_metadata(role_name)
    try:
        sess = Session(
            region_name=registry_credentials['region'],
            aws_access_key_id=creds['access_key'],
            aws_secret_access_key=creds['secret_key'],
            aws_session_token=creds['token'],
        )
        ecr = sess.client('ecr')
        result = ecr.get_authorization_token()
        auth_token = base64.b64decode(result['authorizationData'][0]['authorizationToken']).decode()
        username, password = auth_token.split(':')
        docker_credentials = {
            'username': username,
            'password': password,
        }
    except Exception as exc:
        raise ECRLoginFailed(f"Role based docker credentials fetch failed: {exc}") from exc

    with docker_v1_credential_manager(image=image, registry_credentials=docker_credentials, log_status=log_status):
        yield


def get_role_credentials_from_instance_metadata(role_name: str) -> Dict[str, str]:
    from botocore.utils import InstanceMetadataFetcher
    fetcher = InstanceMetadataFetcher()
    creds: Dict[str, str] = fetcher.retrieve_iam_role_credentials()
    if creds.get('role_name') != role_name:
        # User tried to use a IAM role which is not attached to the EC2 machine
        raise ECRLoginFailed(f"No instance role {role_name} found")
    return creds
