# PAPYBOT

Ask PapyBot where a place is located (in French!), then he will answer you and give you more information.
For instance: Qu'elle est l'adresse d'OpenClassrooms, s'il te plaît ?

## Prerequisites

- Python 3.9.10
- Create an account at https://developer.here.com/ to get your credentials to use the geolocation API.
- At the root of the project, create a env.py file and fill it with your "here.com" credentials

env.py:
**Don't forget the quotation marks around each identifier.**
```python
app_id = "<your app id>"
api_key = "<your api key>"
```
## Installing pipenv the virtual environment via Pipx

Pipx is a tool to help you install and run end-user applications written in Python. 
It installs applications into an isolated and clean environment on their own.
Once you have pipx ready on your system, continue to install Pipenv. 
(https://pipenv.pypa.io/en/latest/install/)

```shell
pip install --user pipx
pipx install pipenv
```


## Activating the virtual environment

```shell
pipenv shell
```


## Installing the dependences

```shell
pipenv install -r requirements.txt
```


## Execute the application

```shell
flask run
```


## With your browser

Go to `http://127.0.0.1:5000/` and ask PapyBot your question to know where a place is located. :)

## Testing

### Installing pytest

I used pytest
```bash
pipenv install pytest
```


### Running test

```bash
python -m pytest -vvs tests/
```
**-v** => See all the tests (passed and failed)
**-v** => See the full problem (not only a part)
**-s** => Show all what is in the "print()" instruction

## Test coverage

### Installing coverage

I used pytest-cov
```bash
pipenv install pytest-cov
```

### Configuring files for the coverage to bypass

I created a file named **.coveragerc** at the root of the project.
This file contains the files and directories to bypass and more.


## Running coverage

### Displaying the result in the shell

```bash
python -m pytest --cov=.
```

### Display the result, which contains many details, in an html file

```bash
python -m pytest --cov=. --cov-report=html
```

The result is in the root of the project, in a folder named **htmlcov**.
The file to run is **index.html**
