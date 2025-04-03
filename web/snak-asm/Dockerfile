# Build stage
FROM rust:1.85 AS builder

RUN curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

WORKDIR /usr/src/app

COPY . .

RUN wasm-pack build --target web

# Serve stage
FROM nginx:alpine

COPY --from=builder /usr/src/app/pkg /usr/share/nginx/html/pkg
COPY --from=builder /usr/src/app/index.html /usr/share/nginx/html/

EXPOSE 80

# Use the default nginx command
CMD ["nginx", "-g", "daemon off;"]
