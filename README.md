# Textbook Marketplace Prototype

Prototype website for Team Downtown's capstone project.
 
# Setup Guide

This section describes the process of setting up and running the server on a local machine. XAMPP is chosen for its ease of installation, but other MySQL distributions may be used.

## Installing MySQL

- Download and install [XAMPP](https://www.apachefriends.org/download.html) (version 7.3.9 at time of writing). For this guide you must install the Apache, MySQL, and phpMyAdmin components.
- Run XAMPP and start the Apache and MySQL modules. Apache is used to configure the database through a web interface, and may be shut down afterwards.
- Click the Admin button for MySQL to open the phpMyAdmin interface. In the Databases tab, create a new database named `marketplace` with `utf8_bin` encoding.
- In the User accounts tab, add a new user for the Django server to use, with a username and password of your choice. Click "Check all" in the privileges section before confirming.
- The database is now ready to be configured by the server. Make sure to start MySQL whenever you run the Django server.

## Installing Python

- Download and install [Python 3](https://www.python.org/downloads/) (version 3.7.4 at time of writing, make sure to get the 64-bit version if you are on 64-bit Windows). In the installer, include pip and add Python to environment variables. I also recommend selecting "Associate files with Python" for convenience.
- Open a command line and enter `pip install virtualenvwrapper-win` to begin creating a virtual environment for Django development.
- Run `mkvirtualenv django` to create an environment named "django" (or whatever you choose to call it). You will automatically enter the environment when creating it; in the future you can enter it with the command `workon django`.
- Once in the environment, `pip install` django, mysqlclient, pillow, and requests.

## Server Setup

- Clone this repository to your machine.
- Open textbookMarketplace\settings.py and scroll down to the DATABASES dictionary; edit the USER and PASSWORD to match the account you created in XAMPP earlier.
- Open a command line and navigate to to the main project folder. Enter `manage.py makemigrations` (or `python manage.py makemigrations` if you did not associate files), then `manage.py migrate` to finish configuring the database.
- Enter `manage.py load_market_data` to populate the database, then start the server with `manage.py runserver`.
- If all went well, the site can now be accessed through your browser at `localhost:8000/`.
