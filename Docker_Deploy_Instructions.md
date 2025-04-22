# Docker Deployment Instructions for SAR Project

## Installing Docker on Ubuntu

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose

# Start Docker service
sudo systemctl start docker
#### sudo systemctl enable docker to keep it persistent

# Add your user to the docker group to avoid permission issues
sudo usermod -aG docker $USER
newgrp docker
```

## Running the SAR Project with Docker

### Before Starting

Clean up any previous Docker containers and volumes:

```bash
docker-compose down --volumes --remove-orphans
docker system prune -f
```

### Launching the Application

```bash
# Start the application
docker-compose up --build
```

### Troubleshooting ContainerConfig Error

If you encounter the 'ContainerConfig' KeyError (common on ARM architectures), try:

```bash
# First, force remove all containers and volumes
docker-compose down --volumes --remove-orphans
docker system prune -a -f --volumes

# Then, rebuild without cache and with specific platform settings
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build --no-cache
docker-compose up
```

If running on ARM (like AWS Graviton, M1/M2 Macs, etc.), you may need to specifically pull images that support your architecture:

```bash
# Pull compatible images explicitly
docker pull --platform=linux/arm64 node:23-slim
docker pull --platform=linux/arm64 php:8.4.6-cli
```

### Maintenance Commands

```bash
# Stop the containers
docker-compose down

# Enter a container's shell (replace container_name with actual name or ID)
docker exec -it container_name /bin/sh

# View logs for a specific container
docker logs container_name

# Follow logs in real-time
docker logs -f container_name
```

### Image Version Details
This project uses:
- Node.js 23
- PHP 8.4.6


## Setup reverse proxy

sudo apt install ufw -y
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 22
sudo ufw enable

this needs to port forward :8000 and :5173 for the front and back end

sudo apt update
sudo apt install -y nginx

use your DNS registrar to setup the DNS A record
make it a flexible type SSL