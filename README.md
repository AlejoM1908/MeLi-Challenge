# MeLi Risk Management Challenge
The following repository contains the code for a MeLi technical challenge. The goal is to design, implement and generate some DevOps tools to help testing the solution on future iterations.

## The Challenge
The challenge consists on a CRUD API for a risk management system in cybersecurity and must be implemented in the Flask framework for Python, while the frontend must be implemented in React. The API must be able to create, read, update and delete risks, and the frontend must be able to display the risks and allow the user to interact with them and create some filtering options.

## The Solution
In each of the directories you will find a more detailed README.md file with the instructions to run the code, but here is a brief description of the solution:

### Backend
Designed in a Clean Architecture aproach, divided in four layers: External services, gateways, use cases and entities. The communication can be done inward using simple estructures and calls, and outward using the interfaces defined in the gateways layer. This allows for a more modular and testable code that can be easily modified and extended, find more information in the [README](back/README.md) of the backend implementation.

### Frontend
Designed using React, Tailwind and Typescript. Is deployed using the web framework Astro, which allows for a more SEO friendly and faster loading website with its island architecture. It has an aproach to the principles of Model-View-Controller with the atomic design pattern on top, wich allows for a more modular and reusable code, find more information in the [README](front/README.md) of the frontend implementation.

### Docker Compose deployment
The solution can be deployed using Docker Compose, which allows for a more portable and scalable deployment of the solution. To deploy the solution, follow this steps:

1. Clone the repository
2. Create the .flaskenv and the .env files in the back as described in the [README](back/README.md) of the backend implementation.
3. Set the MYSQL_HOST variable in the .env file to the name of the database service in the [docker-compose.yml](./docker-compose.yml) file. (The default is db)
4. Set a strong password for the MYSQL_PASS variable in the .env file and also add it to the MYSQL_ROOT_PASSWORD variable in the [docker-compose.yml](./docker-compose.yml) file.
5. Run the following command in the root of the project:
```bash
docker-compose up -d --build
```

the solution will be deployed in the port 5000 of the host machine, but you can change it in the [docker-compose.yml](./docker-compose.yml) file.