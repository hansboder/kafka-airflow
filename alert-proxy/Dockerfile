# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install Poetry
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get remove -y curl

# Set PATH for Poetry
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

COPY . /app

# Install dependencies
RUN poetry install --no-root

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:5000"

# Run app.py when the container launches
CMD ["poetry", "run", "gunicorn", "app:app"]
