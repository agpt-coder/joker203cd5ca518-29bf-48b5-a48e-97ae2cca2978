from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetUserDetailsResponse(BaseModel):
    """
    Response model for user details retrieval. Contains the detailed user information if the user exists or an error response if the user does not exist.
    """

    id: str
    username: str
    createdAt: datetime
    updatedAt: datetime
    role: prisma.enums.Role


async def getUserDetails(userId: str) -> GetUserDetailsResponse:
    """
    Retrieves detailed information about a specific user identified by userId. It fetches data from the user database. If the user exists, it returns the user's details; if not, it triggers the Error Handling Module to return an error indicating that the user was not found.

    Args:
        userId (str): The unique identifier of the user for whom details are to be retrieved. It's passed in the path of the URL.

    Returns:
        GetUserDetailsResponse: Response model for user details retrieval. Contains the detailed user information if the user exists or an error response if the user does not exist.

    Example:
        getUserDetails('123e4567-e89b-12d3-a456-426614174000')
        > GetUserDetailsResponse(id='123e4567-e89b-12d3-a456-426614174000', username='john_doe', createdAt=datetime.datetime.now(), updatedAt=datetime.datetime.now(), role=prisma.enums.Role.API_User)
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"role": True}
    )
    if not user:
        raise ValueError(f"User with ID {userId} not found.")
    return GetUserDetailsResponse(
        id=user.id,
        username=user.username,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
        role=user.role,
    )
