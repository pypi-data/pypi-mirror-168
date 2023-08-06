import base64
import json
from contextlib import nullcontext as does_not_raise
from email.message import Message
from io import BytesIO
from typing import Any, Iterable, Union, Dict
from unittest import mock
from urllib.error import HTTPError, URLError

import pytest
from libbiomedit.portal import DPKGStatus, DpkgInfo, KeyStatus, PortalApi
from libbiomedit.metadata import MetaData, Purpose

CN_FINGERPRINT = "CCBBAADD08ECCECCECCECCDD3A6500D5C1DE39AC"
SGT_HARTMANN_FINGERPRINT = CN_FINGERPRINT[::-1]
A_FINGERPRINT = "A" * 40
B_FINGERPRINT = "B" * 40
C_FINGERPRINT = "C" * 40
D_FINGERPRINT = "D" * 40
E_FINGERPRINT = "D" * 40
F_FINGERPRINT = "D" * 40
CN_PASSWORD = "Chuck Norris needs no password, he IS the password!"
STATUS_BY_FINGERPRINT = {
    A_FINGERPRINT: "APPROVED",
    B_FINGERPRINT: "APPROVAL_REVOKED",
    C_FINGERPRINT: "DELETED",
    D_FINGERPRINT: "KEY_REVOKED",
    E_FINGERPRINT: "PENDING",
    F_FINGERPRINT: "REJECTED",
    SGT_HARTMANN_FINGERPRINT: "UNKNOWN_KEY",
    CN_FINGERPRINT: "APPROVED",
}
TEST_METADATA_DICT: Dict[str, Any] = {
    "sender": CN_FINGERPRINT,
    "recipients": [CN_FINGERPRINT, SGT_HARTMANN_FINGERPRINT],
    "checksum": "abcdef0123456789" * 4,
    "timestamp": "2022-02-02T11:33:55+0100",
    "version": MetaData.version,
    "checksum_algorithm": "SHA256",
    "compression_algorithm": "gzip",
    "transfer_id": 23,
    "purpose": Purpose.TEST.value,
}
TEST_PORTAL_API = PortalApi(
    base_url="https://fake.portal.org",
    username="chuck.norris",
    password="RoundhouseKick",
)
TEST_METADATA = MetaData.from_dict(TEST_METADATA_DICT)
TEST_FILE_NAME = "20220816T090807.zip"


def mock_key_status_response(
    data: str,
    url: str,  # pylint: disable=unused-argument
) -> str:
    """Mock function that emulates the response from the key status
    portal API endpoint.
    """
    fingerprints = json.loads(data)["fingerprints"]
    return json.dumps(
        [
            {"fingerprint": fpr, "status": STATUS_BY_FINGERPRINT[fpr]}
            for fpr in fingerprints
        ]
    )


def mock_post_method(
    server_return_value: Dict[str, str], raise_http_error: bool = False
) -> mock.Mock:
    """Return a mock object that fakes the "_post()" method of PortalApi."""

    # If the mock POST call should return an error, a mock side_effect is set.
    if raise_http_error:
        side_effect = HTTPError(
            url="https://fake.portal.org",
            code=400,
            msg="Bad request",
            hdrs=Message(),
            fp=BytesIO(b'{"detail": "Invalid transfer"}'),
        )
    else:
        side_effect = None

    # Encode the mocked return values from the POST request as JSON. A special
    # case is if the data to return contains "bad" as a key: this indicates
    # that a badly formatted JSON should be returned.
    if "bad" in server_return_value:
        return_value = b"Invalid JSON string..."
    else:
        return_value = json.dumps(server_return_value).encode()

    return mock.Mock(return_value=return_value, side_effect=side_effect)


def test_post() -> None:
    """Test the _post private method of the PortalApi."""

    server_response = b"return value..."

    class MockHTTPResponse(mock.Mock):
        def read(self) -> bytes:
            return server_response

    mock_urlopen = mock.MagicMock()
    mock_urlopen.return_value.__enter__.return_value = MockHTTPResponse()

    portal_api = PortalApi()
    with mock.patch.object(portal_api, "urlopen", mock_urlopen):
        response = portal_api._post(  # pylint: disable=protected-access
            url="https://example.com/endpoint", data=b"..."
        )
        assert response == server_response


