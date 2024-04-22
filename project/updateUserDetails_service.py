from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class User(BaseModel):
    """
    A user object displaying common information like username and role.
    """

    id: str
    createdAt: datetime
    updatedAt: datetime
    username: str
    role: prisma.enums.Role


class UpdateUserResponse(BaseModel):
    """
    Model confirming the success of the update or reflecting the updated user details.
    """

    success: bool
    message: str
    updatedUser: User


async def updateUserDetails(
    userId: str, name: str, password: str, role: prisma.enums.Role
) -> UpdateUserResponse:
    """
    Updates a specific user's details. This endpoint facilitates changes to user profiles, including updating names, passwords, and roles as authorized by admin users.

    Args:
        userId (str): The unique identifier for the user to be updated.
        name (str): The new name of the user, if updating.
        password (str): The new password for the user, if updating.
        role (prisma.enums.Role): The new role assigned to the user, restricted to valid prisma.enums.Role types.

    Returns:
        UpdateUserResponse: Model confirming the success of the update or reflecting the updated user details.
    """
    current_time = datetime.now()
    hashed_password = "hashed_" + password
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId},
        data={
            "username": name,
            "password": hashed_password,
            "role": role,
            "updatedAt": current_time,
        },
    )
    return UpdateUserResponse(
        success=True,
        message="User details updated successfully.",
        updatedUser=updated_user,
    )
