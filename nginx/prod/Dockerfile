FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx/prod/default.conf /etc/nginx/conf.d/default.conf

COPY ./nginx/prod/uwsgi_params /etc/nginx/uwsgi_params

COPY ./nginx/prod/nginx.conf /etc/nginx/nginx.conf


USER root

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static

