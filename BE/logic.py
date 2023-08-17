from bs4 import BeautifulSoup as bs
import requests
from template import *
# open ai관련
from config import conf
import openai

api_key = conf["OPENAI_API_KEY"]
openai.api_key = api_key


# query to gpt api
def queryToGpt(data:str):
    query_text = data
    query_text += "<- get just 5 keywords in English without any special characters in front of them, separated by commas."
    #query_text += "Just extract 5 appearance keywords in English and divide keywords using ','. "
    #query_text += "<- Under 100 bytes."
    # create with API ------------------------------
    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": query_text}],
    )
    return chat_completion.choices[0].message.content
    

# qeury to Dalle api 
def queryToDalle(data):
    diffusion_query_text = data + generate_realistic()
    # diffusion_query_text += data
    # 이미지 create with API --------------------------
    response = openai.Image.create(
    prompt= diffusion_query_text,
    n=2,
    size = "1024x1024",
    )
    image_url = response["data"][0]["url"]
    return image_url

def crawlBobWiki(name:str):
    path = "https://kitribob.wiki/wiki/"
    response = requests.get(path+name)
    soup = bs(response.text , "html.parser")
    text = soup.find("article").text
    return text

