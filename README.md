# RA_for_T
Temporarly no description


<details>
  <summary> TEST ASSIGNMENT </summary>
  
  <h1>Exercise:</h1>

It is necessary to develop a REST API for task accounting.

Required: Python 3.x, FastAPI, PostgreSQL (using SQLAlchemy) and Docker Compose. You also need to implement autotests (pytest) and migrations (alembic).

<h1>API</h1>

You need to implement the following endpoints:
$${\color{green}POST }$$<pre> /tasks</pre>



Create a new task.

request body:
<pre>
{
     "title": "Prepare Report",
     "description": "Write last quarter sales report",
     status: new
}
</pre>
response body:
<pre>
{
     "id": 1,
     "title": "Prepare Report",
     "description": "Write last quarter sales report",
     "status": "new",
     "created_at": "2023-09-01T12:00:00"
}
  </pre>
$${\color{blue}GET}$$<pre> /tasks </pre>



Get a list of all tasks.

Query parameters:

limit: integer (optional, default=20)

response body:
<pre>
{
     "count": 2,
     "items": [
         {
             "id": 1,
             "title": "Prepare Report",
             "description": "Write last quarter sales report",
             "status": "new",
             "created_at": "2023-09-01T12:00:00"
         },
         {
             "id": 2,
             "title": "Update site",
             "description": "Add news and promotions to homepage",
             "status": "in_progress",
             "created_at": "2023-09-02T10:00:00"
         }
     ]
}
</pre>

$${\color{orange}PUT}$$ <pre> /tasks/{task_id} </pre>


Update task.

request body:

<pre>
{
     "title": "Prepare Report",
     "description": "Write last quarter sales report",
     "status": "done"
}
</pre>

response body:

<pre>
{
     "id": 1,
     "title": "Prepare Report",
     "description": "Write last quarter sales report",
     "status": "done",
     "created_at": "2023-09-01T12:00:00",
     "updated_at": "2023-09-03T09:00:00"
}
</pre>

$${\color{red}DELETE}$$ <pre> /tasks/{task_id}</pre>


Delete task.

response body:

<pre>
{
     "id": 1,
     "title": "Prepare Report",
     "description": "Write last quarter sales report",
     "status": "done",
     "created_at": "2023-09-01T12:00:00",
     "updated_at": "2023-09-03T09:00:00",
     "deleted_at": "2023-09-03T11:00:00"
}
</pre>

<h2>Deployment</h2>

The application needs to be containerized.

Write a Dockerfile that:

downloads a base Python image from Docker Hub
copies the application inside the image
installs the necessary packages and dependencies (PostgreSQL, requirements.txt, etc.)
configures all the necessary components for the application to work
starts the application on port 3000


<h1>Outcome</h1>

On a PC with Docker installed, it should be possible to clone the application source repository.

After running the docker build and docker-compose up commands, the application should respond to API calls at 127.0.0.1:3000. Migrations and autotests should run automatically.
</details>


# Getting started

## Requirement 

The only things you need is installed Docker and docker compose plugin.
Everything you can find in official site:


https://www.docker.com

## Description & Explanation

This application allows you to accept requests from clients. Clients can add, modify, and delete tasks, as well as display a list of all tasks.
Since in theory there can be more than one client, I decided to add additional functionality for registering clients and their further authentication
That choice explained by that the every client will recieved similar tasks.

<h3>&#9888; WARNING</h3>
<pre> For access to api you need register or login first</pre>


Every authenticated user get unique token, that has life duration 60 minutes. Token stored in cockies. Token type is <a href="https://jwt.io/introduction"> JWT</a>
After authentication API is available.

##

The API provides the following endpoints:

POST /tasks - create a new task.
GET /tasks - get a list of all tasks.
PUT /tasks/{task_id} - task update.
DELETE /tasks/{task_id} - delete a task.

To create a new task, send a POST request to /tasks with a request body in JSON format containing the title, description, and status of the task. If the task is successfully created, the response will return a JSON object with the task ID, title, description, status, and creation date.

To get a list of all tasks, send a GET request to /tasks with an optional limit parameter that specifies the maximum number of tasks that will be returned in the response. The response will contain a JSON object containing the number of tasks and a list of tasks with their IDs, titles, descriptions, statuses, and creation dates.

To update a task, send a PUT request to /tasks/{task_id} with the task ID in the request path and the request body in JSON format containing the new task title, description, and status values. The response will contain a JSON object with the issue ID, new title, description, status, creation date, and update date.

To delete a task, send a DELETE request to /tasks/{task_id} with the task ID in the request path. The response will be a JSON object with the issue ID, title, description, status, creation date, update date, and delete date.

The API has been deployed in a Docker container using Docker Compose. PostgreSQL was used for data storage using SQLAlchemy. For automated testing, tests were written using pytest. Alembic was used to manage database migrations.














