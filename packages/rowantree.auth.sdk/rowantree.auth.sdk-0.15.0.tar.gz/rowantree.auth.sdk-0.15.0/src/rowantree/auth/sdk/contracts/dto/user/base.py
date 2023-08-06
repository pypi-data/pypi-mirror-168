""" Auth Service User Base Definition """

from typing import Optional

from rowantree.contracts import BaseModel


class UserBase(BaseModel):
    """
    Auth Service User Base

    Attributes
    ----------
    username: str
        The username of the user.
    guid: str
        The user guid.
    email: Union[str, None] = None
        The user email address.
    disabled: Union[bool, None] = None
        Whether the account is enabled or not.
    admin: Union[bool, None] = None
        Whether the account is an admin or not.
    """

    username: str
    guid: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None
    admin: Optional[bool] = None
