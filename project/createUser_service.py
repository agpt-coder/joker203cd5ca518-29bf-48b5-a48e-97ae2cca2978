from datetime import datetime
from enum import Enum

import prisma
import prisma.enums
import prisma.models
from bcrypt import gensalt, hashpw
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


class CreateUserResponse(BaseModel):
    """
    Response model for user creation. Includes the newly created user object and a status message.
    """

    user: User
    status: str


class Role(Enum):
    API_User: str = "API_User"
    API_Admin: str = "API_Admin"
    System_Operator: str = "System_Operator"


async def createUser(
    name: str, email: str, password: str, role: prisma.enums.Role
) -> CreateUserResponse:
    """
    This route allows the creation of a new user in the system. It accepts user details such as name, email, and password, then returns the created user object with a status code of 201.

    Args:
    name (str): Full name of the user.
    email (str): Email address of the user, which will be used for login and notifications.
    password (str): Password for the user account. This should be received in a secure manner and stored securely.
    role (prisma.enums.Role): The role assigned to the user. For this endpoint, typically set to 'API_Admin'.

    Returns:
    CreateUserResponse: Response model for user creation. Includes the newly created user object and a status message.
    """
    hashed_password = hashpw(password.encode("utf-8"), gensalt())
    prisma_user = await prisma.models.User.prisma().create(
        data={
            "username": name,
            "email": email,
            "hashed_password": hashed_password.decode("utf-8"),
            "role": role,
        }
    )
    user = User(
        id=prisma_user.id,
        createdAt=prisma_user.createdAt,
        updatedAt=prisma_user.updatedAt,
        username=prisma_user.username,
        role=prisma_user.role,
    )
    return CreateUserResponse(user=user, status="User created successfully")
