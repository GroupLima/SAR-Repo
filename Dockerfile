# Use an official Node.js runtime as a parent image for the front-end
FROM node:18 AS frontend
WORKDIR /app/search-app/front-end
COPY search-app/front-end/package*.json ./
RUN npm install

# Use an official PHP runtime as a parent image for the back-end
FROM php:8.2-cli AS backend

# Install system dependencies, including Python and necessary tools
RUN apt-get update && apt-get install -y \
    unzip \
    libzip-dev \
    python3 \
    python3-venv \
    python3-pip \
    && docker-php-ext-install zip

# Set the working directory for the back-end
WORKDIR /app/search-app/back-end

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copy the back-end source code
COPY search-app/back-end .

# Create a Python virtual environment and install dependencies
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -Ur requirements.txt

# Ensure that the virtual environment’s binaries are used
ENV PATH="/opt/venv/bin:$PATH"

# Install PHP dependencies with Composer
RUN composer install

# Expose ports for front-end and back-end
EXPOSE 3000 8000

# Start the PHP server
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
