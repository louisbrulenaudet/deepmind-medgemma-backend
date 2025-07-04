# Hackaton Google : Solve for Healthcare & Life Sciences with Gemma

In order to run the backend the fastest way possible, you can use the makefile setup and uv for Python dependency management as this:

```sh
make init
make upgrade
make dev
```

Then you can ping the API at [http://127.0.0.1:8000/api/v1/ping](http://127.0.0.1:8000/api/v1/ping).

Warning, if you run the app through Docker, you will need to use the unsecure 80 port in order to facilitate the domain resultion using in production. So, the url will be [http://localhost/api/v1/ping](http://localhost/api/v1/ping).


## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose for containerization and deployment.
- [uv](https://github.com/astral-sh/uv) (Python dependency manager)
- [ruff](https://docs.astral.sh/ruff/) (linter/formatter)

---

## Environment Setup

1. Copy `.env.template` to `.env` and adjust variables as needed.

---

## Quick Start

### 1. Initialize the environment

```sh
make init
```

### 2. Build Docker containers

```sh
make build
```

### 2.1 Rebuild and restart containers

```sh
make rebuild
```

### 3. Start FastAPI server

```sh
make dev
```

- The API will be available at [http://localhost:8688](http://localhost:8688) by default.

### 4. Stop services

```sh
make stop
```

### 5. Clean up containers and volumes

```sh
make clean
```

---

## Code Quality

- Lint and check code:

  ```sh
  make check
  ```

- Format code:

  ```sh
  make format
  ```
