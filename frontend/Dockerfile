ARG NODE_VERSION=22-alpine

FROM node:${NODE_VERSION} AS builder

ARG APP_PATH=/app

WORKDIR ${APP_PATH}

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:stable-alpine AS web-runtime

ARG APP_PATH=/app

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder ${APP_PATH}/dist /usr/share/nginx/html

COPY <<EOF /etc/nginx/nginx.conf
events {}
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen       80;
        server_name  _;

        root   /usr/share/nginx/html;
        index  index.html;

        location / {
            try_files \$uri \$uri/ /index.html;
        }

        location /healthcheck {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

EXPOSE 80

RUN apk add --no-cache curl

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/healthcheck || exit 1
