FROM python:3.10

WORKDIR /opt/FastAPI-CRUD

RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files first to utilize Docker cache if unchanged.
COPY pyproject.toml poetry.lock ./

# Copy the remaining source code
COPY api ./api
COPY tests ./tests

# Expose the required port
EXPOSE 8000

# Install the dependencies defined in pyproject.toml
RUN poetry install

# Set the entrypoint command to run the FastAPI application using uvicorn
ENTRYPOINT ["poetry", "run", "python", "api/main.py"]
