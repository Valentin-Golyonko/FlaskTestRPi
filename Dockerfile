FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends python3-dev python3-gpiozero libpq-dev nano

WORKDIR /homebox
RUN python -m pip install --upgrade setuptools pip wheel
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]