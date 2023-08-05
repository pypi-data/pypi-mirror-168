
import secrets
from typing import Optional

from .server import ServerCredentials
from ..identity import Identity
from ..prep import prepare

__all__ = ['PlainCredentials']


class PlainCredentials(ServerCredentials):
    """Implementation of :class:`~pysasl.creds.server.ServerCredentials` for
    typical SASL mechanisms like
    :class:`~pysasl.mechanisms.plain.PlainMechanism`.

    Args:
        authcid: Authentication ID string (the username).
        secret: Secret string (the password).
        authzid: Authorization ID string, if provided.

    """

    __slots__ = ['_authcid', '_secret', '_authzid']

    def __init__(self, authcid: str, secret: str, authzid: str = '') -> None:
        super().__init__()
        self._authcid = authcid
        self._secret = secret
        self._authzid = authzid or prepare(authcid)

    @property
    def authcid(self) -> str:
        return self._authcid

    @property
    def authzid(self) -> str:
        return self._authzid

    def verify(self, identity: Optional[Identity]) -> bool:
        if identity is not None:
            self_authcid = prepare(self.authcid)
            other_authcid = prepare(identity.authcid)
            return secrets.compare_digest(self_authcid, other_authcid)  \
                and identity.compare_secret(self._secret)
        return False

    def __repr__(self) -> str:
        return f'PlainCredentials({self.authcid!r}, ..., {self.authzid!r})'
