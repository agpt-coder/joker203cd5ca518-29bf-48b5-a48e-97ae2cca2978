from datetime import datetime
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserUpdateResponse(BaseModel):
    """
    Model for outputting the updated user data after a successful PUT operation.
    """

    id: str
    createdAt: datetime
    updatedAt: datetime
    username: str
    role: prisma.enums.Role


class Role(BaseModel):
    API_User: str = "API_User"
    API_Admin: str = "API_Admin"
    System_Operator: str = "System_Operator"


async def updateUser(
    userId: str, username: Optional[str], role: Optional[prisma.enums.Role]
) -> UserUpdateResponse:
    """
    Updates user information for a specified userId. This function requires full user data which includes fields that need to be updated. It returns the updated user data.

    Args:
    userId (str): The unique identifier for the user expected in the path of the request.
    username (Optional[str]): Updated username, if provided.
    role (Optional[prisma.enums.Role]): Updated role of the user, if provided.

    Returns:
    UserUpdateResponse: Model for outputting the updated user data after a successful PUT operation.
    """
    update_data = {"updatedAt": datetime.now()}
    if username is not None:
        update_data["username"] = username
    if role is not None:
        update_data["role"] = role
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId}, data=update_data, include={"username": True, "role": True}
    )
    return UserUpdateResponse(
        id=updated_user.id,
        createdAt=updated_user.createdAt,
        updatedAt=updated_user.updatedAt,
        username=updated_user.username,
        role=updated_user.role,
    )
