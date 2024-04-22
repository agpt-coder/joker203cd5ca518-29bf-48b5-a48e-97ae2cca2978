import logging
from contextlib import asynccontextmanager
from typing import Optional

import prisma
import prisma.enums
import project.checkRateLimit_service
import project.createUser_service
import project.deleteUser_service
import project.fetchJokeDetails_service
import project.fetchRandomJoke_service
import project.getAllUsers_service
import project.getRandomJoke_service
import project.getSystemRateLimits_service
import project.getUser_service
import project.getUserDetails_service
import project.listUsers_service
import project.setUserRateLimit_service
import project.updateUser_service
import project.updateUserDetails_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="joker203",
    lifespan=lifespan,
    description="create a single api that returns one random joke using litellm",
)


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: str,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a specific user from the system using the userId. Upon successful deletion, it returns a confirmation message. Any errors encountered during the process are handled by the Error Handling Module, ensuring clean and clear feedback is provided to the client.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/jokes/{jokeId}",
    response_model=project.fetchJokeDetails_service.JokeDetailsResponse,
)
async def api_get_fetchJokeDetails(
    jokeId: str,
) -> project.fetchJokeDetails_service.JokeDetailsResponse | Response:
    """
    Provides detailed information about a specific joke, identified by its 'jokeId'. This endpoint facilitates users in retrieving full details of a joke including its content, author, and publication date. The system fetches this information from the litellm platform and presents it in a structured format.
    """
    try:
        res = await project.fetchJokeDetails_service.fetchJokeDetails(jokeId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.getAllUsers_service.GetUsersResponse)
async def api_get_getAllUsers(
    request: project.getAllUsers_service.GetUsersRequest,
) -> project.getAllUsers_service.GetUsersResponse | Response:
    """
    Retrieves a list of all users. This can be used by administrators to audit or manage users. The response includes an array of user objects.
    """
    try:
        res = await project.getAllUsers_service.getAllUsers(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.listUsers_service.GetUsersResponse)
async def api_get_listUsers(
    request: project.listUsers_service.GetUsersRequest,
) -> project.listUsers_service.GetUsersResponse | Response:
    """
    Retrieves a list of all registered users. Useful for administrative purposes, this route provides an overview of users, enabling management functions such as auditing and monitoring.
    """
    try:
        res = await project.listUsers_service.listUsers(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/jokes/random",
    response_model=project.fetchRandomJoke_service.GetRandomJokeResponse,
)
async def api_get_fetchRandomJoke(
    request: project.fetchRandomJoke_service.GetRandomJokeRequest,
) -> project.fetchRandomJoke_service.GetRandomJokeResponse | Response:
    """
    This route retrieves a random joke. It uses the litellm API to generate a random joke, handling any exceptions or errors via the Error Handling Module. Upon success, it returns the joke in a JSON format with a status code of 200. If any error occurs, this triggers the Error Handling Module to log the error and return a structured error response. This ensures a reliable user experience.
    """
    try:
        res = await project.fetchRandomJoke_service.fetchRandomJoke(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/{userId}", response_model=project.getUser_service.UserDetailsResponse)
async def api_get_getUser(
    userId: str,
) -> project.getUser_service.UserDetailsResponse | Response:
    """
    Fetches details of a specific user by their unique identifier (userId). The route returns a single user object or an error if the user does not exist.
    """
    try:
        res = await project.getUser_service.getUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    name: str, email: str, password: str, role: prisma.enums.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    This route allows the creation of a new user in the system. It accepts user details such as name, email, and password, then returns the created user object with a status code of 201.
    """
    try:
        res = await project.createUser_service.createUser(name, email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/jokes/random", response_model=project.getRandomJoke_service.RandomJokeResponse
)
async def api_get_getRandomJoke(
    request: project.getRandomJoke_service.RandomJokeRequest,
) -> project.getRandomJoke_service.RandomJokeResponse | Response:
    """
    Fetches a random joke using the underlying logic of the Randomization Logic Module, which selects a joke randomly from a dataset. This jokes then passes to the Joke Fetching Logic Module, ensuring that it reaches the user in a consumable format. The response will include a joke string in JSON format. Uses GET method to ensure simplicity and efficiency in fetching data.
    """
    try:
        res = project.getRandomJoke_service.getRandomJoke(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/rateLimit/check",
    response_model=project.checkRateLimit_service.RateLimitCheckResponse,
)
async def api_get_checkRateLimit(
    user_id: str,
) -> project.checkRateLimit_service.RateLimitCheckResponse | Response:
    """
    This endpoint checks if the requesting user has exceeded their API request quota. It intercepts API requests, checks the user's request count stored in a database against predefined limits, and returns whether the user can proceed or not. If exceeded, it returns an error message; otherwise, it allows the request to be processed.
    """
    try:
        res = await project.checkRateLimit_service.checkRateLimit(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/rateLimit/user",
    response_model=project.setUserRateLimit_service.RateLimitModificationResponse,
)
async def api_post_setUserRateLimit(
    user_id: str, new_rate_limit: int
) -> project.setUserRateLimit_service.RateLimitModificationResponse | Response:
    """
    This secured endpoint allows administrators to set or modify the rate limit for a specific user. It requires user ID and new rate limit values as inputs. It then updates these values in the database, effectively changing the number of requests a user can make to the API within a defined time frame.
    """
    try:
        res = await project.setUserRateLimit_service.setUserRateLimit(
            user_id, new_rate_limit
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}", response_model=project.updateUser_service.UserUpdateResponse
)
async def api_put_updateUser(
    userId: str, username: Optional[str], role: Optional[prisma.enums.Role]
) -> project.updateUser_service.UserUpdateResponse | Response:
    """
    Updates user information for a specified userId. This route requires full user data which includes fields that need to be updated. It returns the updated user data.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, username, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/{userId}",
    response_model=project.getUserDetails_service.GetUserDetailsResponse,
)
async def api_get_getUserDetails(
    userId: str,
) -> project.getUserDetails_service.GetUserDetailsResponse | Response:
    """
    Retrieves detailed information about a specific user identified by userId. It fetches data from the user database. If the user exists, it returns the user's details; if not, it triggers the Error Handling Module to return an error indicating that the user was not found.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}",
    response_model=project.updateUserDetails_service.UpdateUserResponse,
)
async def api_put_updateUserDetails(
    userId: str, name: str, password: str, role: prisma.enums.Role
) -> project.updateUserDetails_service.UpdateUserResponse | Response:
    """
    Updates a specific user's details. This endpoint facilitates changes to user profiles, including updating names, passwords, and roles as authorized by admin users.
    """
    try:
        res = await project.updateUserDetails_service.updateUserDetails(
            userId, name, password, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/rateLimit/system",
    response_model=project.getSystemRateLimits_service.SystemRateLimitResponse,
)
async def api_get_getSystemRateLimits(
    request: project.getSystemRateLimits_service.SystemRateLimitRequest,
) -> project.getSystemRateLimits_service.SystemRateLimitResponse | Response:
    """
    This endpoint provides a view of the current system-wide rate limits. It could be used by system operators to monitor and manage the overall API usage policies. This route fetches and displays all rate limits from the database, ensuring that system administrators are updated with the latest configurations.
    """
    try:
        res = await project.getSystemRateLimits_service.getSystemRateLimits(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
