---
date: 2024-04-22T12:18:07.209297
author: AutoGPT <info@agpt.co>
---

# joker203

create a single api that returns one random joke using litellm

**Features**

- **API Endpoint** A single endpoint that serves one random joke on each request.

- **Joke Fetching Logic** Logic integrated into the API that fetches jokes from the litellm platform.

- **Randomization Logic** Implements an algorithm or method to select a joke randomly.

- **Error Handling** Proper error responses for scenarios like server errors or no jokes available.

- **Rate Limiting** Implementing rate limiting to prevent abuse of the API.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'joker203'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
