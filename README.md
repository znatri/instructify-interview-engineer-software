# User Item Management

## Prerequisites

1. [Docker](https://docs.docker.com/engine/install/)
1. [Docker Compose](https://docs.docker.com/compose/install/)
1. [Postman](https://www.postman.com/downloads/)
1. [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/#mac-stable)

## Features

- FastAPI
- React Admin
- SQLAlchemy and Alembic
- Pre-commit hooks (black, autoflake, isort, flake8, prettier)
- Github Action
- Dependabot config
- Docker images

## Intro

This is an example React + FastAPI + SQLAlchemy application which manages arbitrary items for users.

The frontend of this project uses React Admin ([Tutorial](https://marmelab.com/react-admin/Tutorial.html)).

## Getting Started

### Start a local containers with docker-compose

```bash
docker-compose up -d

# Run database migration
docker-compose exec backend alembic upgrade head

# Create database used for testing
docker-compose exec postgres createdb apptest -U postgres
```

### Set up Backend API Access

1. Open Postman
1. Hit Cmd-O (*nix) or Ctrl-O (Windows)
1. Paste <http://localhost:8196/api/v1/openapi.json> and import the OpenAPI spec as a Postman collection
1. On the left side, click the `User Item Management` collection
1. Click `Variables` and update the `baseUrl` variable to have a `Current value` of `http://localhost:8196`
1. Save the result

### Obtain a JWT for the Backend API

1. In Postman, navigate in the `User Item Management` collection to api -> v1 -> auth -> jwt -. login.
1. In the `Body` section, set `username` to `admin@example.com` and `password` to `Password123!`
1. Execute the request
1. Copy the contents of the `access_token` field in the response body
1. Navigate to api -> v1 -> users -> Get Users
1. Click `Authorization`
1. Paste the access token in the `Token` field
1. Execute the request

Nice! We're done with the basic setup now.

## Accessing Application Components

### User (Admin) Credentials

User: <admin@example.com>

Password: Password123!

### URLs

- Backend OpenAPI docs: <http://localhost:8196/docs/>
- Frontend: <http://localhost:3196>

## Local development

The backend setup of docker-compose is set to automatically reload the app whenever code is updated. However, for frontend it's easier to develop locally.

```bash
docker-compose stop frontend
cd frontend
yarn
yarn start
```

If you want to develop against something other than the default host, localhost:8196, you can set the `REACT_APP_API_BASE` environment variable:

```bash
export REACT_APP_API_BASE=http://localhost:8196
yarn start
```

Don't forget to edit the `.env` file and update the `BACKEND_CORS_ORIGINS` value (add `http://localhost:3196` to the allowed origins).

### Rebuilding containers

If you add a dependency, you'll need to rebuild your containers like this:

```bash
docker-compose up -d --build
```

If you need to re-create the database volume from scratch:

```bash
docker-compose down

docker volume rm interview-engineer-software_app-db-data

docker-compose up -d --build
```

### Regenerate front-end API package

Instead of writing frontend API client manually, OpenAPI Generator is used. Typescript bindings for the backend API can be recreated with this command:

```bash
yarn genapi
```

## Database

### Initialization & Migrations

```bash
# Apply latest changes (bootstraps the database with initial data)
docker-compose exec backend alembic upgrade head
```

### Accessing the Database

```bash
docker exec -ti postgres psql -d app -U postgres
```

### Backend tests

The `Backend` service uses a hardcoded database named `apptest`. First, ensure that it's created

```bash
docker-compose exec postgres createdb apptest -U postgres
```

Then you can run tests with this command:

```bash
docker-compose run backend pytest --cov --cov-report term-missing
```

## New Feature

### Scope

Add a new endpoint accessible via `/users/valid` which returns only "valid" users.

For the sake of the interview, let's make up a definition of "valid" as follows:

Valid: The email domain of the user is accessible via an HTTP request (e.g. for gmail, a GET / to gmail.com returns 200)

### Testing

Create some tests that verify the expected behavior.

### Submit a Pull Request

Submit a pull request back to the repo for evaluation.

If anything goes wrong creating the pull request, zip up the files and send them to <anthony@assignguard.com>.
