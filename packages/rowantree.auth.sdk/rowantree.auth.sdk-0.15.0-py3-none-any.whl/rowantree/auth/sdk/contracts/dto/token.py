""" Token Definition """
from rowantree.contracts import BaseModel


class Token(BaseModel):
    """
    Token

    Attributes
    ----------
    access_token: str
        Minted access token
    token_type: str
        Type of token
    """

    access_token: str
    token_type: str
