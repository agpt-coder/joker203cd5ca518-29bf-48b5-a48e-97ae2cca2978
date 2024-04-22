import prisma
import prisma.models
from pydantic import BaseModel


class RateLimitModificationResponse(BaseModel):
    """
    Provides feedback after attempting to set or modify a user's rate limit.
    """

    user_id: str
    new_rate_limit: int
    status: str


async def setUserRateLimit(
    user_id: str, new_rate_limit: int
) -> RateLimitModificationResponse:
    """
    This secured endpoint allows administrators to set or modify the rate limit for a specific user. It requires user ID and
    new rate limit values as inputs. It then updates these values in the database, effectively changing the number of requests
    a user can make to the API within a defined time frame.

    Args:
        user_id (str): The unique identifier of the user for whom the rate limit is to be set or modified.
        new_rate_limit (int): The new rate limit value to be applied, defining the maximum number of allowed API requests by
                              this user within the specified time frame.

    Returns:
        RateLimitModificationResponse: Provides feedback after attempting to set or modify a user's rate limit.
    """
    endpoint = await prisma.models.APIEndpoint.prisma().find_first(
        where={"Handler": {"FunctionLogs": {"User": {"id": user_id}}}}
    )
    if not endpoint:
        return RateLimitModificationResponse(
            user_id=user_id,
            new_rate_limit=new_rate_limit,
            status="Failed: No endpoint found for the user.",
        )
    updated_endpoint = await prisma.models.APIEndpoint.prisma().update(
        where={"id": endpoint.id}, data={"rateLimit": new_rate_limit}
    )
    if updated_endpoint:
        return RateLimitModificationResponse(
            user_id=user_id,
            new_rate_limit=new_rate_limit,
            status="Success: Rate limit updated.",
        )
    return RateLimitModificationResponse(
        user_id=user_id,
        new_rate_limit=new_rate_limit,
        status="Failed: Unable to update rate limit.",
    )
