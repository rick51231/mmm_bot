envsubst '\$WEBHOOK_HOST' < /src/config/nginx/nginx.conf.template > /etc/nginx/conf.d/nginx.conf
nginx -g "daemon off;"
