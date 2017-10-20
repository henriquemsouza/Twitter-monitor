# Twitter-monitor
Social Monitor (Twitter) written in Django and Django Rest Made in group
***




##### preparing the environment to run the project locally


1. If virtualenv has not installed install using:
 ```
sudo pip install -U pip setuptools virtualenv
 ```
2. Creating virtualenv:
 ```
virtualenv <venvs_path>/monitwi/ -p python2.7
 ```
 
 - *venvs_path* - This is the directory where all your virtual environments have been, for example: / opt / venvs /
 
 
3. Clone the repository:
 ```
 git clone https://github.com/henriquemsouza/Twitter-monitor.git
 ```
 
 4. Activate your virtualenv with the command:
 ```
 source <venvs_path/monitwi/bin/activate
 ```
 5. Inside the <projects_path> / Twitter-monitor / folder, install all dependencies:
 ```
 pip install -U pip && pip install -r requirements.txt
 ```
## create postgres database
 
 ```
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
sudo su - postgres

createdb mydb
createuser -P myuser
pass 12345678

acess
psql mydb

The following command defines access rights for the new user.
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

\q
 ```


***
***
## how to run the project on windows
*** 
1. download PgAdmin 3 or PgAdmin 4:
##### create a postgres database with the following information

```
db name mydb
user name myuser
password 12345678
 ```
#### If you do not know how to configure pgadmin follow the tutorial of the link below 
 [Tutorial](https://confluence.atlassian.com/display/CONF30/Database+Setup+for+PostgreSQL+on+Windows#app-switcher)

2. Creating virtualenv:
 ```
Open the CMD in the desired folder
mkdir virtualenv
c:\Python27\Scripts\virtualenv.exe virtualenv\monitwi
virtualenv\ENVvir\monitwi\activate
 ```
 
3. Inside the project folder, install all dependencies:
 ```
pip install -r requirements.txt
 ```
 
 4. Run the commands below:
 ```
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
python manage.py runserver
 ```


