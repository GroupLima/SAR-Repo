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
    && docker-php-ext-install zip

# Set the working directory for the back-end
WORKDIR /app/search-app/back-end

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copy the back-end source code
COPY search-app/back-end .

# Ensure the artisan file is present
RUN ls -la /app/search-app/back-end

# Install back-end dependencies
RUN composer install

# Expose ports for front-end and back-end
EXPOSE 3000 8000

# Start both front-end and back-end services
CMD ["sh", "-c", "cd /app/search-app/front-end && npm run dev & cd /app/search-app/back-end && source venv_sar/bin/activate && php artisan serve --host=0.0.0.0"]
