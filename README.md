# Simple Hotel Reservations

## REAL SIMPLE START -- REMEMBER TO KILL db.sqlite -- then 'migrate', then 'createsuperuse' -- start the site, go to the /admin site - add entities.

# Environment setup
## Step 1 -- Clone the repo

Use one or the other.

### Using SSH
```
# using ssh:
git@github.com:cicorias/njit-dbms-final.git
```

### Using http:
```
https://github.com/cicorias/njit-dbms-final.git

```

## Step 2 -- Setup a Python virtual env.

Move into the cloned path --- `njit-dbms-final`

Then, ensure you have Python 3.7+  -- `python -V`

Create a virtual environment.

```
python -m venv .venv
```

Activate that enviornment

### Under bash/Linux/Wsl

```
source .venv/bin/activate
```

### Under Windows PowerShell
```
.\.venv\Scripts\Activate.ps1
```

### Windows CMD
```
./.venv/Scripts/Activate.bat
```


## Step 3 -- Install Dependencies

>Note: You MUST do this after activating the environemnt.

You should see a virtual environment indicator in the command prompt like below:

```
(.venv) E:\g\njit\njit-dbms-final>
```


### Pip install

```
pip install -r requirements.txt
```

## Step 4 -- Verify Django is working

At this point, you have a isolated virtual env with the Django packages install and should be ready to run.

Navigate do the folder `./hotelapp` - in that folder you should see a file `manage.py` - this is Django's main administration tool -- see in the offical docs [django-admin and manage.py](https://docs.djangoproject.com/en/3.1/ref/django-admin/)


From the `./hotelapp/` path, where you just cloned you can run:

```
python manage.py
```
You should get output that lists all the commands - 

>NOTE: if you see something like the following ensure 1. you've setup your virtual environment AND 2. you've activated it.

```
❯ ./manage.py
Traceback (most recent call last):
  File "./manage.py", line 11, in main
    from django.core.management import execute_from_command_line
ModuleNotFoundError: No module named 'django'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "./manage.py", line 22, in <module>
    main()
  File "./manage.py", line 17, in main
    ) from exc
ImportError: Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?
```

## Step 5 -- run migrations

Migrations are core to Django's Object Relational Mapping (ORM). Django can completly manage the schema for a SQL database via models and migrations.  And through the lifecycle of the application as schema changes are needed, as reflected in [models](https://docs.djangoproject.com/en/3.1/topics/db/models/).

For now, the project has a single migration for the Custom User..

### Run migrations admin command

```
# from the ./hotelapp directory
python manage.py migrate
```

At this point any Django models are created in the local sqlite3 database or the database the configuration is running against.  

## STEP 6 - Create super user

This steup MUST be done after `migrate` as we are using custom user objects/schema.

```
# from the ./hotelapp directory
python manage.py createsuperuser
```

You will be prompted for a username which should be in email address format -- and a password. 

At this point, you can start the server with

```
# from the ./hotelapp directory
python manage.py runserver
```

Open your browser and navigate to `http://localhost:8000/admin`



# Functional Requirements.
## Developer next steps
### Here want to dynamically choose either sqlite or postgres
This should use env variables.

1. setup to use either sqlite or postgres


### PostGres setup
