# Motivation for the Casting Agency Project
The Casting Agency is a thriving business for creating movies and managing and assigning actors to those movies. We are within the company and are creating a system to simplify and streamline this process.


Follow instructions to install the latest version of python for platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

## Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organized. Instructions for setting up a virtual environment for platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## PIP Dependencies

Once we have virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the casting_backup.psql file provided. From the backend folder in terminal run:
```bash
psql casting < casting_backup.psql
```

## Running the server

From within the `starter` directory first ensure we are working using our created virtual environment.

To run the server, execute:

1st setup the env
source setup.sh

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use `app.py` file to find the application. 


# General :
1. This app can be accessed as https://casting-agency-capfsnd.herokuapp.com
2. This app can be run locally on http://127.0.0.1:5000
3. Authentication is required on this app

# Important tips to use/retrive access tokens
1. Access token which will remain valid for couple of hours, from the submission of this project, are provided in setup.sh.
2. These access tokens must be used in curl/postman requests to access end points. 
3. Fresh access tokens can also be generated through further steps.
4. Use https://casting-agency-capfsnd.herokuapp.com/authorization/url to receive a URL
5. Use the URL in response for below users
    a)User: ca_mac2957@gmail.com Password: mac_2957 Role: Casting Assistant
    b)User: cd_mac2957@gmail.com Password: mac_2957 Role: Casting Director
    c)User: ep_mac2957@gmail.com Password: mac_2957 Role: Executive Producer
6. Access Token received in redirected URL for all three roles should be copied and used to access API endpoints.
7. To deduce, which role can access which end points, please go through below details of roles, permissions and end points.
8. Access Tokens can also be replaced in setup.sh, so that they can be used to run the test suite, detailed towards the end of this file.


## Role based access for the Casting Agency Project

All the application end points support RBAC except default and /authorization/url

## Roles:
    # Casting Assistant : 
                        Can view actors and movies
                        permissions:
                                    view:actor
                                    view:movie
    # Casting Director : 
                        All permissions a Casting Assistant has
                        Add or delete an actor from the database
                        Modify actors or movies
                        permissions:
                                    view:actor
                                    view:movie
                                    create:actor
                                    delete:actor
                                    modify:actor
                                    modify:movie

    # Executive Producer :
                            All permissions a Casting Director has
                            Add or delete a movie from the database
                            permission:
                                    view:actor
                                    view:movie
                                    create:actor
                                    delete:actor
                                    modify:actor
                                    modify:movie
                                    create:movie
                                    delete:movie




## Error handlers :
Followwing error responses can be recived to users of API
    400: bad request
    404: resource not found
    405: method not allowed
    422: unprocessable
    500: internal server error

GET '/'
- Used for health check, as to verify whether application is running
- doesn't require any permission
- Request Arguments: None
- Returns: A string "Hello"
- example: curl -X GET  https://casting-agency-capfsnd.herokuapp.com/

GET '/authorization/url'
- This is a helper method to provide custom url to login for users and generate reusable token
- doesn't require any permission
- Request Arguments: None
- Returns: an object with key url and it's value
- example: curl -X GET  https://casting-agency-capfsnd.herokuapp.com/authorization/url

GET '/actors'
- Fetches a list of actors
- can be invoked with view:actor permission
- Request Arguments: None
- Returns: An object with keys, 
    1. actors, a list of actors, where each actor object has below keys and values
        int:id: id of the Actor.
        str:name: name of Actor
    2. int:total_actors: an integer that contains number of actors        
 - example: curl -X GET  https://casting-agency-capfsnd.herokuapp.com/actors -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
{
  "actors": [
    {
      "id": 1,
      "name": "Amitabh Bachchan"
    },
    {
      "id": 2,
      "name": "Shahrukh Khan"   
    },
    {
      "id": 3,
      "name": "Tom Cruise"
    },
    {
      "id": 4,
      "name": "Pat cummins"
    }
  ],
  "success": "True",
  "total_actors": 4
}

GET '/actors/<int:actor_id>'
- Fetches details of actor with the specified id in the URL
- can be invoked with view:actor permission
- Request Arguments: None
- Returns: An object representing the actor with the keys
    int:id: id of the Actor.
    str:name: name of Actor.
    str:nationality: nationality of the Actor.
    date:date_of_birth: date of birth of the Actor.
    int:no_of_movies: no of movies, this Actor has been part of,
    movies: list of movies this actor has been part of where each movie object has below keys
        int:id: id of the movie.
        str:name: name of movie.
        str:year: year, in which this movie was released.

 - example: curl -X GET  https://casting-agency-capfsnd.herokuapp.com/actors/2 -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
{
  "actor": {
    "date_of_birth": "Tue, 12 Oct 1965 00:00:00 GMT",
    "id": 2,
    "movies": [
      {
        "id": 1,
        "name": "Mohabbatein",
        "year": 2001
      }
    ],
    "name": "Shahrukh Khan",
    "nationality": "Indian",
    "no_of_movies": [
      1
    ]
  },
  "success": "True"
}


DELETE '/actors/<int:actor_id>'
- deletes the actor with the specified id in the URL
- can be invoked with delete:actor permission
- Request Arguments: None
- Returns: An object deleted_actor which has below keys and values
    int:id: id of the actor.
    str:name: name of the actor.
 - example: curl -X DELETE  https://casting-agency-capfsnd.herokuapp.com/actors/2 -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
{
  "deleted_actor": {
    "id": 2,
    "name": "Shahrukh Khan"
  },
  "success": "True"
}

POST '/actors'
- Creates a new actor with the passed parameters
- can be invoked with create:actor permission
- Request Arguments: Json Object with key value pairs as below, where name is mandatory and other key
    value pairs are optional
    str:name: name of Actor.
    str:nationality: nationality of the Actor.
    date:date_of_birth: date of birth of the Actor.
    movies: list of movie ids this actor has been part of, all these movies should be pre-exising within application
