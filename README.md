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

