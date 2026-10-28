from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints

class userCreate(BaseModel) :
    user_id: int = Field(gt = 0) #number greater than 0
    name: Annotated[str, StringConstraints(min_length=2, max_length=50)] #2-50 characters
    email: EmailStr
    age: int = Field(gt=18, lt=120) #greater than 18. less than 120
    student_id: Annotated[str, StringConstraints(pattern=r"^S\d{7}$")] 
    #S + exactly 7 digits, e.g. S1234567

#annotated and field jsut mean "they must follow the rules inside the brackets"
