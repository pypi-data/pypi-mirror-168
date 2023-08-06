from contextlib import contextmanager
from typing import Any, Dict, Iterator

import requests
from requests.utils import default_headers

import laituri
from laituri.docker.credential_manager.docker_v1 import docker_v1_credential_manager
from laituri.docker.credential_manager.errors import CallbackFailed
from laituri.types import LogStatusCallable, RegistryCredentialsDict
from laituri.utils.retry import retry


@contextmanager
def registry_credentials_callback_v1_credential_manager(
    *,
    image: str,
    registry_credentials: RegistryCredentialsDict,
    log_status: LogStatusCallable,
) -> Iterator[None]:
    try:
        docker_credentials = fetch_docker_credentials(registry_credentials)
    except Exception as exc:
        raise CallbackFailed(f"Credential callback failed: {exc}") from exc

    with docker_v1_credential_manager(image=image, registry_credentials=docker_credentials, log_status=log_status):
        yield


@retry()
def fetch_docker_credentials(request_info: Dict[str, Any]) -> RegistryCredentialsDict:
    headers = default_headers()  # type: ignore[no-untyped-call]
    headers['User-Agent'] = f'{headers.get("User-Agent")} laituri/{laituri.__version__}'
    ri_headers = request_info.get('headers')
    if isinstance(ri_headers, dict):
        headers.update({key: str(value) for (key, value) in ri_headers.items() if key and value})

    response = requests.request(
        method=request_info.get('method', 'POST'),
        url=request_info['url'],
        headers=headers,
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError(f"Invalid response data: {data}")
    return {str(k): v for (k, v) in data.items()}
