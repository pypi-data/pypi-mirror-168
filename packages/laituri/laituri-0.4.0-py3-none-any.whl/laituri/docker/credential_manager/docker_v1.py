import logging
import shutil
import subprocess
from contextlib import contextmanager
from typing import Iterator

from laituri import settings
from laituri.docker.credential_manager.errors import DockerLoginFailed, InvalidDockerCommand
from laituri.types import LogStatusCallable, RegistryCredentialsDict
from laituri.utils.images import get_image_hostname

log = logging.getLogger(__name__)


@contextmanager
def docker_v1_credential_manager(
    *,
    image: str,
    registry_credentials: RegistryCredentialsDict,
    log_status: LogStatusCallable,
) -> Iterator[None]:
    # If image looks like a dockerhub image, use docker.io as the registry domain
    hostname = get_image_hostname(image)
    try:
        docker_login(
            domain=str(hostname),
            username=str(registry_credentials['username']),
            password=str(registry_credentials['password']),
        )
    except DockerLoginFailed as dlf:
        raise DockerLoginFailed(f'Failed Docker login to {hostname}: {str(dlf)}') from dlf
    try:
        yield
    finally:
        docker_logout(hostname)


def get_docker_command() -> str:
    cmd = shutil.which(settings.DOCKER_COMMAND)
    if not cmd:
        raise InvalidDockerCommand(f"Invalid Docker command: {cmd}")
    return cmd


def docker_login(domain: str, username: str, password: str) -> bool:
    """
    Use Docker command-line client to login to the specified image registry.
    """
    args = [
        get_docker_command(),
        'login',
        '--username', username,
        '--password-stdin',
        domain,
    ]
    log.debug(f"Running `{' '.join(args)}`")
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        cmd_input = (password + '\n').encode('utf-8')
        stdout, _ = proc.communicate(input=cmd_input, timeout=settings.DOCKER_TIMEOUT)
    except subprocess.TimeoutExpired as te:
        raise DockerLoginFailed('timed out') from te
    if proc.returncode != 0:
        raise DockerLoginFailed(stdout.decode('utf-8', errors='ignore'))
    return True


def docker_logout(domain: str) -> None:
    """
    Use Docker command-line client to logout from the specified image registry.
    """
    # when logging out of "docker.io" they actually mean "https://index.docker.io/v1/"
    if domain == 'docker.io':
        domain = 'https://index.docker.io/v1/'

    try:
        log.debug(f'Running `docker logout {domain}`')
        subprocess.check_call([
            get_docker_command(),
            'logout',
            domain,
        ], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, timeout=settings.DOCKER_TIMEOUT)
    except subprocess.CalledProcessError as cpe:
        message = cpe.stdout.decode('utf-8', errors='ignore')
        log.warning(f'Failed `docker logout {domain}`: {message}')
