# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
General :
1. This app is hosted locally  with base url as http://127.0.0.1:5000/
2. No authentication required on this app

Error handlers : Followwing error responses can be recived to users of API
    400: bad request
    404: resource not found
    405: method not allowed
    422: unprocessable
    500: internal server error

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with keys, 
    1. categories, a dictionary that contains key value pair, as category id vs category type
    2. int:total_categories: an integer that contains number of categories        
 - example: curl http://127.0.0.1:5000/categories -H "Content-Type: application/json"
{
  "categories": {
    "0": "Science",
    "1": "Art",
    "2": "Geography",
    "3": "History",
    "4": "Entertainment",
    "5": "Sports"
  },
  "success": "True",
  "total_categories": 6
}

GET '/questions'
- Fetches a dictionary of paginated questions
- Request Arguments: Optionally we can provide page number, defaut value of page number is 1
- Returns: An object with keys
    1. categories: a list that contains category objects
        -int:id: Category id.
        -str:type: Category text.
    2. questions: a list of question on the page, where each question object has below keys and values
        int:id: id of the question.
        str:question: question text.
        str:answer: answer test.
        int:difficulty: difficulty level.
        int:category: id of qusestion's category
    3. int:total_questions : number of total questions
 - example: curl http://127.0.0.1:5000/questions?page=2 -H "Content-Type: application/json"
{
  "categories": [
    {
      "id": 0,
      "type": "Science"
    },
    {
      "id": 1,
      "type": "Art"
    },
    {
      "id": 2,
      "type": "Geography"
    },
    {
      "id": 3,
      "type": "History"
    },
    {
      "id": 4,
      "type": "Entertainment"
    },
    {
      "id": 5,
      "type": "Sports"
    }
  ],
  "current_category": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 3,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 3,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "I am beboo bachcha my lord",
      "category": 3,
      "difficulty": 1,
      "id": 24,
      "question": "What was the answer of beboo bachha"
    },
    {
      "answer": "Apollo 13",
      "category": 4,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 4,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Uruguay",
      "category": 5,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "UP",
      "category": 2,
      "difficulty": 5,
      "id": 26,
      "question": "Nabinagar is in which state"
    }
  ],
  "success": "True",
  "total_questions": 17
}


DELETE '/questions/<int:question_id>'
- deletes the question with the specified id in the URL
- Request Arguments: None
- Returns: An object with keys
    1. question: object of deleted question which has below keys and values
        int:id: id of the question.
        str:question: question text.
        str:answer: answer test.
        int:difficulty: difficulty level.
        int:category: id of qusestion's category
 - example: curl -X DELETE http://127.0.0.1:5000/questions/9 -H "Content-Type: application/json"
{
  "question": {
    "answer": "Muhammad Ali",
    "category": 3,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  "success": "True"
}


GET '/categories/<int:category_id>/questions'
- Gets a dictionary of questions, belonging to the specified category specified in URL parameter 
- Request Arguments: None
- Returns: dictionary that contains keys
    1. string:current_category : name of the category supplied in request
    2. questions: a list that contains questions objects, each having below key:value pairs.
        int:id: id of the question.
        str:question: question text.
        str:answer: answer test.
        int:difficulty: difficulty level.
        int:category: id of qusestion's category
    3. int:total_questions : number of total questions belonging to category supplied in request
 - example: curl -X GET http://127.0.0.1:5000/categories/4/questions -H "Content-Type: application/json" 
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 4,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 4,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": "True",
  "total_questions": 2
}


Post '/questions/search'
- Searches for a question based on a string passed through request argument 
- Request Arguments: Json Object
    -str:searchTerm: string based on which questions will searched
- Returns: dictionary that contains keys
    1. questions: a list that contains questions which match to search, where each question has below key value pairs
        int:id: id of the question.
        str:question: question text.
        str:answer: answer test.
        int:difficulty: difficulty level.
        int:category: id of qusestion's category
    2. int:total_questions : number of total questions which match to the search
 - example: curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "Taj"}'
{
  "questions": [
    {
      "answer": "Agra",
      "category": 2,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": "True",
  "total_questions": 1
}


Post '/quizzes'
- Returns a random question, belonging to the supplied category id and other than having ids specified in request 
- Request Arguments: Json Object cotaining below
    1. previous_questions: list of previous question from the category
    2. quiz_category: a dictionary that contains
        -int:id: category id.
        -str:type: type of category.
- Returns: dictionary that contains key
    1. question: a question object
        int:id: id of the question.
        str:question: question text.
        str:answer: answer test.
        int:difficulty: difficulty level.
        int:category: id of qusestion's category
 - example: curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [14],
                "quiz_category": {"type": "Geography", "id": '3'}}'
{
  "question": {
    "answer": "Maya Angelou",
    "category": 3,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": "True"



```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```