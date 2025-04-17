#!/bin/bash

# ARM Architecture Docker Setup Script for SAR Project
echo "Setting up Docker for ARM architecture..."

# Clean up any previous Docker containers and volumes
echo "Cleaning up previous Docker containers and volumes..."
docker-compose down --volumes --remove-orphans
docker system prune -f

# Set up Buildx for multi-architecture support
echo "Setting up Docker Buildx for multi-architecture support..."
docker buildx create --name arm-builder --use || echo "Buildx already set up"
docker buildx inspect --bootstrap

# Detect architecture and set appropriate platform
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    echo "Detected 64-bit ARM architecture (arm64)"
    export BUILDPLATFORM=linux/arm64
elif [ "$ARCH" = "armv7l" ] || [ "$ARCH" = "armhf" ]; then
    echo "Detected 32-bit ARM architecture (armv7)"
    export BUILDPLATFORM=linux/arm/v7
else
    echo "Using default architecture settings"
    export BUILDPLATFORM=linux/amd64
fi

echo "Building with platform: $BUILDPLATFORM"

# Start Docker Compose with the appropriate platform
echo "Starting Docker Compose..."
docker-compose build --no-cache
docker-compose up

echo "Docker setup complete. If you encounter any issues, try running the following commands:"
echo "docker-compose down --volumes --remove-orphans"
echo "docker system prune -f"
echo "docker-compose build --no-cache"
echo "docker-compose up"