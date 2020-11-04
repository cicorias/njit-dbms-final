# Simple Hotel Reservations

# Environment setup
## Clone the repo

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

## Setup a Python virtual env.

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


## Install Dependencies

>Note: You MUST do this after activating the environemnt.

You should see a virtual environment indicator in the command prompt like below:

```
(.venv) E:\g\njit\njit-dbms-final>
```


### Pip install

```
pip install -r requirements.txt
```




# Functional Requirements.
## Developer next steps
### Here want to dynamically choose either sqlite or postgres
This should use env variables.

1. setup to use either sqlite or postgres


### PostGres setup
