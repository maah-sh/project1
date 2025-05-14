

### Create a Python virtual environment, this step is optional, but recommended
```
pip install virtualenv
virtualenv env
source ./env/bin/activate
```

### Install the dependencies
```
pip install -r ../requirements.txt
```

### Run database migrations
```
python manage.py migrate
```

### Create a superuser
```
python manage.py createsuperuser
```

### Run the server
```
python manage.py runserver
```