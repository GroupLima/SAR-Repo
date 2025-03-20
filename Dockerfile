# Use an official Node.js runtime as a parent image
FROM node:18 AS frontend

# Set the working directory for the front-end
WORKDIR /app/search-app/front-end

# Install front-end dependencies
COPY search-app/front-end/package*.json ./
RUN npm install

# Use an official PHP runtime as a parent image
FROM php:8.2-cli AS backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    libzip-dev \
    python3 \
    python3-venv \
    python3-pip \
    && docker-php-ext-install zip \
    || (brew update && brew install unzip libzip python3 && pip3 install virtualenv)

# Set the working directory for the back-end
WORKDIR /app/search-app/back-end

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copy the back-end source code
COPY search-app/back-end .

# Create and activate the virtual environment
RUN python3 -m venv venv-sar && . venv-sar/bin/activate

# Install Python dependencies
COPY search-app/back-end/requirements.txt .
RUN . venv-sar/bin/activate && pip install -r requirements.txt

# Install back-end dependencies
RUN composer install

# Expose ports for front-end and back-end
EXPOSE 3000 8000

# Start the PHP server
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
