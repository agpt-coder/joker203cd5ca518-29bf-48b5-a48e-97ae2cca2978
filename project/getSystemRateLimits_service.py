from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class SystemRateLimitRequest(BaseModel):
    """
    No specific request fields are necessary for retrieving system-wide rate limits, as this operation does not require input from the client side other than the necessary credentials and roles.
    """

    pass


class RateLimitDetails(BaseModel):
    """
    Detailed view of rate limiting settings for specific functionalities or APIs.
    """

    path: str
    limit: int
    duration: int
    roleAffected: prisma.enums.Role


class SystemRateLimitResponse(BaseModel):
    """
    Response model to represent system-wide rate limits which include details such as request limits, time frame, and the particular API or functionality they apply to.
    """

    rateLimits: List[RateLimitDetails]


async def getSystemRateLimits(
    request: SystemRateLimitRequest,
) -> SystemRateLimitResponse:
    """
    This endpoint provides a view of the current system-wide rate limits. It could be used by system operators to monitor and manage the overall API usage policies. This route fetches and displays all rate limits from the database, ensuring that system administrators are updated with the latest configurations.

    Args:
        request (SystemRateLimitRequest): No specific request fields are necessary for retrieving system-wide rate limits, as this operation does not require input from the client side other than the necessary credentials and roles.

    Returns:
        SystemRateLimitResponse: Response model to represent system-wide rate limits which include details such as request limits, time frame, and the particular API or functionality they apply to.
    """
    endpoints = (
        await prisma.models.APIEndpoint.find_many()
    )  # TODO(autogpt): Cannot access member "find_many" for type "type[APIEndpoint]"
    #     Member "find_many" is unknown. reportAttributeAccessIssue
    rate_limits_details = []
    for endpoint in endpoints:
        function_statuses = await prisma.models.FunctionStatus.find_many(
            where={"id": endpoint.handlerId}
        )  # TODO(autogpt): Cannot access member "find_many" for type "type[FunctionStatus]"
        #     Member "find_many" is unknown. reportAttributeAccessIssue
        role_affected = "System_Operator"
        for status in function_statuses:
            if hasattr(status, "details") and "roleAffected" in status.details:
                role_affected = status.details["roleAffected"]
                break
        rate_limit_detail = RateLimitDetails(
            path=endpoint.path,
            limit=endpoint.rateLimit,
            duration=60,
            roleAffected=role_affected,
        )
        rate_limits_details.append(rate_limit_detail)
    response = SystemRateLimitResponse(rateLimits=rate_limits_details)
    return response
