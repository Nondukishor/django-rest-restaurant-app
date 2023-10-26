FROM python:3.11
WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pip install --upgrade pip
RUN pipenv install --dev
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin
COPY . /app/
EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]