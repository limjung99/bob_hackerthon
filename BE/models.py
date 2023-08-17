from pydantic import BaseModel

# json model
class Data(BaseModel):
    name : str
    is_crawl : bool
    describe : str 

    