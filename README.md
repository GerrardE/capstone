# Capstone Backend

## Motivation
Capstone is a project that models a company that is responsible for creating movies, managing and assigning actors to those movies. I am an Executive Producer within the company and I am creating a system to simplify and streamline my process.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Database Setup

Create a database `capstone` and `capstone_test` for development and test respectively.
With Postgres running, restore a database for both using the capstone.psql file provided. From the root folder in terminal run:

```bash
psql capstone < capstone.psql
```

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

Run tests with the `python app_test.py` command

You can also test the endpoints with [Postman](https://getpostman.com) by importing the postman collection `capstone.postman_collection.json`. Each folder in the collection represents the various roles. Some variables have been defined for the collection like so;

- `{{url}}` variable is the localhost url
- `{{remote}}` variable is the link to the live application at [capstone-app-backend](https://capstone-app-backend.herokuapp.com/api)

## Resources
- Documentation can be found [here](https://documenter.getpostman.com/view/7418457/SzKQwzQQ)
- Generate access tokens using this [url](https://capstone-app.auth0.com/authorize?audience=auth&response_type=token&client_id=tqFImTSXfAfSu1mNq9kqnUuhGrHKs1lr&redirect_uri=http://localhost:8000/home) and the account details provided below

- There are 3 accounts set up already for each personnel;

```bash
assistant@gmail.com
director@gmail.com
producer@gmail.com
```

```bash
use 'capstone_2020' as password for all accounts
```
