from django.shortcuts import render,redirect
import requests
from django.http import JsonResponse
import base64

def get_data(owner,repo):
    # Make the URL to get from requests
    API_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Fetching data from Github API
    response = requests.get(API_url,timeout = 10)

    # Checking if the  Url is valid
    # If status code not equal to 200 return None
    if response.status_code != 200:
        return  None
    else: #else Convert response into json structure and return it
        data = response.json()
        print(data)
        return data

# Function to get readme from url
def get_readme(owner,repo):
    # making the url from owner and repository
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    # Fetch response from Github API
    response = requests.get(url,timeout=10)

    # Checking if the response is valid
    #If readme does not exist then return "No readme found "
    if response.status_code != 200:
        return "No readme found"

    # Convert readme into json
    readme = response.json()

    # If readme is empty then return "Readme is empty "
    if not readme.get("content"):
        return "Readme is Empty"

    # Decode readme from base64
    readme = base64.b64decode(readme["content"])
    readme = readme.decode("utf-8",errors="ignore")

    # Limit readme length
    readme = readme[:3000]

    #Return the readme
    print(readme)
    return readme

#Function to split the url
def split_url(url):

    if not url:
        return None, None

    url = url.rstrip('/')
    url = url.split("/")

    if len(url) != 5:
        return None, None

    if url[2] != "github.com":
        return None, None

    owner = url[3]
    repository = url[4]

    return owner, repository

#Checking if url is valid
def checking(url):
    owner,repo = split_url(url)
    if not owner or not repo:
        return None
    data = get_data(owner, repo)
    if not data:
        return None
    return "ok"