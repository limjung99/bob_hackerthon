from fastapi import FastAPI
from models import Data
from config import conf
from app import *

app = FastAPI()

@app.get("/")
async def root():
    return "hello!"

@app.post("/api/generate/")
async def search(data:Data):
    name = data.name
    is_crawl = data.is_crawl
    describe = data.describe
    text = ""
    # 밥위키 크롤해서 text 받아오기
    if is_crawl:
        text = crawlBobWiki(name)
    else:
        text = describe
    
    # text -> bob위키 크롤링 텍스트 or 자기자신을 묘사한 텍스트
    


    # 이 위에 구현해주면 되용

    return text



