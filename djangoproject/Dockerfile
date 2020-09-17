# FROM python:3.8.5-buster

# LABEL key="MemesBD"

# ADD . /api
# WORKDIR /api
# # You will need this if you need PostgreSQL, otherwise just skip this
# # RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
# # RUN pip install uwsgi
# RUN pip install -r requirements.txt

# RUN sh initdb.sh
# # RUN python manage.py collectstatic

# ENV PORT=8000
# EXPOSE 8000
# # Runner script here
# # CMD ["/api/runner.sh"]
# # CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "mememaker.wsgi:application"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# # docker build -t mememaker -f Dockerfile .
# # docker run -it -p 80:8000 mememaker


FROM python:3.8.5

ENV PYTHONDONTWRITEBYTECODE 1 # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 # Prevents Python from buffering stdout and stderr

ENV PATH="/scripts:${PATH}"

# RUN mkdir /app
ADD djangoproject /app
WORKDIR /app


RUN apt-get update \
    &&  apt-get install gcc libc-dev g++ libffi-dev libxml2 libffi-dev unixodbc-dev -y \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip


COPY djangoproject/requirements.txt /app/
RUN pip install -r  requirements.txt
RUN pip install uwsgi==2.0.19
RUN apt-get purge -y --auto-remove gcc


COPY scripts /scripts
RUN chmod +x /scripts/*


COPY djangoproject /app/


RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser --disabled-password user

RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

#USER user


RUN find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && \
	find . -path "*/migrations/*.pyc"  -delete

RUN python manage.py makemigrations && \
    python manage.py migrate

RUN python manage.py collectstatic --no-input

CMD ["entrypoint.sh"]
