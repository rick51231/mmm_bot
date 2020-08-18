envsubst < /src/config/nginx/nginx.conf.template > /etc/nginx/conf.d/nginx.conf # /etc/nginx/conf.d/default.conf
nginx -g "daemon off;"
