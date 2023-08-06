import contextlib
from contextlib import nullcontext as does_not_raise
import json
from unittest import mock
from typing import (
    Optional,
    Any,
    Sequence,
    Dict,
    Iterable,
    List,
    Generator,
    cast,
)
import pytest
import gpg_lite as gpg

from libbiomedit import crypt
from libbiomedit.metadata import METADATA_FILE, METADATA_FILE_SIG

CN_EMAIL = "chuck.norris@roundhouse.gov"
CN_UID = gpg.Uid(full_name="Chuck Norris", email=CN_EMAIL)
CN_FINGERPRINT = "CCBBAADD08ECCECCECCECCDD3A6500D5C1DE39AC"
CN_SUBKEY_FINGERPRINT = "55C5314BB9EFD19AE7CC4774D892C41917B20115"
CN_SIGNATURE = gpg.Signature(
    issuer_uid=CN_UID,
    issuer_key_id=CN_FINGERPRINT[-16:],
    issuer_fingerprint=CN_FINGERPRINT,
    creation_date="1550241679",
    signature_class="13x",
    validity=gpg.model.SignatureValidity.good,
)
KEYSERVER = "http://hagrid.hogwarts.org"
A_UID = gpg.Uid(full_name="Alice", email="alice@redqueen.org")
B_UID = gpg.Uid(full_name="Bob", email="bob@example.org")
C_UID = gpg.Uid(full_name="Sgt Hartmann", email=CN_EMAIL)
D_UID = gpg.Uid(full_name="Doug", email=CN_EMAIL)
A_FINGERPRINT = "A" * 40
B_FINGERPRINT = "B" * 40
C_FINGERPRINT = "C" * 40
D_FINGERPRINT = "D" * 40

# Base data to generate default "user" PGP keys.
def mock_key(**kwargs: Any) -> gpg.Key:
    """Generate a mock PGP key."""

    mock_data = dict(
        key_id=CN_FINGERPRINT[-16:],
        fingerprint=CN_FINGERPRINT,
        validity=gpg.Validity.ultimately_valid,
        key_length=4096,
        pub_key_algorithm=1,
        creation_date="1550241679",
        uids=(CN_UID,),
        owner_trust="u",
        key_type=gpg.KeyType.public,
        origin=KEYSERVER,
        signatures=(CN_SIGNATURE,),
        key_capabilities=frozenset(
            (
                gpg.KeyCapability.sign,
                gpg.KeyCapability.certify,
                gpg.KeyCapability.encrypt,
            )
        ),
        sub_keys=(),
    )

    return gpg.Key(**cast(Dict[str, Any], {**mock_data, **kwargs}))


def mock_subkey(fingerprint: str) -> gpg.SubKey:
    return gpg.SubKey(
        key_type=gpg.KeyType.public,
        key_id=fingerprint[-16:],
        fingerprint=fingerprint,
        validity=gpg.Validity.ultimately_valid,
        key_length=4096,
        pub_key_algorithm=1,
        creation_date="1550241679",
        key_capabilities=frozenset((gpg.KeyCapability.encrypt,)),
    )


SUBKEY_CN = mock_subkey(CN_SUBKEY_FINGERPRINT)
SUBKEY_A = mock_subkey("ABCD" * 10)
KEY_CN = mock_key(sub_keys=(SUBKEY_CN,))
KEY_A = mock_key(
    fingerprint=A_FINGERPRINT,
    key_id=A_FINGERPRINT[-16:],
    uids=(A_UID,),
    sub_keys=(SUBKEY_A,),
)
KEY_B = mock_key(fingerprint=B_FINGERPRINT, key_id=B_FINGERPRINT[-16:], uids=(B_UID,))
KEY_C = mock_key(fingerprint=C_FINGERPRINT, key_id=C_FINGERPRINT[-16:], uids=(C_UID,))
KEY_D = mock_key(fingerprint=D_FINGERPRINT, key_id=D_FINGERPRINT[-16:], uids=(D_UID,))
CN_REVOKED_SUBKEY_FINGERPRINT = "0" * 40
KEY_CN_REVOKED = mock_key(
    fingerprint="F" * 40,
    validity=gpg.Validity.revoked,
    sub_keys=(CN_REVOKED_SUBKEY_FINGERPRINT,),
)
KEY_NO_ORIGIN = mock_key(origin=None)


