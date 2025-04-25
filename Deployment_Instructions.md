1. Choose VPS provider, or use your own. This setup currently uses the Oracle cloud VPS which provides an ARM Ubuntu instance.
    - Keep in mind if a system that is other than Ubuntu on ARM is used, the docker files will need altering to reflect this.

2. Choose DNR (Domain Name Registrar). This setup currently uses the Cloudflare service.

3. SSH into your VPS (search and follow a guide if you don't know how to set this up)

4. Either manually copy the project or clone it in the home directory (just type `cd` to get there) from Github by first setting your global name and username with `git config --global user.name "Mona Lisa"` and `git config --global user.email "MonaLisa@example.com"`
    - Then authenticate to github by [generating ssh keys guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
5. Install certbot and its dependencies with `sudo apt install python3 python3-certbot python3-certbot-nginx python3-venv libaugeas0`
6. Use ufw or another firewall service to open the needed ports, remember if you are using a VPS to also open these ports on the subnet/security system on there too. We only require the subnet to add the http and https ports be open (80 and 443). Ensure that if this is a server you don't have physical access to that you enable port 22 on the firewall service before applying any rule changes.
    - For example with ufw it is     
        - `sudo apt install ufw`
        - `sudo ufw allow 443 && sudo ufw allow 80 && sudo ufw allow 22 && sudo systemctl enable ufw` this opens the https, http and ssh ports respectively
        - Check if ufw was really enabled by typing `sudo systemctl status ufw` and if there are all greens/enabled signs then it is fine, otherwise retry with `sudo systemctl enable ufw`
        - Sometimes you have to reboot the VPS to get the firewall properly active by doing `sudo reboot` 
7. Install nginx with `sudo apt install nginx`
    - Create the nginx config file for your site using `sudo touch /etc/nginx/sites-available/your_optional_subdomain.your_domain_name.domain_extension` - for this project I am currently deploying on a subdomain `sar2` with the domain name `andreasmaita` and the domain extension `.com` which comprises `sar2.andreasmaita.com`. Assume all further instructions with this domain can be replaced with your domain.
    - Paste in your configuration, the current one is:
```
server {
    listen 80;
    server_name sar2.andreasmaita.com;
    
    # Let's Encrypt verification must come BEFORE any redirects
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect all HTTP traffic to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name sar2.andreasmaita.com;
    
    ssl_certificate /etc/letsencrypt/live/sar2.andreasmaita.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sar2.andreasmaita.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    # Frontend - Proxy to Vite dev server
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (required for hot module reload)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Backend - Proxy API requests to Laravel/PHP backend
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
7.
    - Create a symbolic link to the config file using `sudo ln -s /etc/nginx/sites-available/sar2.andreasmaita.com /etc/nginx/sites-enabled/`
    - Restart nginx with `sudo systemctl restart nginx`
    - Run certbot and register your certificates with liveencrypt using `sudo certbot --nginx -d sar2.andreasmaita.com`
    - Install SSL certificates such that your site can use secure HTTPS instead of just HTTP with `sudo certbot install --cert-name sar2.andreasmaita.com`
    - Update your nginx config file for your domain such that it handles SSL encryption and allows HTTPS connection by adding the following to the end of your previous nginx configuration 
8. Install docker and docker-compose using the instructions at [guide](https://medium.com/@piyushkashyap045/comprehensive-guide-installing-docker-and-docker-compose-on-windows-linux-and-macos-a022cf82ac0b)
    - Either re-log into the system or run `newgrp docker` to refresh permissions
9. Make sure the backend and other ports needed for the project are exposed with `sudo ufw allow <port_number>` e.g. port 8000 for php + python backend
10. Go to the `SAR-Repo` directory and run the project using `docker-compose up -d`, or instead I personally like the auto attach feature of using `docker-compose up --build`
11. If there are any issues with the docker environment or containers, attempt to reset the containers and everything with these commands `docker-compose down --volumes --remove-orphans && docker system prune -f` and then run the command from the previous step