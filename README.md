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
You can install the required dependencies via
```
pip install -r requirements.txt
```

## Deploying
This code can be deployed as a CRON job in any environment or simply run once. For running via CRON, first define your CRON file and initialize it (CentOs7 example) via
```
systemctl start crond
```
If you would like to run this script once then simply run `python run.py`

Note: You will still need to define all necessary environment variables. This can be done in the CRON file or elsewhere in your environment.

## Testing
In order to run the tests you must first install the required dependencies via
```
pip install -r test_requirements.txt
```

After this you may run the tests via
```
nosetests tests/ --cover-package=categorizer/
```
Optionally, you may provide the flag `--with-coverage` to `nosetests` to determine the test coverage of this project.


## Running Locally
If you would like to run Categorizer locally, you will need to specify the following environment variables.
1. `sysenv` (dev, prod)
2. `DEVIRISPWD` (Used to connect to the Dev IRIS instance)
3. `IRISPWD` (Used to connect to the Prod IRIS instance)

The project can then be run locally by running `python run.py`
