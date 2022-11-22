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

### Running the server

To run the server, execute:

```bash
source setup.sh
python app.py
```

## Heroku Hosting

The app is currently hosted at Heroku [here](https://casting-agency-capstone-48172.herokuapp.com/).
It will be removed after 28th November 2022.

However, to access the endpoints, you will need to send authentication headers with your requests.
An example of how to do this using curl:
```
curl https://casting-agency-capstone-48172.herokuapp.com/movies -H "Authorization: Bearer <insert_jwt_token>"
```
## API Endpoints
```


Endpoints
GET '/actors'
GET '/movies'
DELETE '/actors/<int:actor_id>'
DELETE '/movies/<int:movie_id>'
POST '/actors'
POST '/movies'
PATCH '/actors/<int:actor_id>'
PATCH '/movies/<int:movie_id>'

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


## Testing
To run the tests, run
```
createdb casting_agency_test
python test_app.py
```

There are additional Postman tests which can be found [here](casting_agency.postman_collection.json).
The host value could be a local host (e.g. localhost:5000) or the heroku host.