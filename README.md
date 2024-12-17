# Flask Weather API

This repository contains a Flask-based Weather API application.

## Project Structure

- `.github/`: GitHub-related configurations (e.g., workflows)
- `.vscode/`: Visual Studio Code configuration
- `tests/`: Directory containing test files
- `weather/`: Main application directory
- `docker-compose.yml`: Docker Compose configuration file
- `Makefile`: Makefile for project commands
- `nginx.conf`: Nginx configuration file

## Getting Started

To run this project, you'll need Docker and Docker Compose installed on your system.

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Start the application using Docker Compose:
   ```
   docker-compose up --build
   ```

3. The API should now be accessible at `http://localhost:8080`

## Development

To run tests:
```
make test
```

For more commands, check the `Makefile`.

## License

This project is licensed under the terms of the LICENSE file in the repository.
