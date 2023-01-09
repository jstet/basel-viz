from pydantic import BaseModel
from pydantic.schema import Optional, List
from datetime import datetime

class Standard(BaseModel):
    all: List[dict]

    class Config:
        orm_mode = True



    

    