@pytest.mark.parametrize("endpoint_name", ["pgpkey_status", "dpkg_check", "dpkg_log"])
def test_endpoint_url(endpoint_name: str) -> None:
    """Test the PortalApi's properties dedicated to provide endpoint URLs."""

    # Create a new PortalApi object with the value of the endpoint we are
    # currently testing overridden.
    portal_api = PortalApi(base_url="https://test.com")
    setattr(portal_api, endpoint_name, "/backend/test/endpoint/")

    # Call the property for the current endpoint we are testing, and check that
    # it evaluates to the expected value.
    endpoint_url = getattr(portal_api, f"{endpoint_name}_endpoint")
    assert endpoint_url == "https://test.com/backend/test/endpoint/"


@pytest.mark.parametrize(
    "fingerprints",
    [
        (A_FINGERPRINT,),
        (A_FINGERPRINT, CN_FINGERPRINT),
        (A_FINGERPRINT, SGT_HARTMANN_FINGERPRINT),
        (B_FINGERPRINT, C_FINGERPRINT, D_FINGERPRINT, E_FINGERPRINT, F_FINGERPRINT),
        (A_FINGERPRINT, A_FINGERPRINT, B_FINGERPRINT, B_FINGERPRINT),
    ],
)
def test_get_key_status(fingerprints: Iterable[str]) -> None:
    """Test that the Portal API is able to retrieve the status of a key from
    the portal.
    """
    portal_api = PortalApi()
    with mock.patch.object(portal_api, "_post", mock_key_status_response):
        status = portal_api.get_key_status(fingerprints=fingerprints)
        for fingerprint in fingerprints:
            # Check that the correct value is returned.
            assert status[fingerprint] == KeyStatus(STATUS_BY_FINGERPRINT[fingerprint])

            # Check there are no duplicates.
            assert len(status.keys()) == len(set(fingerprints))


@pytest.mark.parametrize(
    "fingerprints, expectation",
    [
        # Test that should pass:
        # * All keys are approved.
        [(A_FINGERPRINT,), does_not_raise()],
        [(A_FINGERPRINT, CN_FINGERPRINT), does_not_raise()],
        [
            (A_FINGERPRINT, CN_FINGERPRINT, CN_FINGERPRINT, CN_FINGERPRINT),
            does_not_raise(),
        ],
        # * Approved keys fingerprints are passed via a generator.
        [(x for x in (A_FINGERPRINT, CN_FINGERPRINT)), does_not_raise()],
        #
        # Tests that should raise an error:
        # * One or more keys are not approved.
        [
            (SGT_HARTMANN_FINGERPRINT,),
            pytest.raises(RuntimeError, match="not approved"),
        ],
        [
            (SGT_HARTMANN_FINGERPRINT, CN_FINGERPRINT, A_FINGERPRINT),
            pytest.raises(RuntimeError, match="not approved"),
        ],
        # * Non-approved keys fingerprints are passed via a generator.
        [
            (x for x in (SGT_HARTMANN_FINGERPRINT, CN_FINGERPRINT)),
            pytest.raises(RuntimeError, match="not approved"),
        ],
    ],
)
def test_verify_key_approval(fingerprints: Iterable[str], expectation: Any) -> None:
    """Test that the Portal API is able to tell if a key is approved or not."""
    portal_api = PortalApi()
    with mock.patch.object(portal_api, "_post", mock_key_status_response), expectation:
        portal_api.verify_key_approval(fingerprints=fingerprints)


@pytest.mark.parametrize(
    "username, password",
    [
        ("chuck_norris", CN_PASSWORD),
        ("chuck_norris", None),
        (None, CN_PASSWORD),
        (None, None),
    ],
)
def test_auth_header(username: str, password: str) -> None:
    """Test the authentication headers are properly generated"""
    expected_auth_header = (
        {
            "Authorization": "Basic "
            + base64.b64encode(f"{username}:{password}".encode()).decode()
        }
        if username and password
        else {}
    )
    portal_api = PortalApi(username=username, password=password)
    assert portal_api.auth_header() == expected_auth_header


@pytest.mark.parametrize(
    "error_type, expectation",
    [
        ["http", pytest.raises(RuntimeError, match="Invalid PGP fingerprint")],
        ["url", pytest.raises(RuntimeError, match="Could not connect to the server")],
    ],
)
def test_handle_errors(error_type: str, expectation: Any) -> None:
    """Test that the error handling of post requests is made properly."""
    side_effect: Union[HTTPError, URLError]
    if error_type == "http":
        side_effect = HTTPError(
            url="example.org/endpoint",
            code=400,
            msg="Invalid PGP fingerprint",
            hdrs=Message(),
            fp=BytesIO(b'{"fingerprints": "Invalid PGP fingerprint"}'),
        )
    else:
        side_effect = URLError(reason="service unavailable")

    portal_api = PortalApi()
    with expectation, mock.patch.object(portal_api, "_post") as mock_post:
        mock_post.side_effect = side_effect
        _ = portal_api.get_key_status(fingerprints=["BAD VALUE"])


