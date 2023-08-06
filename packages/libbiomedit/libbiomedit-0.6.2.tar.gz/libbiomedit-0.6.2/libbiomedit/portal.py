import base64
import json
from dataclasses import dataclass, fields
from enum import Enum
from functools import wraps
from http.client import HTTPResponse
from typing import Any, Callable, Dict, Iterable, Optional, TypeVar
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from .metadata import MetaData

URL_OPENER = Callable[..., HTTPResponse]


class KeyStatus(Enum):
    APPROVED = "APPROVED"  # Key approved by key authority (analogous to signature).
    APPROVAL_REVOKED = "APPROVAL_REVOKED"  # Approval was revoked by key authority.
    DELETED = "DELETED"  # Key was deleted from keyserver (user ID is removed).
    KEY_REVOKED = "KEY_REVOKED"  # Key was revoked by user.
    PENDING = "PENDING"  # Key info was added to database but key not yet approved.
    REJECTED = "REJECTED"  # Key was never approved and is not trusted.
    UNKNOWN_KEY = "UNKNOWN_KEY"  # Key info is not present in the portal.


class DPKGStatus(Enum):
    ENTER = "ENTER"  # Data package has arrived at the landing zone.
    PROCESSED = "PROCESSED"  # Data package has been successfully forwarded to
    #                          another node or a project space.
    ERROR = "ERROR"  # An error occurred while processing the package.


@dataclass
class DpkgInfo:
    """Data package transit information summary."""

    destination_node: str
    project_code: str
    data_provider: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "DpkgInfo":
        """Convert a dictionary into a DpkgInfo object.

        The "destination_node" and "project_code" fields are mandatory. A
        ValueError is raised if they are missing.
        """

        field_names = {f.name for f in fields(cls)}
        try:
            # Node codes are always in lower case.
            data["destination_node"] = data["destination_node"].lower()
            return cls(**{key: val for key, val in data.items() if key in field_names})
        except (KeyError, TypeError) as e:
            # If any mandatory fields are missing, this error is raised.
            raise ValueError(
                "Invalid DpkgInfo data: one or more mandatory keys are "
                f"missing from the input data: {e}"
            ) from e


