""" Token Claims Definition """

from datetime import datetime

from pydantic import BaseModel


class TokenClaims(BaseModel):
    """
    Token Claims

    Attributes
    ----------
    sub: str
        The subject of the token. (the target user guid)
    iss: str
        The issuer of the token (the auth url for the current domain)
    exp: datetime
        The expiry time of the token
    disabled: bool
        Whether or not the user is disabled
    admin: bool
        Whether or not the user is ad admin.
    """

    sub: str
    iss: str
    exp: datetime

    # TOO: move to scopes
    disabled: bool
    admin: bool
