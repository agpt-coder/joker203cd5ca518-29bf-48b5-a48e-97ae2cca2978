from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class JokeDetailsResponse(BaseModel):
    """
    This model represents the detailed view of a joke, showing all relevant fields retrieved from the litellm platform structured for client use.
    """

    id: str
    text: str
    source: str
    createdAt: datetime
    updatedAt: datetime


async def fetchJokeDetails(jokeId: str) -> JokeDetailsResponse:
    """
    Provides detailed information about a specific joke, identified by its 'jokeId'. This endpoint facilitates users in retrieving full details of a joke including its content, author, and publication date. The system fetches this information from the litellm platform and presents it in a structured format.

    Args:
    jokeId (str): Unique identifier for a joke, used to fetch the detailed information of the joke.

    Returns:
    JokeDetailsResponse: This model represents the detailed view of a joke, showing all relevant fields retrieved from the litellm platform structured for client use.

    Example:
    jokeId = '12345'
    details = await fetchJokeDetails(jokeId)
    print(details)
    """
    joke = await prisma.models.Joke.prisma().find_unique(where={"id": jokeId})
    if joke is None:
        raise ValueError(f"Joke with ID {jokeId} not found.")
    return JokeDetailsResponse(
        id=joke.id,
        text=joke.text,
        source=joke.source,
        createdAt=joke.createdAt,
        updatedAt=joke.updatedAt,
    )
