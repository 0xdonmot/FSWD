# Backend - Full Stack Trivia API


### Installing Dependencies for the Backend

1. **Python version**
This project works with python 3.7

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
With Postgres running, restore a database using the trivia.psql file. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

To run the server, execute:

```bash
flask run --reload
```

## API Endpoints
```


Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}

GET '/questions'
- Fetches a list of questions in which each element has question information in the form of key: value pairs.
- Request Arguments: None
- Returns: An list of question objects and other relevant information. 
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 20
}

DELETE '/questions/<int:question_id>'
- Deletes a question from the database with the given question id
- Request Arguments: question id
- Returns: An object with a single key, deleted, that lists the question id deleted. 
{
    'deleted' : 4
}

POST '/questions'
- Creates a new question and saves this to the database
- Request Arguments: question, answer, category, difficulty
- Returns: The newly created question object 
{
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
}

POST '/questions/search'
- Fetches questions based on a case insensitive search
- Request Arguments: search term
- Returns: A list of question objects which contain the search term
[
    {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
    }
]

GET '/categories/<int:category_id>/questions'
- Fetches all questions within a specified category
- Request Arguments: 
- Returns: A list of question objects which match the given category id 
[
    {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
    }
]

POST '/quizzes'
- Fetches a random question for a specified category as long as the question has not been asked previously
- Request Arguments: quiz category, previous questions
- Returns: A single question object within the specified category
{
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
