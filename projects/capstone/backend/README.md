# Backend - Casting Agency API


### Installing Dependencies for the Backend

1. **Python version**
This project works with python 3.10

2. **Dependencies** 
Requirements can be installed through:
```bash
pip install -r requirements.txt
```

3. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)

 - [SQLAlchemy](https://www.sqlalchemy.org/) 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)

### Database Setup
With Postgres running, create a database by running the following command:
```bash
createdb casting_agency
```

Note, the database url is setup for Heroku. The database url path will need to be configured if the app is to be used locally.

### Running the server

To run the server, create a local database and update the database url path in setup.sh

Then, execute:

```bash
source setup.sh
python app.py
```

### Roles

There are three roles defined, with varying levels of access:

- Casting Assistant.
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and..
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All Casting Director permissions and..
    - Add or delete a movie from the database

### Data Model

[_models.py_](models.py)

There are two tables created in the database:
- Actor
    - This is used to store data on actors.
    - It contains information on their name, age and gender
- Movie
    - This is used to store data on movies.
    - It contains information on the movie name and release date.
Each table has insert, update, delete and format helper functions.

### Local / Heroku Hosting

The app is currently hosted at Heroku [here](https://casting-agency-capstone-48172.herokuapp.com/).
It will be removed after 28th November 2022.

#### Hosting Steps

To host the app, please follow the below steps:
- Create a Heroku account [here](https://signup.heroku.com/) and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
```
# Install, if Heroku as Standalone
curl https://cli-assets.heroku.com/install.sh | sh
# Or, use Homebrew on Mac
brew tap heroku/brew && brew install heroku
# Verify the installation
heroku --version
# Verify the download
which heroku
```
- Create an API key on Heroku and use it to login via the CLI. Enter your API key when asked for your password.
```
heroku login -i
```
- Ensure Git is installed locally.
- Install Postgres
```
# Mac/Linux
# Install Postgres using Brew. Reference: https://wiki.postgresql.org/wiki/Homebrew 
brew install postgresql
# Verify the installation
postgres --version
pg_ctl -D /usr/local/var/postgres start
pg_ctl -D /usr/local/var/postgres stop
```
- Verify the database
```
# Open psql prompt
psql [username]
# View the available roles
\du
# View databases
\list
```
- Clone this directory
```
# Create a project directory
mkdir casting_agency_sample
# Clone the FSND repo
git clone https://github.com/0xdonmot/FSWD.git
# Copy the casting agency app to the new directory
cp FSND/projects/capstone/ casting_agency_sample/
```
- Create a python virtual environment, to isolate the required project dependencies and python runtime environment.
```
cd casting_agency_sample
# Create a Virtual environment
python3 -m venv myvenv 
source myvenv/bin/activate
```
- Set up the environment variables
```
# You should have setup.sh and requirements.txt available
chmod +x setup.sh
source setup.sh
# The setup.sh will create various environment variables including
# DATABASE_URL, API_AUDIENCE, ALGORITHMS, AUTH0_DOMAIN, casting_assistant_auth,
# casting_director_auth, executive_producer_auth
# Change the DATABASE_URL, as applicable to you.
```
- Install the python dependences
```
pip install -r requirements.txt
python app.py
```
- You should now be able to view and send calls at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

#### Heroku Deployment

- Create and save the app's environment variables in Heroku via _Heroku dashboard >> Particular App >> Settings >> Reveal Config Vars_.
- Initialise Git
```
# Run it just once, in the beginning
git init
# For the first time commit, you need to configure the git username and email:
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
- Create an App in the Heroku Cloud
```
heroku create [my-app-name] --buildpack heroku/python
# For example, 
# heroku create myapp-663697908 --buildpack heroku/python
# https://myapp-663697908.herokuapp.com/ | https://git.heroku.com/myapp-663697908.git
```
- Add PostgreSQL addon for the database
```
heroku addons:create heroku-postgresql:hobby-dev --app [my-app-name]
```
- Configure the App
```
heroku config --app [my-app-name]
# DATABASE_URL:
# postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1
```
- Copy the DATABASE_URL from the above step and update the local variable.
```
export DATABASE_URL="postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1"
# Verify
echo $DATABASE_URL
# postgres://xjlhouchsdbnuw:0e9a708916e496be7136d0eda4c546253f1f5425ec041fd6e3efda3a1f819ba2@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d3mrjpmsi4vvn1
```
- Update the DATABASE_URL variable in the Heroku Cloud.
- Push the app
```
# Check which files are ready to be committed
git add -A
git status
git commit -m "your message"
git push heroku master
```
- Open the app at the deployed app url!
- Errors in the accessing the app can be debugged from the command line, using the following command.
```
heroku logs
```


[Getting Started with Python and Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
[Deployment Docs](https://devcenter.heroku.com/categories/deployment)
[FSND repo](https://github.com/0xdonmot/FSWD)


#### Heroku API Calls

To access the API endpoints, you will need to send authentication headers with your requests.
An example of how to do this using curl:
```
curl https://casting-agency-capstone-48172.herokuapp.com/movies -H "Authorization: Bearer <insert_jwt_token>"
```
### API Endpoints
__Endpoints__
- GET '/actors'
- GET '/movies'
- DELETE '/actors/<int:actor_id>'
- DELETE '/movies/<int:movie_id>'
- POST '/actors'
- POST '/movies'
- PATCH '/actors/<int:actor_id>'
- PATCH '/movies/<int:movie_id>'

```
GET '/actors'
- Fetches a list of actors, which contains information on the actors in the form of key: value pairs.
- Request Arguments: None
- Returns: A list of actor objects
{
    "actors": [
        {
            "age": 39,
            "gender": "Male",
            "id": 1,
            "name": "John Wayne"
        }
    ],
    "success": true
}

GET '/movies'
- Fetches a list of movies, which contains information on the movies in the form of key: value pairs.
- Request Arguments: None
- Returns: A list of movie objects
{
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 16 Jun 2005 00:00:00 GMT",
            "title": "Batman Begins"
        }
    ],
    "success": true
}

DELETE '/actors/<int:actor_id>'
- Deletes an actor from the database with the given actor id
- Request Arguments: actor id
- Returns: An object that lists the actor id deleted. 
{
    "deleted_actor_id": 1,
    "success": true
}

DELETE '/movies/<int:movie_id>'
- Deletes an movie from the database with the given movie id
- Request Arguments: movie id
- Returns: An object that lists the movie id deleted. 
{
    "deleted_movie_id": 1,
    "success": true
}

POST '/actors'
- Creates a new actor and saves this to the database
- Request Arguments: name, age, gender
- Returns: The newly created actor object 
{
    "new_actor": {
        "age": 39,
        "gender": "Male",
        "id": 1,
        "name": "John Wayne"
    },
    "success": true
}

POST '/movies'
- Creates a new movie and saves this to the database
- Request Arguments: title, release date
- Returns: The newly created movie object 
{
    "new_movie": {
        "id": 1,
        "release_date": "Thu, 16 Jun 2005 00:00:00 GMT",
        "title": "Batman Begins"
    },
    "success": true
}

PATCH '/actors/<int:actor_id>'
- Edits an actor's details and saves this to the database
- Request Arguments: title, release date
- Returns: The edited actor object 
{
    "actor": {
        "age": 41,
        "gender": "Female",
        "id": 2,
        "name": "John Wayne"
    },
    "success": true
}

POST '/movies/<int:movie_id>'
- Edits a movie's details and saves this to the database
- Request Arguments: title, release date
- Returns: The edited movie object 
{
    "movie": {
        "id": 1,
        "release_date": "Thu, 16 Jun 2005 00:00:00 GMT",
        "title": "Batman Empieza"
    },
    "success": true
}


```


### Testing

#### Unit Tests
There are various unit tests in the directory. These test each API endpoint for successes and failures. Each request requires authorization. Therefore, these tests also test the role based access controls.

To run the tests, run
```
createdb casting_agency_test
python test_app.py
```
#### Postman Tests
There are additional Postman tests which can be found [here](casting_agency.postman_collection.json).

To run the tests, ensure you have Postman [installed](https://www.postman.com/downloads/), import the [testing file](casting_agency.postman_collection.json), ensure the host value is appropriate (e.g. localhost:5000). Right-click on the imported collection and click 'run collection'.

### AUTH0 Tokens
The API requires access tokens to access the data. The access tokens found in this directory will only work for 24 hours (until 24 November ~ 18:00). To request new access tokens, please use the below login details to login [here](https://dev-5kjn5d0mu43a1k3c.uk.auth0.com/authorize?audience=http://localhost:8080&response_type=token&client_id=cqTS6WHQJMrPFFMJBXeZijsagNISMzQJ&redirect_uri=http://127.0.0.1:8080). 

- Casting Assistant
    - email: casting_assistant@capstone.com
    - password: Castingagency!
- Casting Director
    - email: casting_director@capstone.com
    - password: Castingagency!
- Executive Producer
    - email: executive_producer@capstone.com
    - password: Castingagency!

The access token will be accessible in the url response.

To generate three separate tokens, you will need to make this request in separate Incognito browsers.