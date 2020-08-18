
export INCLUDE="include /etc/nginx/conf.d/certificate/certificate.conf*;"

FILE=/var/www/certificate/certificate-cert.pem
if [ -f "$FILE" ]; then
    export INCLUDE="include /etc/nginx/conf.d/certificate/certificate.conf*;"
else
    /code/certificate/acme.sh --issue --dns dns_cf -d bot."$WEBHOOK" -d www.""$WEBHOOK" --key-file /code/certificate/certificate-key.pem --fullchain-file /code/certificate/certificate-cert.pem
    export INCLUDE=""
fi

envsubst '\$WEBHOOK_HOST \$INCLUDE' < /src/config/nginx/nginx.conf.template > /etc/nginx/conf.d/nginx.conf
