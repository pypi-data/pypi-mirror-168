""" Claim Utilities """

import logging
from typing import Optional

from jose import JWTError, jwt
from starlette import status
from starlette.exceptions import HTTPException

from rowantree.common.sdk import demand_env_var

from ..contracts.dto.token_claims import TokenClaims


def get_claims(token: str) -> TokenClaims:
    """
    Gets claims from an OAuth2 token.

    Parameters
    ----------
    token: str
        Encoded token.

    Returns
    -------
    claims: TokenClaims
        An instance of TokenClaims, otherwise an HTTPException exception.
    """

    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        issuer: str = get_issuer()

        payload: dict = jwt.decode(
            token=token,
            key=demand_env_var(name="ACCESS_TOKEN_SECRET_KEY"),
            algorithms=[demand_env_var(name="ACCESS_TOKEN_ALGORITHM")],
            issuer=issuer,
        )
        token_issuer: Optional[str] = payload.get("iss")
        guid: Optional[str] = payload.get("sub")
        if token_issuer != issuer or guid is None:
            logging.debug("Received issuer: %s, expected: %s, guid was: %s", token_issuer, issuer, guid)
            raise credentials_exception
        logging.debug(payload)
        return TokenClaims(**payload)
    except JWTError:
        raise credentials_exception from JWTError


def get_issuer() -> str:
    """
    Builds issuer string

    Returns
    -------
    issuer: str
        The issuer for the domain.
    """

    return f"https://{demand_env_var(name='ROWANTREE_TLD')}/auth"
