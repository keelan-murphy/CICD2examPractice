from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base, UserDB
from app.schemas import UserCreate, UserRead

# Create tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab 3 - FastAPI SQLAlchemy User API")


@app.get("/health")
def health():
    return {"status": "ok"}

#ON PAGE 16
@app.post(
    "/api/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def add_user(new_user: UserCreate, db: Session = Depends(get_db)):
    # Turn validated JSON into a database row object
    db_user = UserDB(**new_user.model_dump())
    db.add(db_user)

    try:
        db.commit()          # save permanently to app.db
        db.refresh(db_user)  # load DB-generated id onto db_user
    except IntegrityError:
        db.rollback()        # undo failed transaction
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email or student_id already exists",
        )
    return db_user  # response_model=UserRead (+ from_attributes) shapes the JSON



#PAGE 24 
@app.get("/api/users", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    statement = select(UserDB).order_by(UserDB.id)
    return db.execute(statement).scalars().all()
#PAGE 26
@app.get("/api/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user

#NOT IN THE LECTURE NOTES
@app.delete(
    "/api/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(db_user)  # mark row for removal
    db.commit()         # make it permanent in app.db
    return              # 204 = no body