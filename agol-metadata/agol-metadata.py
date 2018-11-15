# Kudos to Thomas Maschler for the code
# https://gist.github.com/thomas-maschler/388554ddb6deae6371db

import requests
import json

def request_token(user, password):

    d = {"username": user,
         "password": password,
         "referer":"http://www.arcgis.com",
         "f": "json"}
    
    url = "https://www.arcgis.com/sharing/rest/generateToken"

    r = requests.post(url, data = d)

    response = json.loads(r.content)

    if 'error' in response.keys():
        raise Exception(response['message'], response['details'])
    
    return response

def update_metadata(user, item, token, metadata):
    
    d = {"overwrite": "true",
         "token" :token,
         "f":"json"}
    f = {'metadata': ('metadata.xml', open(metadata, 'rb'), 'text/xml', {'Expires': '0'})} 
    
    url = 'http://www.arcgis.com/sharing/rest/content/users/{0}/items/{1}/update'.format(user, item)
    r = requests.post(url, data = d, files = f)

    response = json.loads(r.content)

    if 'error' in response.keys():
        raise Exception(response['message'], response['details'])

    return response
  
if __name__ == "__main__":
    metadata = "the path to your metadata XML-file should go here"
    user = "your username should go here"
    password = "your password should go here"
    item = "your item id should go here" 
    token = request_token(user, password)['token']
    
    print(update_metadata(user, item, token, metadata))