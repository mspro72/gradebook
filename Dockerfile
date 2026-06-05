FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root --no-interaction

COPY . .

EXPOSE 5000

CMD ["poetry", "run", "python", "run.py"]