from pydantic import BaseModel

# json model
class Data(BaseModel):
    name : str
    describe : str 

    