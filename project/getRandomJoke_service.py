import random
from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class RandomJokeRequest(BaseModel):
    """
    This model represents the details required to fetch a random joke. Since this is a GET request without any input parameters, no fields are necessary.
    """

    pass


class RandomJokeResponse(BaseModel):
    """
    The response for the GET /jokes/random endpoint. It returns a joke object with a text and any additional metadata.
    """

    text: str
    createdAt: datetime
    updatedAt: datetime
    source: str
    id: str


def getRandomJoke(request: RandomJokeRequest) -> RandomJokeResponse:
    """
    Fetches a random joke using the underlying logic of the Randomization Logic Module, which selects a joke randomly from a dataset. This jokes then passes to the Joke Fetching Logic Module, ensuring that it reaches the user in a consumable format. The response will include a joke string in JSON format. Uses GET method to ensure simplicity and efficiency in fetching data.

    Args:
    request (RandomJokeRequest): This model represents the details required to fetch a random joke. Since this is a GET request without any input parameters, no fields are necessary.

    Returns:
    RandomJokeResponse: The response for the GET /jokes/random endpoint. It returns a joke object with a text and any additional metadata.
    """
    jokes = prisma.models.Joke.prisma().find_many()
    selected_joke = random.choice(jokes)
    response = RandomJokeResponse(
        text=selected_joke.text,
        createdAt=selected_joke.createdAt,
        updatedAt=selected_joke.updatedAt,
        source=selected_joke.source,
        id=selected_joke.id,
    )
    return response
