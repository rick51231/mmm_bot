
export INCLUDE="include /etc/nginx/conf.d/certificate/certificate.conf*;"

FILE=/var/www/certificate/certificate-cert.pem
if [ -f "$FILE" ]; then
    export INCLUDE="include /etc/nginx/conf.d/certificate/certificate.conf*;"
else
    export INCLUDE=""
fi

envsubst '\$WEBHOOK_HOST \$INCLUDE' < /src/config/nginx/nginx.conf.template > /etc/nginx/conf.d/nginx.conf