class MockGPGStore(mock.Mock):
    """A mock GPG store instance.
    * local_keys: keys that are in the user's local keyring.
    * keyserver_keys: keys that are available on the keyserver.
    """

    def __init__(
        self,
        local_keys: List[gpg.Key],
        keyserver_keys: Sequence[gpg.Key],
        detached_sig_signee: str = CN_FINGERPRINT,
    ):
        super().__init__()
        self.local_keys = local_keys
        self.keyserver_keys = keyserver_keys
        self.download_count = 0
        self.detached_sig_signee = detached_sig_signee

    def list_pub_keys(
        self,
        search_terms: Iterable[str],
        sigs: bool = True,  # pylint: disable=unused-argument
    ) -> Sequence[gpg.Key]:
        """Return the list of local keys where the search term matches either
        the email, the fingerprint of the key ID.
        """
        # Make sure that a valid search term was passed.
        for x in search_terms:
            if "@" not in x and len(x) != 40 and len(x) != 16:
                raise ValueError(f"invalid search term: [{x}]!")

        # Return the keys that match one of the search terms.
        return [
            key
            for key in self.local_keys
            if any(
                (
                    key.fingerprint.endswith(x)
                    or key.uids[0].email == x
                    or any(subkey.fingerprint == x for subkey in key.sub_keys)
                )
                for x in search_terms
            )
        ]

    def vks_recv_key(
        self,
        identifier: str,
        keyserver: str,
        url_opener: crypt.URL_OPENER_TYPE = crypt.DEFAULT_URL_OPENER,  # pylint: disable=unused-argument
    ) -> None:
        """Add the requested keys to the local keys if they are present in
        the keyserver_keys list. This simulates key download.
        """
        received_keys = [
            key for key in self.keyserver_keys if key.fingerprint == identifier
        ]
        self.local_keys.extend(
            key for key in received_keys if key not in self.local_keys
        )
        # If a key was not found on the mock keyserver, raise an error.
        if not received_keys:
            raise gpg.KeyserverKeyNotFoundError(
                fingerprint=identifier, keyserver=keyserver
            )
        # Increment counter that keeps track of how many files where downloaded.
        self.download_count += 1

    def import_file(self, *args: Any, **kwargs: Any) -> None:
        pass

    def vks_get_key_by_fingerprint(
        self,
        keyserver: str,
        fingerprint: str,
        url_opener: crypt.URL_OPENER_TYPE = crypt.DEFAULT_URL_OPENER,  # pylint: disable=unused-argument
    ) -> mock.Mock:
        """Wrapper around vks_recv_key that only download keys specified
        via their fingerprint.
        """
        if len(fingerprint) < 40:
            raise RuntimeError("Not a valid PGP fingerprint")
        self.vks_recv_key(identifier=fingerprint, keyserver=keyserver)
        return mock.Mock()

    def verify_detached_sig(
        self,
        src: bytes,  # pylint: disable=unused-argument
        sig: bytes,
    ) -> str:
        """If the signature is valid, return the signee's fingerprint."""
        if sig != b"valid":
            raise gpg.GPGError("Invalid signature")
        return self.detached_sig_signee


