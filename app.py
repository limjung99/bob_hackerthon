from bs4 import BeautifulSoup as bs
import requests


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




