from contextlib import contextmanager
from typing import ContextManager, Iterator

from laituri.types import LogStatusCallable, RegistryCredentialsDict


@contextmanager
def dummy_credential_manager(
    *,
    image: str,
    registry_credentials: RegistryCredentialsDict,
    log_status: LogStatusCallable,
) -> Iterator[None]:
    """
    Credential context manager that does nothing.

    This can used when no credentials are included.
    """
    yield


def get_dummy_credential_manager() -> ContextManager[None]:
    """
    Construct a dummy credential manager without having to think about arguments.
    """
    return dummy_credential_manager(image="", registry_credentials={}, log_status=lambda s: None)