class MockArchiveReader:
    """A mock .tar file reader that returns mock objects instead of files.
    The mock archive reader also store the information of whether a detached
    signature file is valid or not.
    """

    def __init__(
        self,
        metadata_file_content: bytes = b"fake data",
        signature_file_content: bytes = b"valid",
    ):
        self.signature = signature_file_content
        self.metadata = metadata_file_content
        self.contents = {
            METADATA_FILE: metadata_file_content,
            METADATA_FILE_SIG: signature_file_content,
        }

    def extract_member(self, name: str) -> mock.Mock:
        if name.endswith(".sig"):
            if self.signature == b"no detached signature file":
                raise ValueError("No detached sig file in this archive")
            file_content = self.signature
        else:
            if self.metadata == b"no metadata file":
                raise ValueError("No metadata file in this archive")
            file_content = self.metadata

        # Return a IOBytes like mock object that has a .read() method.
        mock_file = mock.Mock()
        mock_file.read = mock.Mock(return_value=file_content)
        return mock_file

    def __repr__(self) -> str:
        assert self.metadata is not None and self.signature is not None  # for mypy
        return f"MockArchiveReader({self.metadata.decode()}, {self.signature.decode()})"


@pytest.mark.parametrize("full_fingerprint", [True, False])
def test_pgp_key_as_str(full_fingerprint: bool) -> None:
    """Verify that the rendering of keys as strings works as expected."""

    expected_str_representation = (
        f"{CN_UID.full_name} <{CN_UID.email}> "
        f"[{CN_FINGERPRINT if full_fingerprint else CN_FINGERPRINT[-16:]}]"
    )
    assert (
        crypt.pgp_key_as_str(KEY_CN, full_fingerprint=full_fingerprint)
        == expected_str_representation
    )


@pytest.mark.parametrize(
    "test_fingerprint, expectation",
    [
        # Test valid fingerprint.
        [CN_FINGERPRINT, does_not_raise()],
        #
        # Test invalid fingerprints.
        [
            CN_FINGERPRINT[-16:],
            pytest.raises(RuntimeError, match="Invalid fingerprint"),
        ],
        ["BAD FINGERPRINT", pytest.raises(RuntimeError, match="Invalid fingerprint")],
        ["A" * 39 + "G", pytest.raises(RuntimeError, match="Invalid fingerprint")],
    ],
)
def test_assert_is_pgp_fingerprint(test_fingerprint: str, expectation: Any) -> None:
    """Verify that valid/invalid fingerprints are detected properly."""
    with expectation:
        crypt.assert_is_pgp_fingerprint(test_fingerprint)


@pytest.mark.parametrize(
    "key, expectation",
    [
        # Tests that should PASS:
        #  * using a non-revoked key.
        [KEY_CN, does_not_raise()],
        #
        # Tests that should RAISE AN ERROR:
        #  * a user-revoked key should raise an error.
        [KEY_CN_REVOKED, pytest.raises(RuntimeError, match="key has been revoked")],
    ],
)
def test_assert_key_not_revoked(
    key: gpg.Key,
    expectation: Any,
) -> None:
    """Verify that a user-revoked key raises an error."""

    with expectation:
        crypt.assert_key_not_revoked(key)


@pytest.mark.parametrize(
    "fingerprint_to_download, expectation",
    [
        # Tests that should PASS:
        # * If a key exists on the keyserver, it gets downloaded as expected.
        [A_FINGERPRINT, does_not_raise()],
        #
        # Tests that should raise an ERROR:
        # * When a key is not found on the keyserver, an error is raised.
        [
            D_FINGERPRINT,
            pytest.raises(
                RuntimeError,
                match=f"Download of key \\[{D_FINGERPRINT}\\] "
                f"from \\[{KEYSERVER}\\] failed",
            ),
        ],
    ],
)
def test_download_key_by_fingerprint(
    fingerprint_to_download: str,
    expectation: Any,
) -> None:

    # Create a fake GPGStore object (a local keyring).
    local_keys = [KEY_CN]
    keyserver_keys = [KEY_A, KEY_B]
    gpg_store = MockGPGStore(local_keys, keyserver_keys)

    # Test function.
    with mock.patch(
        "gpg_lite.keyserver.vks_get_key_by_fingerprint",
        gpg_store.vks_get_key_by_fingerprint,
    ), expectation:
        crypt.download_key_by_fingerprint(
            fingerprint=fingerprint_to_download,
            gpg_store=gpg_store,
            keyserver_url=KEYSERVER,
            sigs=True,
        )


