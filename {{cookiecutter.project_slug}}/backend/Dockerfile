FROM python:3.8 as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Install pipenv and compilation dependencies
RUN pip install pipenv
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
WORKDIR /app
COPY ./app/Pipfile* .
RUN pipenv install --system --deploy --ignore-pipfile

# Install application into container
WORKDIR /app
COPY ./app .
ENV PYTHONPATH=/app

EXPOSE 80
# RUN bash -c 'echo -e 12345'
# RUN chmod u+x ./prestart.sh
# RUN ./prestart.sh
# RUN ["python","app/backend_pre_start.py"]

CMD ["/start.sh"]
