FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/app/requirements.txt

COPY . /src/app

COPY ./utils/ipython/ipython_config.py /root/.ipython/profile_default/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]