does_not_warn = does_not_raise


@pytest.mark.parametrize(
    "key_identifiers, local_keys, keyserver_keys, keyserver_url, "
    "allow_download, expected_download_count, expectation, warning",
    [
        # Tests that should PASS:
        #  * All keys are present in the local keyring and the keyserver.
        #    Keys get retrieved successfully and refreshed.
        #    (expected_download_count = 0)
        [
            [A_FINGERPRINT, B_FINGERPRINT, C_FINGERPRINT, D_FINGERPRINT],
            [KEY_A, KEY_B, KEY_C, KEY_D],
            [KEY_A, KEY_B, KEY_C, KEY_D],
            KEYSERVER,
            True,
            4,
            does_not_raise(),
            does_not_warn(),
        ],
        [
            [CN_FINGERPRINT, CN_FINGERPRINT],
            [KEY_CN],
            [KEY_CN, KEY_A],
            KEYSERVER,
            True,
            2,
            does_not_raise(),
            does_not_warn(),
        ],
        # * Keys are not refreshed if there is either no keyserver specified,
        #   download is not allowed, or keys are not present on the keyserver.
        [
            [CN_FINGERPRINT],
            [KEY_CN],
            [KEY_CN],
            None,
            True,
            0,
            does_not_raise(),
            does_not_warn(),
        ],
        [
            [CN_FINGERPRINT],
            [KEY_CN],
            [KEY_CN],
            KEYSERVER,
            False,
            0,
            does_not_raise(),
            does_not_warn(),
        ],
        [
            [CN_FINGERPRINT],
            [KEY_CN],
            [],
            KEYSERVER,
            True,
            0,
            does_not_raise(),
            pytest.warns(
                UserWarning,
                match=rf"could not be refreshed:.*{CN_FINGERPRINT}",
            ),
        ],
        # * If a key is missing, it gets downloaded from the keyserver.
        [
            [CN_FINGERPRINT, A_FINGERPRINT],
            [KEY_B, KEY_C],
            [KEY_CN, KEY_A],
            KEYSERVER,
            True,
            2,
            does_not_raise(),
            does_not_warn(),
        ],
        #
        # Tests that should raise an ERROR:
        #  * One or more keys are missing from local keyring and no keyserver.
        [
            [CN_FINGERPRINT, A_FINGERPRINT],
            [KEY_A, KEY_B],
            [],
            None,
            True,
            0,
            pytest.raises(RuntimeError, match="no keyserver URL is provided"),
            does_not_warn(),
        ],
        # * One or more keys are missing from both local keyring and keyserver.
        [
            [CN_FINGERPRINT, A_FINGERPRINT],
            [KEY_A, KEY_B],
            [KEY_A, KEY_B],
            KEYSERVER,
            True,
            0,
            pytest.raises(
                RuntimeError,
                match=f"Download of key \\[{CN_FINGERPRINT}\\] "
                f"from \\[{KEYSERVER}\\] failed",
            ),
            does_not_warn(),
        ],
        # * One or more keys are missing and auto-download is disabled.
        #   (when key download is disabled, keys are not downloaded and
        #   therefore a missing local key raises an error, even if the key
        #   is present on the keyserver).
        [
            [CN_FINGERPRINT, A_FINGERPRINT],
            [KEY_B, KEY_C],
            [KEY_CN, KEY_A],
            KEYSERVER,
            False,
            0,
            pytest.raises(RuntimeError, match="key download is disabled"),
            does_not_warn(),
        ],
        # * Only keys specified via their fingerprint can be downloaded from
        #   the keyserver.
        [
            [CN_EMAIL],
            [KEY_A],
            [KEY_CN],
            KEYSERVER,
            True,
            0,
            pytest.raises(
                RuntimeError,
                match="only keys specified via their full fingerprint "
                "can be auto-downloaded",
            ),
            does_not_warn(),
        ],
        # * The search term matches multiples keys in the local keyring.
        #   (KEY_C and KEY_D have the same email as KEY_CN).
        [
            [CN_EMAIL],
            [KEY_CN, KEY_C, KEY_D],
            [],
            KEYSERVER,
            True,
            0,
            pytest.raises(
                RuntimeError,
                match="more than one key in your local keyring "
                f"matches with \\[{CN_EMAIL}\\]",
            ),
            does_not_warn(),
        ],
        # * A revoked key (KEY_CN_REVOKED) raises an error.
        [
            [CN_EMAIL],
            [KEY_CN_REVOKED, KEY_A],
            [KEY_CN_REVOKED],
            KEYSERVER,
            True,
            0,
            pytest.raises(RuntimeError, match="key has been revoked"),
            does_not_warn(),
        ],
    ],
)
def test_retrieve_and_refresh_keys(
    key_identifiers: List[str],
    local_keys: List[gpg.Key],
    keyserver_keys: List[gpg.Key],
    keyserver_url: Optional[str],
    allow_download: bool,
    expected_download_count: int,
    expectation: Any,
    warning: Any,
) -> None:
    """Verify that keys are downloaded/refreshed as expected."""

    gpg_store = MockGPGStore(local_keys, keyserver_keys)

    def mock_vks_get_key_by_fingerprint(keyserver: str, fingerprint: str) -> mock.Mock:
        if len(fingerprint) < 40:
            raise RuntimeError("Not a valid PGP fingerprint")
        gpg_store.vks_recv_key(identifier=fingerprint, keyserver=keyserver)
        return mock.Mock()

    with mock.patch(
        "gpg_lite.keyserver.vks_get_key_by_fingerprint", mock_vks_get_key_by_fingerprint
    ):

        with expectation, warning:
            refreshed_keys = crypt.retrieve_and_refresh_keys(
                key_identifiers=key_identifiers,
                gpg_store=gpg_store,
                keyserver_url=keyserver_url,
                allow_key_download=allow_download,
            )
            # Check that keys are returned in the same order as input search terms.
            assert key_identifiers == [key.fingerprint for key in refreshed_keys]

            # If keys are supposed to be downloaded or refreshed, verify that
            # this was really done.
            assert gpg_store.download_count == expected_download_count


