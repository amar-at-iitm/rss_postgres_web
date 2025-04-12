# Using the official PostgreSQL image
FROM postgres:latest

# Setting build arguments for PostgreSQL
ARG DB_USER
ARG DB_PASS
ARG DB_NAME

# Setting environment variables for PostgreSQL
ENV POSTGRES_USER=$DB_USER
ENV POSTGRES_PASSWORD=$DB_PASS
ENV POSTGRES_DB=$DB_NAME

COPY init.sql /docker-entrypoint-initdb.d/

# Exposing the default PostgreSQL port
EXPOSE 5432
