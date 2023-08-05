
from __future__ import annotations

from collections.abc import Set
from datetime import datetime

from ..interfaces.token import TokenCredentials, TokensInterface
from ..plugin import Plugin

__all__ = ['tokens', 'AllTokens']

#: Registers token plugins.
tokens: Plugin[type[TokensInterface]] = Plugin(
    'pymap.token', default='macaroon')


class AllTokens(TokensInterface):
    """Uses :data:`tokens` to support all registered token types.

    For token creation, the :attr:`~pymap.plugin.Plugin.default` token plugin
    is used. For token parsing, each token plugin is tried until one succeeds.

    """

    def get_login_token(self, identifier: str, authcid: str, key: bytes, *,
                        authzid: str | None = None,
                        location: str | None = None,
                        expiration: datetime | None = None) \
            -> str | None:
        try:
            token_type = tokens.default
        except KeyError:
            return None
        return token_type().get_login_token(
            identifier, authcid, key, authzid=authzid, location=location,
            expiration=expiration)

    def get_admin_token(self, admin_key: bytes | None, *,
                        authzid: str | None = None,
                        location: str | None = None,
                        expiration: datetime | None = None) \
            -> str | None:
        try:
            token_type = tokens.default
        except KeyError:
            return None
        return token_type().get_admin_token(
            admin_key, authzid=authzid, location=location,
            expiration=expiration)

    def parse(self, authzid: str, token: str, *,
              admin_keys: Set[bytes] = frozenset()) \
            -> TokenCredentials:
        for _, token_type in tokens.registered.items():
            try:
                return token_type().parse(authzid, token,
                                          admin_keys=admin_keys)
            except ValueError:
                pass
        raise ValueError('invalid token')
