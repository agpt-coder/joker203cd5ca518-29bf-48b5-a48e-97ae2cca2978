from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetUsersRequest(BaseModel):
    """
    Request model for retrieving list of users. It doesn't require a body or query parameters since it's a straightforward GET request.
    """

    pass


class User(BaseModel):
    """
    A user object displaying common information like username and role.
    """

    id: str
    createdAt: datetime
    updatedAt: datetime
    username: str
    role: prisma.enums.Role


class GetUsersResponse(BaseModel):
    """
    Response model containing an array of users. Each user contains standard fields according to the User database model.
    """

    users: List[User]


async def getAllUsers(request: GetUsersRequest) -> GetUsersResponse:
    """
    Retrieves a list of all users. This can be used by administrators to audit or manage users. The response includes an array of user objects.

    Args:
        request (GetUsersRequest): Request model for retrieving list of users. It doesn't require a body or query parameters since it's a straightforward GET request.

    Returns:
        GetUsersResponse: Response model containing an array of users. Each user contains standard fields according to the User database model.
    """
    users_records = await prisma.models.User.prisma().find_many()
    users = [
        User(
            id=user.id,
            createdAt=user.createdAt,
            updatedAt=user.updatedAt,
            username=user.username,
            role=user.role.name,
        )
        for user in users_records
    ]
    response = GetUsersResponse(users=users)
    return response
