FROM nginx:latest

RUN apt update
RUN apt install -y certbot
RUN apt install -y python3-certbot-nginx
RUN mkdir -p /var/www/certbot

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/
