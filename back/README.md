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

- SECRET_KEY: A secret key for the application for security purposes. Obligatory.

- MYSQL_HOST: The host of the MySQL database. Obligatory.
- MYSQL_PORT: The port of the MySQL database. Default: 3306
- MYSQL_USER: The user of the MySQL database. Obligatory.
- MYSQL_PASSWORD: The password of the MySQL database. Optional if the database doesn't have a password.
- MYSQL_DATABASE: The name of the MySQL database. Obligatory.

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
Soon to be added.

## Testing
Soon to be added.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
