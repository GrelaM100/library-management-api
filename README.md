# Library Management API

This is a simple API for managing a library system. The API allows library staff to track and update the status of books in the library. Each book has a unique serial number, title, author, and information about whether it is currently borrowed and by whom.

## Features

- Add a new book
- Remove a book
- Retrieve a list of all books
- Get details of a book by serial number
- Update the status of a book (borrowed/available)

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

    ```sh
    git clone https://github.com/GrelaM100/library-management-api.git
    cd library-management-api
    ```


2. Build and run the application using Docker Compose:

    ```sh
    docker-compose up
    ```

    To run the application in detached mode, use:

    ```sh
    docker-compose up -d
    ```

    Note: If the `INIT_DB` variable is set to `true`, the database will be initialized with 3 example books.

3. The application will be available at `http://localhost:8000`.

4. Auto-generated API documentation is available at:

    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

## Running Tests

To run the tests, use the following command:

```sh
docker-compose exec api bash /app/tests-start.sh
