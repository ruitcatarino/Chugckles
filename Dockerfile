FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /src/app

WORKDIR /src/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]