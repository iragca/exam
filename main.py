import polars as pl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    Handles the user login process. The function checks if the user exists in the users CSV file.
    If the username and password match, the user is logged in successfully.

    Args:
        User (User): The username and password provided by the user.

    Returns:
        dict: A response indicating whether the login was successful or not.
              - If successful, ttasktatus will be "Logged in".
              - If failed (user not found or incorrect password), appropriate message will be returned.
    """
    data = pl.read_csv("users.csv")

    correct_user = User.username in data["username"]
    correct_password = User.password in data["password"]

    if correct_user and correct_password:
        return {"status": "Logged in"}
    elif correct_user and not correct_password:
        return {"status": "Incorrect Password"}

    return {"status": "User not found"}


@app.post("/create_user/")
async def create_user(User: User):
    """
    Creates a new user by adding their username and password to the users CSV file.

    Args:
        User (User): The username and password for the new user.

    Returns:
        dict: A response indicating whether the user was successfully created.
              - If successful, the status will be "User Created".
              - If user already exists, a relevant message will be returned.
    """

    data = pl.read_csv("users.csv")

    if User.username in data["username"]:
        return {"status": "User already exists"}

    pl.concat(
        [data, pl.DataFrame({"username": [User.username], "password": [User.password]})]
    ).write_csv("users.csv")

    return {"status": "User Created"}


@app.post("/create_task/")
async def create_task(Task: Task):
    """
    Creates a new task by adding the task description, deadline, and associated user to the tasks CSV file.

    Args:
        Task (Task): The task description, deadline, and associated user.

    Returns:
        dict: A response indicating whether the task was successfully created.
              - If successful, the status will be "Task Created".
    """
    print(Task)
    task_data = pl.read_csv("tasks.csv")
    user_data = pl.read_csv("users.csv")

    if Task.user not in user_data["username"]:
        return {"status": "User not found"}

    pl.concat(
        [
            task_data,
            pl.DataFrame(
                {
                    "task": [Task.task],
                    "deadline": [Task.deadline],
                    "user": [Task.user],
                }
            ),
        ]
    ).write_csv("tasks.csv")

    return {"status": "task Created"}


@app.get("/get_tasks/")
async def get_tasks(name: str):
    """
    Retrieves the list of tasks associated with a specific user.

    Args:
        name (str): The username for which the tasks need to be fetched.

    Returns:
        dict: A list of tasks (task description, deadline) associated with the given user.
              - If tasks are found, the response will include the task details.
              - If no tasks are found for the user, an empty list will be returned.
    """

    print(name)
    task_data = pl.read_csv("tasks.csv").to_pandas()
    user_data = pl.read_csv("users.csv")

    if name not in user_data["username"]:
        return {"error": "User not found"}

    tasks = task_data.loc[task_data["user"] == name]

    if len(tasks) == 0:
        return {"tasks": []}

    return {"tasks": tasks.values.tolist()}
