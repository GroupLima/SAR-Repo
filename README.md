# SAR-Project

New Search Aberdeen Registers (SAR) search tool web application project
<br>A modernised, maintainable version of [sar.abdn.ac.uk](sar.abdn.ac.uk)
<br> Project implementation seen at [sar2.andreasmaita.com](http://sar2.andreasmaita.com)
<br> We are going to get an A1!!
<br> ☆*: .｡. o(≧▽≦)o .｡.:*☆

## Team Lima

Developers: Caitlin Thaeler, Piotr Smialek, Holly Sinclair, Andreas Maita, Fariha Ibnat, Rebekah Leslie, Haziel Osunde, Dermot Stelfox
<br>For CS3028 Principles of Software Engineering, University of Aberdeen

## Instructions for Running the Project

If you are not a member of our organisation, you may either want to create a fork of this repository so you can clone it on your device, or simply download the search-app directory using [this link](https://download-directory.github.io/?url=https://github.com/GroupLima/SAR-Repo/tree/main/search-app). If you are using WSL + GitHub Desktop to clone the project, you will need to map your network drive if you haven't done so already so that GitHub Desktop knows the correct location to clone the repo.

Now, you will need to install a few packages and dependencies in order to run the laravel project. The following instructions are for Linux or WSL environments, but you should also be able to successfully run the website on macOS as well.

### Download PHP, Laravel and Composer:

#### Linux (Debian-based)

1. `sudo apt update && sudo apt upgrade`
2. `sudo apt install nodejs unzip`
3. Install PHP for your system `/bin/bash -c "$(curl -fsSL https://php.new/install/linux)"`
4. `sudo apt-get install php-mbstring php-xml php-json php-zip php-curl`

#### MacOS

1. Assuming you have [homebrew](https://docs.brew.sh/Installation) installed, otherwise substitute `brew` in the following commands for your package manager
2. `brew upgrade`
3. Install system requirements `brew install nodejs unzip php-mbstring php-xml php-json php-zip php-curl` (NOT ACCURATE, SOME PACKAGES NOT ON HOMEBREW - TO DO)
4. Install PHP for your system `/bin/bash -c "$(curl -fsSL https://php.new/install/mac)"`

### Running the Project

1. Change directory to the search app `cd search-app`

#### Back-End

1. Change directory to back-end with `cd back-end`
2. Create the python virtual environment `python3 -m venv venv_sar` (need to make a new venv for each system, don't need to remake it if it is already there but make sure it is all entirely ignored by the repo)
3. Source the python virtual environment `source venv_sar/bin/activate`
4. Install the python requirements (only on first setup/run) `pip install -r requirements-pip.txt`
5. Go to the back-end directory `cd search-app/back-end`
6. Install the composer requirements (only on first setup/run) `composer install`
7. Run PHP server using `php artisan serve`

#### Front-end

1. Change directory to front-end (assuming currently in back-end) with `cd ../front-end`
2. Open second terminal, keeping the first running
3. Go to the front-end directory `cd search-app/front-end`
4. Install NPM requirements (only on first setup/run) `npm install`
5. Run Vite Server with Vue tooling:
   1. Deploy site and run regularly with:
      1. Compile site only on first run / site changes being made `npm run build`
      2. Run with `npm run preview`
   2. NOT FOR DEPLOYMENT BECAUSE HAS DEV PRIVILLEGES `npm run dev`