@pytest.mark.parametrize(
    "server_return_value, raise_http_error, expectation",
    [
        # Tests that should pass:
        [{"project_code": "007"}, False, does_not_raise()],
        #
        # Tests that should raise an error:
        # * Server generates an HTTPError.
        [
            {"project_code": "007"},
            True,
            pytest.raises(RuntimeError, match="PortalApi: Invalid transfer"),
        ],
        # * Server returns unexpected field in JSON.
        [
            {"bad_field": "007"},
            False,
            pytest.raises(
                RuntimeError, match="response from portal does not include field"
            ),
        ],
        # * Server returns bad JSON.
        [
            {"bad": "json"},
            False,
            pytest.raises(RuntimeError, match="got invalid json from portal"),
        ],
    ],
)
def test_verify_dpkg_metadata(
    server_return_value: Dict[str, str],
    raise_http_error: bool,
    expectation: Any,
) -> None:
    """Test that the Portal API is able to check data package metadata."""

    # Create a mock to impersonate the "_post" method of PortalApi.
    mock_post = mock_post_method(server_return_value, raise_http_error)

    with mock.patch.object(TEST_PORTAL_API, "_post", mock_post), expectation:
        code = TEST_PORTAL_API.verify_dpkg_metadata(
            metadata=TEST_METADATA, file_name=TEST_FILE_NAME
        )
        assert code == "007"
        mock_post.assert_called_once_with(
            url=TEST_PORTAL_API.dpkg_check_endpoint,
            data=json.dumps(
                {
                    "file_name": TEST_FILE_NAME,
                    "metadata": json.dumps(TEST_METADATA_DICT),
                }
            ).encode(),
        )


dpkg_info_partial = {"destination_node": "dest_node", "project_code": "007"}
dpkg_info_full = {**dpkg_info_partial, "data_provider": "chuck_norris"}
dpkg_info_bad_field = {**dpkg_info_partial, "bad_field": "an unexpected field"}
dpkg_info_missing_field = {"destination_node": "dest_node"}


@pytest.mark.parametrize(
    "server_return_value, raise_http_error, expectation",
    [
        # Tests that should pass:
        # * Full data package info is returned by server.
        [dpkg_info_full, False, does_not_raise()],
        # * Only partial info is returned, but all mandatory fields are there.
        [dpkg_info_partial, False, does_not_raise()],
        # * A bad field is present in addition of regular fields.
        [dpkg_info_bad_field, False, does_not_raise()],
        #
        # Tests that should raise an error:
        # * Server generates an HTTPError.
        [
            dpkg_info_full,
            True,
            pytest.raises(RuntimeError, match="PortalApi: Invalid transfer"),
        ],
        # * Server returns bad JSON.
        [
            {"bad": "json"},
            False,
            pytest.raises(RuntimeError, match="got invalid json from portal"),
        ],
        # * Server return value misses a required field.
        [
            dpkg_info_missing_field,
            False,
            pytest.raises(
                RuntimeError,
                match="response from portal is missing one or more expected fields",
            ),
        ],
    ],
)
def test_log_dpkg_status(
    server_return_value: Dict[str, str],
    raise_http_error: bool,
    expectation: Any,
) -> None:
    """Test that the Portal API is able to log a data package status."""

    # Create a mock to impersonate the "_post" method of PortalApi.
    mock_post = mock_post_method(server_return_value, raise_http_error)
    test_node = "Node_Code"
    test_status = DPKGStatus.ENTER

    with mock.patch.object(TEST_PORTAL_API, "_post", mock_post), expectation:
        package_info = TEST_PORTAL_API.log_dpkg_status(
            status=test_status,
            metadata=TEST_METADATA,
            file_name=TEST_FILE_NAME,
            node=test_node,
        )

        # Note at this point, server_return_value is always a dict, because
        # otherwise an error was already raised in the call to
        # log_dpkg_status() above. This check is for helping mypy realize this.
        assert isinstance(server_return_value, dict)

        assert package_info == DpkgInfo.from_dict(server_return_value)
        mock_post.assert_called_once_with(
            url=TEST_PORTAL_API.dpkg_log_endpoint,
            data=json.dumps(
                {
                    "file_name": TEST_FILE_NAME,
                    "metadata": json.dumps(MetaData.asdict(TEST_METADATA)),
                    "node": test_node.lower(),
                    "status": test_status.value,
                }
            ).encode(),
            headers=TEST_PORTAL_API.auth_header(),
        )
