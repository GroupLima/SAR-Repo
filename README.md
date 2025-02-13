# SAR-Project

New Search Aberdeen Registers (SAR) search tool web application project
<br>A modernised, maintainable version of [sar.abdn.ac.uk](sar.abdn.ac.uk)
<br> We are going to get an A1!!
<br> ☆*: .｡. o(≧▽≦)o .｡.:*☆

## Team Lima

Developers: Caitlin Thaeler, Piotr Smialek, Holly Sinclair, Andreas Maita, Fariha Ibnat, Rebekah Leslie, Haziel Osunde, Dermot Stelfox
<br>For CS3028 Principles of Software Engineering, University of Aberdeen

## Instructions for Running the Project

If you are not a member of our organisation, you may either want to create a fork of this repository so you can clone it on your device, or simply download the search-app directory using [this link](https://download-directory.github.io/?url=https://github.com/GroupLima/SAR-Repo/tree/main/search-app). If you are using WSL + GitHub Desktop to clone the project, you will need to map your network drive if you haven't done so already so that GitHub Desktop knows the correct location to clone the repo.

Now, you will need to install a few packages and dependencies in order to run the laravel project. The following instructions are for Linux or WSL environments, but you should also be able to successfully run the website on macOS as well.

### Download PHP, Laravel and Composer:

1. `sudo apt update`
2. `sudo apt upgrade`
3. `sudo apt install nodejs`
4. `sudo apt install unzip`
5. Install PHP for your system (ONLY ONE OF THESE)
   - Linux: `/bin/bash -c "$(curl -fsSL https://php.new/install/linux)"`
   - MaxOS:`/bin/bash -c "$(curl -fsSL https://php.new/install/mac)"`

`sudo apt-get install php-mbstring php-xml php-json php-zip php-curl`

### Running the Project

#### Back-End

1. Source the python virtual environment `source venv_sar/bin/activate` (this is relative to the repository, so assumes you are in the root directory of the repository)
2. Install the python requirements (only on first setup/run) `pip install -r venv_sar/requirements.txt`
3. Go to the back-end directory `cd search-app/back-end`
4. Install the composer requirements (only on first setup/run) `composer install`
5. Run PHP server using `php artisan serve`

#### Front-end

1. Open second terminal, keeping the first running
2. Go to the front-end directory `cd search-app/front-end`
3. Install NPM requirements (only on first setup/run) `npm install`
4. Run Vite Server with Vue tooling
   1. NOT FOR DEPLOYMENT BECAUSE HAS DEV PRIVILLEGES `npm run dev`