@dataclass
class PortalApi:
    base_url: str = "https://portal.dcc.sib.swiss"
    # Note: endpoint URLs must end with a "/" otherwise Django complains.
    dpkg_check: str = "backend/data-package/check/"
    dpkg_log: str = "backend/data-package/log/"
    pgpkey_status: str = "backend/pgpkey/status/"
    urlopen: URL_OPENER = urlopen
    username: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self) -> None:
        # Verify and set the base URL value: ensure that the specified
        # base_url contains only scheme, hostname and optional port number.
        parsed = urlparse(self.base_url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"

    def _build_endpoint_url(self, endpoint_url: str) -> str:
        """Build the URL of a portal endpoint."""
        return urljoin(self.base_url, endpoint_url)

    def _post(
        self,
        url: str,
        data: bytes,
        headers: Optional[Dict[str, str]] = None,
    ) -> bytes:
        """Make a POST request that sends the specified data to the specified
        url endpoint.
        """
        request = Request(
            url,
            data,
            method="POST",
            headers={
                "Content-Type": "application/json; charset=UTF-8",
                **(headers or {}),
            },
        )
        # Make the request using the class' specified URL opener and return
        # the text contained in the response from the server.
        with self.urlopen(request) as response:
            return response.read()

    @property
    def pgpkey_status_endpoint(self) -> str:
        """Endpoint to retrieve the approval status of a PGP key."""
        return self._build_endpoint_url(self.pgpkey_status)

    @property
    def dpkg_check_endpoint(self) -> str:
        """Endpoint to check the metadata of a data package (dpkg)."""
        return self._build_endpoint_url(self.dpkg_check)

    @property
    def dpkg_log_endpoint(self) -> str:
        """Endpoint to log the progress of a data package (dpkg) transfer."""
        return self._build_endpoint_url(self.dpkg_log)

    def auth_header(self) -> Dict[str, str]:
        """Generate an authorization header for requests that require to be
        authenticated.
        """
        auth_str = (
            self.username
            and self.password
            and base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        )
        return {"Authorization": f"Basic {auth_str}"} if auth_str else {}

    def get_key_status(self, fingerprints: Iterable[str]) -> Dict[str, KeyStatus]:
        """Query the portal API for the status of one or more PGP keys
        specified via their fingerprints.

        Returns the status of the queried PGP keys as dict of the form
        {<fingerprint>: <status>}.
        """
        response = _handle_errors(self._post)(
            url=self.pgpkey_status_endpoint,
            data=json.dumps({"fingerprints": list(fingerprints)}).encode(),
        )
        # Note: portal API queries to the key status endpoint return a value
        # of the form: [{<fingerprint>: value, <status>: value}, ...]
        return {
            key["fingerprint"]: KeyStatus(key["status"]) for key in json.loads(response)
        }

    def verify_key_approval(self, fingerprints: Iterable[str]) -> None:
        """Verify that the PGP keys are approved by the central authority.

        Verification of key approval is done via a call to the portal API.

        :param fingerprints: fingerprints of PGP keys to verify.
        :raises RuntimeError: if one or more keys are not approved.
        """
        # Get the status of the key(s) to be verified from the portal.
        unique_fingerprints = set(fingerprints)
        key_statuses = self.get_key_status(unique_fingerprints)

        # If one or more keys are not approved, display an error message.
        non_approved_keys = ", ".join(
            f"{fingerprint} [{key_statuses[fingerprint].value}]"
            for fingerprint in unique_fingerprints
            if key_statuses[fingerprint] is not KeyStatus.APPROVED
        )
        if non_approved_keys:
            raise RuntimeError(
                "The following keys are not approved and cannot be used to "
                f"encrypt/decrypt data: {non_approved_keys}"
            )

    def verify_dpkg_metadata(self, metadata: MetaData, file_name: str) -> str:
        """Verify a DTR (data transfer request) ID number using the portal API.

        Return the "project code" of the project to which the DTR belongs if the
        DTR ID is valid.

        :param MetaData: MetaData object corresponding to the metadata file of
            the data package to check.
        :param file_name: name of data package file.
        :raises RuntimeError: if the DTR ID is not-approved, if the data in the
            metadata does not match with project the DTR ID belongs to (e.g.
            wrong data sender or recipient), or if any other error occurs (e.g.
            portal server is not reachable).
        """
        response = _handle_errors(self._post)(
            url=self.dpkg_check_endpoint,
            data=json.dumps(
                {
                    "file_name": file_name,
                    "metadata": json.dumps(MetaData.asdict(metadata)),
                }
            ).encode(),
        )
        try:
            project_code: str = json.loads(response)["project_code"]
            return project_code
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(
                "PortalApi.verify_dpkg_metadata: got invalid json from portal: "
                + response.decode()
            ) from e
        except KeyError as e:
            raise RuntimeError(
                "PortalApi.verify_dpkg_metadata: json response from portal "
                "does not include field `project_code`: " + response.decode()
            ) from e

    def log_dpkg_status(
        self,
        status: DPKGStatus,
        metadata: MetaData,
        file_name: str,
        node: str,
    ) -> DpkgInfo:
        """Connect to the portal Api to log the status of a data package.

        Connecting to the portal endpoint for package logging allows to
        record the status of a package into the portal database.
        """
        response = _handle_errors(self._post)(
            url=self.dpkg_log_endpoint,
            data=json.dumps(
                {
                    "file_name": file_name,
                    "metadata": json.dumps(MetaData.asdict(metadata)),
                    "node": node.lower(),
                    "status": status.value,
                }
            ).encode(),
            headers=self.auth_header(),
        )
        try:
            dpkg_info: Dict[str, str] = json.loads(response)
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(
                "PortalApi.log_dpkg_status: got invalid json from portal: "
                + response.decode()
            ) from e

        try:
            return DpkgInfo.from_dict(dpkg_info)
        except ValueError as e:
            raise RuntimeError(
                "PortalApi.log_dpkg_status: json response from portal "
                f"is missing one or more expected fields. {e}. "
                f"{response.decode()}."
            ) from e


R = TypeVar("R")


def _handle_errors(f: Callable[..., R]) -> Callable[..., R]:
    @wraps(f)
    def _f(*args: Any, **kwargs: Any) -> R:
        try:
            return f(*args, **kwargs)
        except HTTPError as e:
            msg_raw = e.read()
            try:
                msg = json.loads(msg_raw)["detail"]
            except (json.decoder.JSONDecodeError, KeyError, TypeError):
                msg = msg_raw.decode()
            raise RuntimeError("PortalApi: " + msg) from e
        except URLError:
            raise RuntimeError("Could not connect to the server.") from None

    return _f
