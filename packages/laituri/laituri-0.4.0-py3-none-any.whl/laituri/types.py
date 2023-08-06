from typing import Any, Callable, ContextManager, Dict

LogStatusCallable = Callable[[str], None]
RegistryCredentialsDict = Dict[str, Any]
CredentialManager = ContextManager[None]
CredentialManagerFactory = Callable[..., CredentialManager]