@pytest.mark.parametrize(
    "metadata_content, signature_file_content, detached_sig_signee, expectation",
    [
        # Tests that should PASS:
        #  * An archive containing valid data is passed. The fingerprint from
        #    the data sender as given in the metadata file matches the
        #    fingerprint from the detached signature file.
        [{"sender": CN_FINGERPRINT}, b"valid", CN_FINGERPRINT, does_not_raise()],
        #  * An archive containing valid data is passed and a subkey was used
        #    to create the detached signature file.
        [{"sender": CN_FINGERPRINT}, b"valid", CN_SUBKEY_FINGERPRINT, does_not_raise()],
        #
        # Tests that should RAISE AN ERROR:
        #  * Missing metadata.json file.
        [
            None,
            b"valid",
            CN_FINGERPRINT,
            pytest.raises(RuntimeError, match=f"'{METADATA_FILE}' file is missing"),
        ],
        #  * Missing detached signature file.
        [
            {"sender": CN_FINGERPRINT},
            b"no detached signature file",
            CN_FINGERPRINT,
            pytest.raises(
                RuntimeError, match=f"signature file '{METADATA_FILE_SIG}' is missing"
            ),
        ],
        #  * Archive contains an invalid signature.
        [
            {"sender": CN_FINGERPRINT},
            b"invalid",
            CN_FINGERPRINT,
            pytest.raises(RuntimeError, match="signature is invalid"),
        ],
        #  * The fingerprints from the metadata file and the detached signature
        #    do not match and the detached signature was not made with a
        #    subkey of the key indicated under "sender".
        [
            {"sender": A_FINGERPRINT},
            b"valid",
            CN_FINGERPRINT,
            pytest.raises(
                RuntimeError,
                match=f"the key '{CN_FINGERPRINT}' used to sign the metadata "
                "file does not match the key associated with the data sender "
                f"fingerprint '{A_FINGERPRINT}'",
            ),
        ],
        #  * The fingerprints from the metadata file and the detached signature
        #    do not match, and the key from the detached signature is not found
        #    in the user's local keyring.
        [
            {"sender": A_FINGERPRINT},
            b"valid",
            "ABCDEF0123" * 4,
            pytest.raises(
                RuntimeError,
                match=f"public key '{'ABCDEF0123' * 4}' is not available in "
                "local keyring.",
            ),
        ],
        #  * The "sender" field is missing from the metadata.json file.
        [
            {},
            b"valid",
            CN_FINGERPRINT,
            pytest.raises(RuntimeError, match=f"Invalid {METADATA_FILE}:"),
        ],
        #  * The sender in the metadata.json file is not a valid fingerprint.
        [
            {"sender": "bad fingerprint"},
            b"valid",
            CN_FINGERPRINT,
            pytest.raises(RuntimeError, match=f"Invalid {METADATA_FILE}:"),
        ],
        #  * PGP key of data sender is user-revoked.
        [
            {"sender": KEY_CN_REVOKED.fingerprint},
            b"valid",
            CN_FINGERPRINT,
            pytest.raises(RuntimeError, match="signee's key is invalid"),
        ],
        #  * Detached signature was made with a subkey of a revoked PGP key.
        [
            {"sender": CN_REVOKED_SUBKEY_FINGERPRINT},
            b"valid",
            CN_FINGERPRINT,
            pytest.raises(RuntimeError, match="signee's key is invalid"),
        ],
    ],
)
def test_verify_metadata_signature(
    metadata_content: Optional[Dict[str, str]],
    signature_file_content: bytes,
    detached_sig_signee: str,
    expectation: Any,
) -> None:
    """Verify that data package metadata are signed as expected."""

    @contextlib.contextmanager
    def mock_archive_reader_init(f: Any) -> Generator[mock.Mock, None, None]:
        yield mock_archive_open_obj(f)  # pylint: disable=cell-var-from-loop

    # Special case: simulate the scenario where the metadata file is missing.
    if metadata_content is None:
        metadata_file_content = b"no metadata file"
    # Regular case: a metadata file is present.
    else:
        test_metadata = {
            "recipients": [CN_FINGERPRINT, A_FINGERPRINT, B_FINGERPRINT],
            "checksum": "fade655fd178c7fd03d8b52f9350cae9076b532622bc0794f147418a289b7cad",
            "timestamp": "2022-02-01T14:13:45+0100",
            "version": "0.7.1",
            "checksum_algorithm": "SHA256",
            "compression_algorithm": "gzip",
            "transfer_id": 7,
            "purpose": "TEST",
        }
        test_metadata.update(metadata_content)
        metadata_file_content = json.dumps(test_metadata).encode()

    mock_archive = MockArchiveReader(metadata_file_content, signature_file_content)
    mock_archive_open_obj = mock.Mock(return_value=mock_archive)
    mock_gpg_store = MockGPGStore(
        local_keys=[KEY_CN, KEY_A, KEY_B, KEY_C, KEY_D],
        keyserver_keys=[KEY_CN_REVOKED],
        detached_sig_signee=detached_sig_signee,
    )

    # Run function to test.
    with mock.patch(
        "libbiomedit.crypt.archive_reader", mock_archive_reader_init
    ), expectation:
        crypt.verify_metadata_signature(
            tar_file="/fake_tarfile.tar",
            gpg_store=mock_gpg_store,
            keyserver_url=KEYSERVER,
            allow_key_download=False,
        )
