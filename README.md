# SAR-Project
New Search Aberdeen Registers (SAR) search tool web application project
<br>A modernised, maintainable version of [sar.abdn.ac.uk](sar.abdn.ac.uk)
<br> We are going to get an A1!!
<br> ☆*: .｡. o(≧▽≦)o .｡.:*☆

### Team Lima
Developers: Caitlin Thaeler, Piotr Smialek, Holly Sinclair, Andreas Maita, Fariha Ibnat, Rebekah Leslie, Haziel Osunde, Dermot Stelfox
<br>For CS3028 Principles of Software Engineering, University of Aberdeen

### Instructions for Running the Project

If you are not a member of our organisation, you may either want to create a fork of this repository so you can clone it on your device, or simply download the search-app directory using [this link](https://download-directory.github.io/?url=https://github.com/GroupLima/SAR-Repo/tree/main/search-app). If you are using WSL + GitHub Desktop to clone the project, you will need to map your network drive if you haven't done so already so that GitHub Desktop knows the correct location to clone the repo.

Now, you will need to install a few packages and dependencies in order to run the laravel project. The following instructions are for Linux or WSL environments, but you should also be able to successfully run the website on macOS as well.

#### Download PHP, Laravel and Composer:
`sudo apt update`
<br>`sudo apt upgrade`
<br>`sudo apt install nodejs`
<br>`sudo apt install unzip`

Linux:
* `/bin/bash -c "$(curl -fsSL https://php.new/install/linux)"`

MaxOS:
* `/bin/bash -c "$(curl -fsSL https://php.new/install/mac)"`

`sudo apt-get install php-mbstring php-xml php-json php-zip php-curl`
<br>`sudo apt install python3-rapidfuzz`

Now you want to either close the terminal and reopen, or use source.
<br>Navigate to search-app and type `composer install` into the terminal, followed by `php artisan serve` . Now you should be able to access the application by clicking the url in the terminal.


