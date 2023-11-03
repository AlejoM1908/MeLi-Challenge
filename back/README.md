# MeLi Risk Management Challenge - Backend
The following project is a challenge proposed by Mercado Libre for a position as a backend developer in the Risk Management team.

## Prerequisites
- Python 3.8 or higher
- Docker (optional)
- pip (recommended)

## Getting Started
To get started with this project, you can clone this repository, intall the dependencies and create a .flaskenv with the environment variables of your choice.

To install all the dependencies with pip, run the following command:
```bash
pip install -r requirements.txt
```

I highly recommend using a virtual environment to install the dependencies. You can see the [python documentation](https://docs.python.org/3/library/venv.html) about them for more information.

### Environment variables guide
For the .flaskenv file, you can use the following variables:

- FLASK_APP: The name of the application. Obligatory: src.
- FLASK_ENV: The environment in which the application is running. Default: production
- FLASK_DEBUG: Enable or disable debug mode. Default: 0
- FLASK_RUN_HOST: The host to listen on. Default: 127.0.0.1 (localhost)
- FLASK_RUN_PORT: The port to listen on. Default: 5000

For the .env file, you can use the following variables:

- JWT_SECRET: A secret key for the application for security purposes. Obligatory.
- REFRESH_SECRET: A secret key for the application for security purposes. Obligatory.

- MYSQL_HOST: The host of the MySQL database. Obligatory.
- MYSQL_PORT: The port of the MySQL database. Default: 3306
- MYSQL_USER: The user of the MySQL database. Obligatory.
- MYSQL_PASS: The password of the MySQL database. Optional if the database doesn't have a password.
- MYSQL_NAME: The name of the MySQL database. Obligatory.

- COUNTRY_API_URL: The URL of the country API. Obligatory.

### Build and run with Docker
To build the image, run the following command:
```bash
docker build -t image-name .
```

To run the container, run the following command:
```bash
docker run -d --name container-name -p 5000:5000 image-name
```

Change the variables image-name and container-name to your liking.

If you want to run the container with a different port, change the exposed port in the Dockerfile, the port in the .flaskenv file and the port in the docker run command.

### Run with Flask
To run the application locally, run the following command:
```bash
flask run
```

## Architecture
The project follows the principles of clean architectures, separating the application into four layers: external services, gateways, use cases and entities.

- External services: This layer is responsible for communicating with external services, such as the database, the flask framework, etc.
- Gateways: This layer is responsible for generating a communication interface between the external services and the use cases.
- Use cases: This layer is responsible for the business logic of the application.
- Entities: This layer is responsible for representing the entities of the application in a way that is easy to understand and manipulate.

## Endpoints
You can access all the endpoints with a Swagger UI in the following URL: FLASK_RUN_HOST:FLASK_RUN_PORT/swagger, or if you prefer runnig it with postman, in the root of the project you can find a file called MeLi Risk Management Challenge.postman_collection.json with all the endpoints to load to postman.

## Authentication Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/v1.1/login` | Login endpoint. Returns a JWT token and a refresh token. |
| `/v1.1/refresh` | Refresh endpoint. Returns a new JWT token and a new refresh token. Requires a refresh token as a Cookie header. |
| `/v1.1/register` | Register endpoint. Registers a new user. |

## Provider Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/v1.1/providers` | Providers endpoint. Supports GET and POST methods. Requires a JWT token as a Bearer Token header. |
| `/v1.1/providers/<provider_id>` | Provider endpoint. Supports GET, PUT, and DELETE methods. Requires a JWT token as a Bearer Token header. |

## Role Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/v1.1/roles` | Roles endpoint. Supports GET and POST methods. Requires a JWT token as a Bearer Token header. |
| `/v1.1/roles/<role_id>` | Role endpoint. Supports GET, PUT, and DELETE methods. Requires a JWT token as a Bearer Token header. |

## Risk Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/v1.1/risks` | Risks endpoint. Supports GET and POST methods. Requires a JWT token as a Bearer Token header. |
| `/v1.1/risks/<risk_id>` | Risk endpoint. Supports GET, PUT, and DELETE methods. Requires a JWT token as a Bearer Token header. |

## User Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/v1.1/profile` | Profile endpoint. Returns all the info of the token user. Requires a JWT token as a Bearer Token header. |
| `/v1.1/users/<user_id>/roles` | Gets all the roles of a user. Requires a JWT token as a Bearer Token header. |
| `/v1.1/users/<user_id>/roles/<role_id>` | Adds or removes a role from a user. Requires a JWT token as a Bearer Token header. |
| `/v1.1/risks/<risk_id>/users/<user_id>` | Adds or removes links between risks and users. Requires a JWT token as a Bearer Token header. |

## Data Filtering

The endpoint `/v1.1/risks` has a Query Parameter functionality that allows for single and multiple filters. The filters are:

- `provider:<provider_id>` - Filter by provider id.
- `user:<user_id>` - Filter by user id.
- `probability:<probability>` - Filter by probability. Can be ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']
- `impact:<impact>` - Filter by impact. Can be ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']
- `<string>` - If the length is 3, query the country API for match, so filtering by country, else query the database for match in risks name or description.

You can format the query parameters as you like, for example:
- `/v1.1/risks?provider=1,user=1,probability=VERY_LOW,impact=VERY_LOW,arg`


## Testing
The automatic white box unit testing was developed with pytest. To run the tests, run the following command:

```bash
pytest
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
