# MeLi Risk Management Challenge - Frontend
The following project is a challenge proposed by Mercado Libre for a position as a backend developer in the Risk Management team.

## Prerequisites
- Node.js 14.15.4 or higher
- npm 6.14.10 or higher
- Docker (optional)

## Getting Started
To get started with this project, you can clone this repository and install the dependencies.

To install all the dependencies with npm, run the following command:
```bash
npm install
```

### Build and run with Docker
To build the image, run the following command:
```bash
docker build -t image-name .
```

To run the container, run the following command:
```bash
docker run -d --name container-name -p 3000:3000 image-name
```

Change the variables image-name and container-name to your liking.

### Run with npm
To run the application locally, run the following command to start the development server:
```bash
npm start
```

To build the application, run the following command:
```bash
npm run build
```

## Architecture
The project follows the principles of Model-View-Controller with the atomic design pattern, separating the application into three layers: atoms, molecules and pages.

- Atoms: This layer is responsible for representing the smallest components of the application, such as buttons, inputs, etc.
- Molecules: This layer is responsible for representing the components of the application that are composed of atoms, such as forms, cards, etc.
- Pages: This layer is responsible for representing the pages of the application, such as the home page, the search page, etc.

## Available Scripts
- Dev
- Build
- Start
- Preview
- Astro

- npm run start: Runs the app in the development mode.
- npm run build: Builds the app for production pourposes to the build folder.
- npm run dev: Runs the app in the development mode with Astro.
- npm run preview: Runs the app in the production mode.
- npm run astro: Runs the app in the development mode with Astro.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.