import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model for deleting a user. It includes a success message indicating the deletion outcome.
    """

    message: str


async def deleteUser(userId: str) -> DeleteUserResponse:
    """
    Deletes a specific user from the system using the userId. Upon successful deletion, it returns a confirmation message.
    Any errors encountered during the process are handled internally, ensuring clean and clear feedback is provided to the client.

    Args:
        userId (str): The unique identifier for the user to be deleted.

    Returns:
        DeleteUserResponse: Response model for deleting a user. It includes a success message indicating the deletion outcome.
    """
    try:
        user = await prisma.models.User.prisma().delete(where={"id": userId})
        if user:
            message = f"User with ID {userId} has been successfully deleted."
        else:
            message = "No user found with the specified ID."
    except Exception as e:
        return DeleteUserResponse(message=f"Failed to delete user due to: {str(e)}")
    return DeleteUserResponse(message=message)
