""" Password Related Utilities """

from passlib.context import CryptContext

# Acts as a singleton
ROWANTREE_AUTH_SDK_PASSWORD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies hashed password.

    Parameters
    ----------
    plain_password: str
        Plan text password
    hashed_password: str
        Hashed password

    Returns
    -------
    verified: bool
        True if the password matches the hash, False otherwise.
    """

    return ROWANTREE_AUTH_SDK_PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generates password hash.

    Parameters
    ----------
    password: str
        Plain text password.

    Returns
    -------
    hashed_password: str
        Hashed password.
    """

    return ROWANTREE_AUTH_SDK_PASSWORD_CONTEXT.hash(password)
