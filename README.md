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

 comando a seguir define direito de acesso ao novo usuário.
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

\q
 ```