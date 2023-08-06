from typing import Optional

from requests import RequestException, Response

from laituri.errors import LaituriError


class DockerLoginFailed(LaituriError):
    """We failed to login to Docker from some reason."""

    pass


class ECRLoginFailed(LaituriError):
    """We failed to login to ECR from some reason."""

    pass


class InvalidDockerCommand(LaituriError):
    """The Docker command is misconfigured."""


class CallbackFailed(LaituriError):
    """
    Calling a registry credentials callback failed.
    """

    def get_callback_response(self) -> Optional[Response]:
        """
        Attempt to reach into the inner exception to get the response object returned by the callback.
        """
        if isinstance(self.__cause__, RequestException):
            response = self.__cause__.response
            if isinstance(response, Response):
                return response
        return None
