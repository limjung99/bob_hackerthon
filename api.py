from fastapi import FastAPI
from models import Data
from config import conf
from app import *

import requests
import os
import openai
openai.api_key = '' # 추가


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
    text=text.replace("\n", "")

    text = main_word_extractor(text)
    # text -> 주요 단어 리스트(keybert and tfidf)





    # 이미지 create with API
    response = openai.Image.create(
    prompt=text, 
    n=2,
    size = "1024x1024"
    )
    image_url = response["data"][0]["url"]
    image_data = requests.get(image_url).content

    # 이 위에 구현해주면 되용

    return image_data # return 이미지



