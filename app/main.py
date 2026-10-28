from fastapi import FastAPI, HTTPException, status

from app.schemas import UserCreate

app = FastAPI(title="Example template")

users: list[UserCreate] = [] 
#temporary storage... restart server -> list empties


@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/hello")
def hello():
    return{"status": "hello FROM FASTAPI"}

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(new_user: UserCreate):
    for existing_user in users: 
        if existing_user.user_id == new_user.user_id:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail="A user with this user_id already exists",
            )
    users.append(new_user)
    return new_user

