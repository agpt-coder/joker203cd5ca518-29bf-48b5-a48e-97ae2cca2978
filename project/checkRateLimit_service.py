import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class RateLimitCheckResponse(BaseModel):
    """
    This response model informs the client whether the user has exceeded the API request rate limit or not.
    """

    exceeded: bool
    remaining_requests: int
    error_message: Optional[str] = None


async def checkRateLimit(user_id: str) -> RateLimitCheckResponse:
    """
    This endpoint checks if the requesting user has exceeded their API request quota. It intercepts API requests,
    checks the user's request count stored in a database against predefined limits, and returns whether the user
    can proceed or not. If exceeded, it returns an error message; otherwise, it allows the request to be processed.

    Args:
    user_id (str): The unique identifier of the user for whom the rate limit check is being made. Typically passed as
    a header or extracted from session/token.

    Returns:
    RateLimitCheckResponse: This response model informs the client whether the user has exceeded the API request rate limit or not.
    """
    api_endpoint = await prisma.models.APIEndpoint.prisma().find_first(
        where={"handlerId": "<current_function_id>"}
    )
    if not api_endpoint:
        return RateLimitCheckResponse(
            exceeded=True,
            remaining_requests=0,
            error_message="API endpoint configuration not found.",
        )
    today_start = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    request_count = await prisma.models.Log.prisma().count(
        where={
            "userId": user_id,
            "APIEndpoint": {"id": api_endpoint.id},
            "createdAt": {"gte": today_start},
        }
    )
    rate_limit_exceeded = request_count >= api_endpoint.rateLimit
    return RateLimitCheckResponse(
        exceeded=rate_limit_exceeded,
        remaining_requests=max(0, api_endpoint.rateLimit - request_count),
        error_message="Rate limit exceeded." if rate_limit_exceeded else None,
    )
