import polars as pl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.dml import INSERT, SELECT
from backend.db import initdb

ENGINE = initdb()

insert = INSERT(ENGINE)
select = SELECT(ENGINE)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)


class User(BaseModel):
    username: str
    password: str


class Task(BaseModel):
    task: str
    deadline: str
    user: str


@app.post("/login/")
async def user_login(User: User):
    """
    Handles the user login process.
    The function checks if the user exists in the users CSV file.
    If the username and password match, the user is logged in successfully.

    Args:
        User (User): The username and password provided by the user.

    Returns:
        dict: A response indicating whether the login was successful or not.
              - If successful, ttasktatus will be "Logged in".
              - If failed (user not found or incorrect password),
                appropriate message will be returned.
    """
    data = select.users_by_username(User.username)

    if data is None:
        return JSONResponse(
            content={"status": "User doesn't exist"}, status_code=404
        )

    correct_user = User.username in data[1]
    correct_password = User.password in data[2]

    if correct_user and correct_password:
        return JSONResponse(
            content={"status": "Logged in"}, status_code=200
        )
    elif correct_user and not correct_password:
        return JSONResponse(
            content={"status": "Incorrect password"}, status_code=401
        )

    return JSONResponse(
        content={"status": "Something went wrong"}, status_code=500
    )


@app.post("/create_user/")
async def create_user(User: User):
    """
    Creates a new user by adding their username and password
    to the users table.

    Args:
        User (User): The username and password for the new user.

    Returns:
        dict: A response indicating whether the user was successfully created.
              - If successful, the status will be "User Created".
              - If user already exists, a relevant message will be returned.
    """

    data = select.users_by_username(User.username)

    if data is not None:
        return JSONResponse(
            content={"status": "User already exists"}, status_code=409
        )

    try:
        data = insert.user(User.username, User.password)
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"status": "Something went wrong"}, status_code=500
        )
    else:
        return JSONResponse(
            content={"status": "User Created"}, status_code=201
        )


@app.post("/create_task/")
async def create_task(Task: Task):
    """
    Creates a new task by adding the task description, deadline,
    and associated user to the tasks CSV file.

    Args:
        Task (Task): The task description, deadline, and associated user.

    Returns:
        dict: A response indicating whether the task was successfully created.
              - If successful, the status will be "Task Created".
    """

    data = select.users_by_username(Task.user)

    if data is None:
        return JSONResponse(
            content={"status": "User doesn't exist"}, status_code=404
        )

    try:
        insert.task(Task.task, Task.deadline, Task.user)
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"status": "Something went wrong"}, status_code=500
        )
    else:
        return JSONResponse(
            content={"status": "task Created"}, status_code=201
        )


@app.get("/get_tasks/")
async def get_tasks(name: str):
    """
    Retrieves the list of tasks associated with a specific user.

    Args:
        name (str): The username for which the tasks need to be fetched.

    Returns:
        dict:
            A list of tasks (task description, deadline)
            associated with the given user.
              - If tasks are found, the response will include the task details.
              - If no tasks are found for the user,
                an empty list will be returned.
    """

    data = select.users_by_username(name)

    if data is None:
        return JSONResponse(
            content={"status": "User doesn't exist"}, status_code=404
        )

    try:

        data = select.tasks_by_username(name)

        if len(data) == 0:
            return JSONResponse(
                content={"tasks": []}, status_code=200
            )

        tasks = (
            pl.DataFrame(select.tasks_by_username(name))
            .select(["task", "deadline", "username"])
            .with_columns(
                pl.col("deadline").cast(pl.Utf8).alias("deadline")
            )
            .to_pandas()
            .values.tolist()
        )

    except Exception as e:
        print(type(e))
        return JSONResponse(
            content={"status": "Something went wrong"}, status_code=500
        )
    else:
        return JSONResponse(
            content={"tasks": tasks}, status_code=200
        )
