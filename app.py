from bs4 import BeautifulSoup as bs
import requests


# 데이터 단어 추출
from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import word_extractor

# open ai관련
import os
import openai

stopwords = [
    "의", "가", "이", "은", "들", "는", "좀", "잘", "걍", "과", "도", "를", "으로", "자", "에", "와", "한", "하다",
    "저", "그", "것", "들", "그녀", "인", "적", "하는", "입니다", "게", "와", "에게", "으로는", "도", "등", "에서", "로", "에는", "나", "해", "합니다", "일", "말", "인데", "그런", "데", "다"
]


# query to gpt api
def queryToGpt(data):
    pass

# qeury to Dalle api 
def queryToDalle(data):
    pass

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
    kiwi = Kiwi()
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



