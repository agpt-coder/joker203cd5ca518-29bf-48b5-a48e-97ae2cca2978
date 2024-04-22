from datetime import datetime
from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel, ValidationError


class UserDetailsResponse(BaseModel):
    """
    Output model representing the details of a specific user fetched from the database or an error message if not found.
    """

    id: str
    username: str
    createdAt: datetime
    updatedAt: datetime
    role: prisma.enums.Role


class Role(Enum):
    API_User: str = "API_User"
    API_Admin: str = "API_Admin"
    System_Operator: str = "System_Operator"


async def getUser(userId: str) -> UserDetailsResponse:
    """
    Fetches details of a specific user by their unique identifier (userId). The function returns a single user object.

    Args:
        userId (str): The unique identifier of the user to fetch.

    Returns:
        UserDetailsResponse: Output model representing the details of a specific user fetched from the database.

    Raises:
        ValueError: If the user does not exist.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        raise ValueError("User not found")
    try:
        user_details = UserDetailsResponse(
            id=user.id,
            username=user.username,
            createdAt=user.createdAt,
            updatedAt=user.updatedAt,
            role=user.role,
        )
    except ValidationError as e:
        raise ValueError(f"Data validation error: {str(e)}")
    return user_details
