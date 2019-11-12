# Categorizer

Categorizer aids in the sorting and closing of various abuse types in IRIS. It is currently capable of sorting the following types from the DS-Abuse box in IRIS
1. Phishing
2. Malware
3. Network Abuse
4. Spam
5. Law Enforcement Officers (LEOs)


## Cloning
To clone the repository via SSH perform the following
```
git clone git@github.secureserver.net:digital-crimes/categorizer.git
```
It is recommended that you clone this project into a pyvirtualenv or equivalent virtual enviornment.

## Installing Dependencies
### Ubuntu Based System Dependencies
For connecting to the IRIS DB locally with a Ubuntu based development system, you will need to ensure that you have the ODBC Driver Manager packages installed and FreeTDS driver settings specified.
```
sudo apt-get install unixodbc-dev unixodbc-bin unixodbc
```

Edit your odbcinst.ini file. 
```
sudo vim /etc/odbcinst.ini
```
Add the following info for the FreeTDS Driver and save the file.
```
[FreeTDS]
Description = TDS driver (Sybase/MS SQL)
# Some installations may differ in the paths
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
CPTimeout =
CPReuse =
FileUsage = 1
TDS Version = 8.0
```

### Project Dependencies
To install all dependencies for development and testing simply run `make`.

## Building
Building a local Docker image for the respective development environments can be achieved by

```
make [dev, prod]
```

## Deploying
Deploying the Docker image to Kubernetes can be achieved via

```
make [dev, prod]-deploy
```

You must also ensure you have the proper push permissions to Artifactory or you may experience a `Forbidden` message.

## Testing
```
make test     # runs all unit tests
make testcov  # runs tests with coverage
```

## Style and Standards

All deploys must pass Flake8 linting and all unit tests which are baked into the [Makefile](Makefile).

There are a few commands that might be useful to ensure consistent Python style:
```
make flake8  # Runs the Flake8 linter
make isort   # Sorts all imports
make tools   # Runs both Flake8 and isort
```


## Running Locally
If you would like to run Categorizer locally, you will need to specify the following environment variables.
1. `sysenv` (dev, prod)
2. `IRIS_USERNAME` (Used to connect to the IRIS database)
3. `IRIS_PASSWORD` (Used to connect to the IRIS database)

The project can then be run locally by running `python run.py`
