from bs4 import BeautifulSoup as bs
import requests
from template import *


# 데이터 단어 추출
from keybert import KeyBERT
from kiwipiepy import Kiwi 
from transformers import BertModel
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# open ai관련
from config import conf
import openai

api_key = conf["OPENAI_API_KEY"]
openai.api_key = api_key


# query to gpt api
def queryToGpt(data:str):
    query_text = data
    query_text += "<- by using these features,Guess how this person looks like and "
    query_text += "Just extract 5 appearance keywords in English and divide keywords using ','. "
    # create with API ------------------------------
    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": query_text}],
    )
    return chat_completion.choices[0].message.content
    

# qeury to Dalle api 
def queryToDalle(data):
     diffusion_query_text = generate_realistic()
    print(diffusion_query_text)
    # 이미지 create with API --------------------------
    response = openai.Image.create(
    prompt= diffusion_query_text,
    n=2,
    size = "1024x1024",
    )
    image_url = response["data"][0]["url"]
    image_data = requests.get(image_url).content

def crawlBobWiki(name:str):
    path = "https://kitribob.wiki/wiki/"
    response = requests.get(path+name)
    soup = bs(response.text , "html.parser")
    text = soup.find("article").text
    return text


########### 단어 추출 관련 함수들################
def noun_extractor(text):
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
            results.append(token)
    return results

def tokenizer(text):
    okt = Okt()
    return okt.morphs(text)



def main_word_extractor(text):
    text = text.replace("\n","")
    kiwi.analyze(text)
    nouns = noun_extractor(text)
    text = ' '.join(nouns)
    
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    result = ' '.join(filtered_words)
    
    # keybert
    model = BertModel.from_pretrained('skt/kobert-base-v1')
    kw_model = KeyBERT(model)
    keywords = kw_model.extract_keywords(result, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=10)
    
    
    
    vectorizer = TfidfVectorizer(tokenizer=tokenizer, max_features=10)
    tfidf_matrix = vectorizer.fit_transform([text])  # 리스트 형태로 변환

    # tfidf
    feature_names = vectorizer.get_feature_names_out()
    sorted_feature_names = np.array(feature_names)[tfidf_matrix.sum(axis=0).argsort()[0, ::-1]]
    
    
    # 형태 통일
    first_words = [item[0] for item in keywords]
    second_words = sorted_feature_names[0]

    # 공통 부분 찾기
    common_words = set(first_words).intersection(second_words)
    print("공통 단어:", common_words)

    # 상위 3개 단어 뽑기
    top3_first = first_words[:3]
    top3_second = second_words[:3]

    print("keybert에서 상위 3개 단어:", top3_first)
    print("tfidf에서 상위 3개 단어:", top3_second)
    
    top3_first.extend(top3_second)
    top3_first.extend(common_words)
    
    ans=set(top3_first)
    
    return list(ans)
##############################################################3



