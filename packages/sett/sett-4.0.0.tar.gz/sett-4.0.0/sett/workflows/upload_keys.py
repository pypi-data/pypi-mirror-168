from typing import Sequence, Iterable

from gpg_lite.keyserver import VksEmailStatus
from libbiomedit import crypt

from ..core.crypt import (
    upload_keys as crypt_upload_keys,
    request_key_verification as crypt_request_key_verification,
    search_pub_key,
    verify_key_length,
)
from ..core.error import UserError
from ..utils.config import Config
from ..utils.log import create_logger, log_runtime_info

logger = create_logger(__name__)


@log_runtime_info(logger)
def verify_keylengths_and_upload_keys(
    fingerprints: Sequence[str], *, config: Config
) -> None:
    """Verify key lengths and upload keys"""
    keys = frozenset(
        search_pub_key(k, config.gpg_store, sigs=False) for k in fingerprints
    )
    for key in keys:
        verify_key_length(key)
    upload_keys(fingerprints=fingerprints, config=config)


@log_runtime_info(logger)
def upload_keys(
    fingerprints: Iterable[str],
    *,
    verify_key: bool = True,
    config: Config,
) -> None:
    """Uploads one or more public PGP keys to the keyserver specified in the
    config. Triggers a verification if the status returned by the keyserver is appropriate.

    Note that we basically assume that each key contains one single UID (email address).
    """
    if config.offline:
        raise UserError("Uploading keys is not possible in offline mode.")
    if config.keyserver_url is None:
        raise UserError("Keyserver URL is undefined.")
    keys = frozenset(
        search_pub_key(k, config.gpg_store, sigs=False) for k in fingerprints
    )
    if keys:
        logger.info("Uploading keys '%s'", ", ".join(k.key_id for k in keys))
        for key in keys:
            if not key.uids or not key.uids[0].email:
                raise UserError(
                    f"The selected key '{crypt.pgp_key_as_str(key)}' does NOT contain an email."
                )
            email = key.uids[0].email
            (response,) = crypt_upload_keys(
                [key.fingerprint],
                keyserver=config.keyserver_url,
                gpg_store=config.gpg_store,
            )
            if email in response.status:
                if (
                    response.status[email]
                    in (
                        VksEmailStatus.UNPUBLISHED,
                        VksEmailStatus.PENDING,
                    )
                    and verify_key
                ):
                    logger.info("Requesting verification for '%s'", email)
                    crypt_request_key_verification(
                        response.token, key.uids[0].email, config.keyserver_url
                    )
                if response.status[email] == VksEmailStatus.REVOKED:
                    raise UserError(f"'{key.key_id}' is revoked and can NOT be used.")
