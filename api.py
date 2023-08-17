from fastapi import FastAPI
from fastapi.responses import Response
from models import Data
from config import conf
from app import *
from template import *

import requests
import openai

app = FastAPI()
api_key = conf["OPENAI_API_KEY"]
openai.api_key = api_key

@app.get("/")
async def root():
    return "This is home for bob image generator. Enjoy it:)"

@app.post("/api/generate/")
def search(data:Data):
    name = data.name
    is_crawl = data.is_crawl
    describe = data.describe
    crawled_text = ""
    # 밥위키 크롤해서 text 받아오기
    if is_crawl:
        crawled_text = crawlBobWiki(name)
    else:
        crawled_text = describe
    crawled_text=crawled_text.replace("\n", "")
    list_text = main_word_extractor(crawled_text)
    # text -> 주요 단어 리스트(keybert and tfidf)
    # gpt 쿼리 api ----------------------------------
    

    important_keywords = ""
    for text in list_text:
        important_keywords+=text+","



    # 프롬프트 쿼리 튜닝 
    query_text = crawled_text
    '''
    query_text+=important_keywords
    query_text+= " <- must apply this keywords."
    '''
    query_text += "Extract keywords at least 5, under 10."

    # create with API ------------------------------
    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": query_text}],
    )
    print(chat_completion.choices[0].message.content)

    diffusion_query_text = generate_realistic()
    diffusion_query_text += "Having these characteristic."
    diffusion_query_text += chat_completion.choices[0].message.content
    # 이미지 create with API --------------------------
    response = openai.Image.create(
    prompt= diffusion_query_text,
    n=2,
    size = "1024x1024",
    )
    image_url = response["data"][0]["url"]
    image_data = requests.get(image_url).content
    print(image_url)
    # 이 위에 구현해주면 되용
    Response(content=image_data, media_type="image/jpeg")


  