- Returns: An object created actor which has below keys and values
    int:id: id of the actor.
    str:name: name of the actor.
 - example: curl -X POST https://casting-agency-capfsnd.herokuapp.com/actors -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d '{"name": "Pat cummins",   "nationality": "British","date_of_birth": "29-jun-1958"}'
{
  "created_actor": {
    "id": 5,
    "name": "Pat cummins"
  },
  "success": "True"
}

PATCH '/actors/<int:actor_id>'
- updates the actor with the specified id in the URL with passed parameters
- can be invoked with modify:actor permission
- Request Arguments: Json Object with below optional key value pairs
    str:name: name of Actor.
    str:nationality: nationality of the Actor.
    date:date_of_birth: date of birth of the Actor.
    int:no_of_movies: no of movies, this Actor has been part of,
    movies: list of movie ids this actor has been part of, all these movies should be pre-existing within application
- Returns: An object updated_actor which has below keys and values 
    int:id: id of the actor.
    str:name: name of the actor.
 - example: curl -X PATCH https://casting-agency-capfsnd.herokuapp.com/actors/5 -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d '{"name": "Pat cummins Sr","nationality": "British"}'
{
  "success": "True",        
  "updated_actor": {        
    "id": 5,
    "name": "Pat cummins Sr"
  }
}
  
GET '/movies'
- Fetches a list of movies
- can be invoked with view:movie permission
- Request Arguments: None
- Returns: An object with keys, 
    1. movies, a list of movies, where each movie object has below keys and values
        int:id: id of the movie.
        str:name: name of movie
    2. int:total_movies: an integer that contains number of movies        
 - example: curl -X GET  https://casting-agency-capfsnd.herokuapp.com/movies -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
{
  "movies": [
    {
      "id": 1,
      "name": "Mohabbatein",
      "year": 2001
    },
    {
      "id": 2,
      "name": "Judgement Day",
      "year": 1995
    }
  ],
  "success": "True",
  "total_movies": 2
}

GET '/movies/<int:movie_id>'
- Fetches details of movie with the specified id in the URL
- can be invoked with view:movie permission
- Request Arguments: None
- Returns: An object representing the movie with the keys
    int:id: id of the movie.
    str:name: name of the movie
    str:genre: genre of the movie
    str:language: language of the movie
    int:year: release year of the movie
    float:imdb_rating: imdb rating of the movie
    int:no_of_actors: number of actors in the movie
    actors: list of actors, who have acted in the movie where each actor object has below keys
        int:id: id of the actor.
        str:name: name of actor.
 - curl -X GET  https://casting-agency-capfsnd.herokuapp.com/movies/1 -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
{
  "movie": {
    "actors": [
      {
        "id": 1,
        "name": "Amitabh Bachchan"
      }
    ],
    "genre": "Romance",
    "id": 1,
    "imdb_rating": 7.6,
    "language": "Hindi",
    "name": "Mohabbatein",
    "no_of_actors": [
      1
    ],
    "year": 2001
  },
  "success": "True"
}

DELETE '/movies/<int:actor_id>'
- deletes the movie with the specified id in the URL
- can be invoked with delete:movie permission
- Request Arguments: None
- Returns: An object deleted_movie which has below keys and values
    int:id: id of the movie.
    str:name: name of the movie.
    int:year: year in which this movie was released
 - example: curl -X DELETE  https://casting-agency-capfsnd.herokuapp.com/movies/1 -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
{
  "deleted_movie": {
    "id": 1,
    "name": "Mohabbatein",
    "year": 2001
  },
  "success": "True"
}

POST '/movies'
- Creates a new movie with the passed parameters
- can be invoked with create:movie permission
- Request Arguments: Json Object with key value pairs as below, where name is mandatory and other key
    value pairs are optional
    int:id: id of the movie.
    str:name: name of the movie
    str:genre: genre of the movie
    str:language: language of the movie
    int:year: release year of the movie
    float:imdb_rating: imdb rating of the movie
    actors: list of ids of actors, who have acted in the movie 
- Returns: An object created_movie which has below keys and values
    int:id: id of the movie.
    str:name: name of the movie
    int:year: release year of the movie
 - example: curl -X POST https://casting-agency-capfsnd.herokuapp.com/movies -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d '{"name": "Yet To Be Announced","genre": "Western","language": "French","year": "2022","imdb_rating": "0","actors":[1] }'
{
  "created_movie": {
    "id": 4,
    "name": "Yet To Be Announced",
    "year": 2022
  },
  "success": "True"
}

PATCH '/movies/<int:movie_id>'
- updates the movie with the specified id in the URL with passed parameters
- can be invoked with modify:movie permission
- Request Arguments: Json Object with below optional key value pairs
    int:id: id of the movie.
    str:name: name of the movie
    str:genre: genre of the movie
    str:language: language of the movie
    int:year: release year of the movie
    float:imdb_rating: imdb rating of the movie
    actors: list of ids of actors, who have acted in the movie, all these actors should be pre-existing
- Returns: An object updated_movie which has below keys and values 
    int:id: id of the movie.
    str:name: name of the movie.
    int:year: release year of the movie.
 - example: curl -X PATCH  https://casting-agency-capfsnd.herokuapp.com/movies/4 -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d '{"name": "the unknown" }'
{
  "success": "True",
  "updated_movie": {
    "id": 4,
    "name": "the unknown",
    "year": 2022
  }
}

## Testing

To run the tests, run

1. source setup.sh
2. dropdb casting_test
3. createdb casting_test
4. psql casting_test < casting_backup.psql
5. python test_app.py