FROM node:18-alpine AS builder
MAINTAINER Lars van Rhijn <larsvanrhijn@gmail.com>
LABEL description="Mentorpunten VueJS application"

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
# Include the .env file for build-time environment variables
COPY . ./
RUN npm run build-only

FROM nginx
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/dist .
COPY docker.blueprint.env /usr/share/nginx/docker.blueprint.env
COPY resources/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
