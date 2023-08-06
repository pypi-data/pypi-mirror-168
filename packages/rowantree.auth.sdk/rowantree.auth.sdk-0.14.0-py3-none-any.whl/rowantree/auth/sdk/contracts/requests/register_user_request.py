""" Auth Service Register User Base Definition """
from rowantree.contracts import BaseModel


class RegisterUserRequest(BaseModel):
    """
    Auth Service Register User Base

    Attributes
    ----------
    username: str
        The username of the user.
    email: Union[str, None] = None
        The user email address.
    password: str
        user password.
    """

    username: str
    email: str
    password: str
