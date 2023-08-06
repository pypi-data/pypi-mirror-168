""" Request Status Codes Definition """
from rowantree.contracts import BaseModel


class RequestStatusCodes(BaseModel):
    """
    Request Status Codes DTO

    Attributes
    ----------
    allow: list[int]
        A list of allowed response codes.
    retry: list[int]
        A list of re-try-able response codes.
    """

    allow: list[int]
    retry: list[int]
