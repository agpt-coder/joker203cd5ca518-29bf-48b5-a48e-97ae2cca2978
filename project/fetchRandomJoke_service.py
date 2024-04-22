import httpx
from pydantic import BaseModel


class GetRandomJokeRequest(BaseModel):
    """
    This GET request does not require any input parameters since it is used to fetch a random joke without user-specific data or criteria.
    """

    pass


class Error(BaseModel):
    """
    Detailed description of the error, including status code and a human-readable message.
    """

    status_code: int
    message: str


class GetRandomJokeResponse(BaseModel):
    """
    This response model encapsulates the joke received from the litellm API or the error response structured by the Error Handling Module.
    """

    joke: str
    error: Error


async def fetchRandomJoke(request: GetRandomJokeRequest) -> GetRandomJokeResponse:
    """
    This route retrieves a random joke. It uses the litellm API to generate a random joke, handling any exceptions
    or errors via the Error Handling Module. Upon success, it returns the joke in a JSON format with a status code
    of 200. If any error occurs, this triggers the Error Handling Module to log the error and return a structured
    error response. This ensures a reliable user experience.

    Args:
    request (GetRandomJokeRequest): This GET request does not require any input parameters since it is used to fetch
    a random joke without user-specific data or criteria.

    Returns:
    GetRandomJokeResponse: This response model encapsulates the joke received from the litellm API or the error
                           response structured by the Error Handling Module.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.litellm.com/jokes/random")
            response.raise_for_status()
            joke_data = response.json()
            joke_text = joke_data.get("joke")
            if joke_text:
                return GetRandomJokeResponse(joke=joke_text, error=None)
            else:
                return GetRandomJokeResponse(
                    joke="",
                    error=Error(
                        status_code=404, message="Joke not found in API response."
                    ),
                )
    except httpx.RequestError as e:
        return GetRandomJokeResponse(
            joke="", error=Error(status_code=500, message=f"Network error: {str(e)}")
        )
    except httpx.HTTPStatusError as e:
        return GetRandomJokeResponse(
            joke="",
            error=Error(
                status_code=e.response.status_code,
                message="Failed to fetch joke from API",
            ),
        )
    except Exception as e:
        return GetRandomJokeResponse(
            joke="",
            error=Error(
                status_code=500, message=f"An unexpected error occurred: {str(e)}"
            ),
        )
