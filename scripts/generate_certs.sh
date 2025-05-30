#!/bin/bash
CERT_DIR="./reverse-proxy/certs"
# Controleer of de map 'certs' al bestaat en er bestanden in zitten
if [ -d "$CERT_DIR" ] && [ "$(ls -A $CERT_DIR)" ]; then
    echo "Certificates already exist in $CERT_DIR. Skipping generation."
else
    echo "Generating self-signed certificates in $CERT_DIR..."
    mkdir -p $CERT_DIR
    openssl req -x509 -nodes -days 365 \
        -newkey rsa:2048 -keyout $CERT_DIR/nginx-selfsigned.key \
        -out $CERT_DIR/nginx-selfsigned.crt \
        -subj "/CN=localhost"
    echo "Self-signed certificates generated."
fi
