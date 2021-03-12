## about Travelller

Traveller is a trip organizer by it you can schedule your future trips.
By using Traveller you can add, delete, edit your current trips and also get
trips for certain period of time.

## Getting Started

- Base URL : The app is hosted [Here](https://flask-travel-planner.herokuapp.com/) on Heroku.

- Authentication : This version of the app require authentication and you can register your account from [Here](https://flask-travel-planner.herokuapp.com/register)

- Authorization : The app has three main roles

  - Regular user: can CRUD only his own account and trips.
  - Manager : can CRUD all the users and only his own trips.
  - Admin: can CRUD on all users and trips.

### Installing Dependencies To use the app locally

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database

App uses Sqlite database.

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=travel_planner
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `travel_planner` directs flask to use the `travel_planner` directory and the `__init__.py` file to find the application.
