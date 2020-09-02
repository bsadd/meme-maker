FROM python:3.8.5-buster

LABEL key="MemesBD"

ADD . /api
WORKDIR /api
# You will need this if you need PostgreSQL, otherwise just skip this
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
# RUN pip install uwsgi
RUN pip install -r requirements.txt

RUN sh initdb.sh
# RUN python manage.py collectstatic

ENV PORT=8000
EXPOSE 8000
# Runner script here
# CMD ["/api/runner.sh"]
# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "mememaker.wsgi:application"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# docker build -t mememaker -f Dockerfile .
# docker run -it -p 80:8000 mememaker