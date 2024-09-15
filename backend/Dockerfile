FROM python:3.12.0-alpine

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apk update
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

# CMD ["npm", "start"]

# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["python3", "app/main.py"]