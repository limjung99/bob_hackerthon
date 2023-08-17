from fastapi import FastAPI
from fastapi.responses import Response
from models import Data
from app import *
from template import *
import base64
import requests
import openai


app = FastAPI()


@app.get("/")
async def root():
    return "This is home for bob image generator. Enjoy it:)"

@app.post("/api/generate/")
def search(data:Data):
    name = data.name # 이름
    self_describe = data.describe # 자신이 생각한 자신의 모습 
    crawled_text = ""
    crawled_text = crawlBobWiki(name) # 밥위키 크롤링 데이터 
    crawled_text=crawled_text.replace("\n", "")
    describe_texts = [crawled_text,self_describe]
    query_texts = []
    images_base64 = []
    # GPT에게 쿼리
    for text in describe_texts:
        query_text = queryToGpt(text)
        query_texts.append(query_text)
    # Dal-e에게 쿼리
    for text in query_texts:
        image_data = queryToDalle(text)
        image_base64 =  base64.b64encode(image_data).decode("utf-8")
        images_base64.append(image_base64)


    # 이 위에 구현해주면 되용
    Response(content=image_data, media_type="image/jpeg")


  


