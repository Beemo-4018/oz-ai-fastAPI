from fastapi import FastAPI

app = FastAPI()

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]


@app.get("/users")
def get_users_handlers():
    return users


@app.get("/users/{user_id}")
def get_user_handler(user_id: int):
    return users[user_id - 1]
