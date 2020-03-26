# Baackup
That's right, with double a. It's a backup tool written in Django framework to automate the procedure of collecting all the necessary files and folders from local or remote (ssh) machines.  

## Installation
```bash
sudo git clone https://github.com/bkbilly/Baackup.git /opt/Baackup
cd /opt/Baackup
sudo pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
