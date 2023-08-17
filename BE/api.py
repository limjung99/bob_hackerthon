from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import Data
from logic import *
from template import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 호스트 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


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
    describe_texts = [self_describe, crawled_text] #밥위키, 내거
    query_texts = []
    images_urls = {}
    # GPT에게 쿼리 
    # 0 : bob위키를 바탕으로 생성한 이미지 
    # 1 : 내가 생각한 나의 이미지 
    for text in describe_texts:
        query_text = queryToGpt(text)
        query_texts.append(query_text)
    
    # Dal-e에게 쿼리
    for idx,text in enumerate(query_texts):
        image_url = queryToDalle(text)
        images_urls[idx]={
            "image_url" : image_url ,
            "text" : text
        }
    return JSONResponse(content=images_urls)



  


