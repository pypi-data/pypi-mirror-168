""" Defines the route level auth dependencies for use with FastAPI """

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException

from ..contracts.dto.token_claims import TokenClaims
from .claims import get_claims, get_issuer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_issuer())


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenClaims:
    """
    Gets token claims for token.

    Parameters
    ----------
    token: str
        Oauth2 Token

    Returns
    -------
    claims: TokenClaims
        An instance of TokenClaims.
    """

    return get_claims(token=token)


def is_enabled(token_claims: TokenClaims = Depends(get_current_user)) -> TokenClaims:
    """
    Enforces that the user is enabled.

    Parameters
    ----------
    token_claims: TokenClaims
        User claims to review.

    Returns
    -------
    claims: TokenClaims
        An instance of TokenClaims, otherwise an HTTPException exception.
    """

    if token_claims.disabled:
        raise HTTPException(status_code=401, detail="Inactive user")
    return token_claims


def is_admin(token_claims: TokenClaims = Depends(is_enabled)) -> TokenClaims:
    """
    Enforces that the user is an admin.

    Parameters
    ----------
    token_claims: TokenClaims
        User claims to review.

    Returns
    -------
    claims: TokenClaims
        An instance of TokenClaims, otherwise an HTTPException exception.
    """

    if not token_claims.admin:
        raise HTTPException(status_code=401, detail="Insufficient Permissions")
    return token_claims
