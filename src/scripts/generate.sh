
export INCLUDE="include /etc/nginx/conf.d/certificate/certificate.conf*;"
FILE=/var/www/certificate/certificate-cert.pem

for (( i=1; i <= 10; i++ ))
do
  if [ -f "$FILE" ]; then
      export INCLUDE="include /etc/nginx/conf.d/certificate/certificate.conf*;"
      break
  else
      /code/certificate/acme.sh --issue --dns dns_cf -d $WEBHOOK_HOST -d www.$WEBHOOK_HOST --key-file /code/certificate/certificate-key.pem --fullchain-file /code/certificate/certificate-cert.pem
  fi
done


envsubst '\$WEBHOOK_HOST \$INCLUDE' < /src/config/nginx/nginx.conf.template > /etc/nginx/conf.d/nginx.conf
