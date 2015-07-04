from xml.etree import ElementTree
from .helpers import raise_errors_on_failure
import requests
import json

class Streamlike:
    def __init__(self,login,password,api_key):
        self.login = login
        self.password = password
        self.api_key = api_key
        self.api_url = 'https://api.streamlike.com/'
        self.token = self.get_token()

    def get_token(self):
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Streamlike-Authorization': 'streamlikeAuth certificate="{0}"'.format(self.api_key),
                }
        payload = { 
                    'login':self.login,
                    'password':self.password
                    }
        r = requests.post("https://api.streamlike.com/streamlikeAuthToken", 
                            data=payload, headers=headers)
        headers['X-Streamlike-Authorization'] = 'streamlikeAuth token="{0}"'.format(ElementTree.fromstring(r.text).find('token').text)
        headers['Content-Type'] = 'application/xml'
        r = requests.post("https://api.streamlike.com/streamlikeAuthSessionToken", headers=headers)
        return ElementTree.fromstring(r.text).find('token').text

    def make_call(self,endpoint,method,payload=None,params=None):
        headers = {
        'Accept':'application/json',
        'Content-Type': 'application/json',
        'X-Streamlike-Authorization': 'streamlikeAuth token="{0}"'.format(self.token)
                }
        if method == 'GET':
            r = requests.get(self.api_url + endpoint, headers=headers, params=params)
            r = raise_errors_on_failure(r)
        if method == 'DELETE':
            r = requests.delete(self.api_url + endpoint, headers=headers, 
                            data=json.dumps(payload))
            r = raise_errors_on_failure(r)
        if method == 'POST':
            r = requests.post(self.api_url + endpoint, headers=headers,
                            data=json.dumps(payload))
            r = raise_errors_on_failure(r)
        if method == 'PUT':
            r = requests.put(self.api_url + endpoint, headers=headers,
                            data=json.dumps(payload))
            r = raise_errors_on_failure(r)
       
        return r.json()

    def add_media(self,media_url,permalink,media_type,name,status,
                    description,credits,keyword,codec='h264',hide_controls=True,callback_url=None,
                    ):
        payload = {
            'media':{
                'media_type':media_type,
                'permalink':permalink,
                'name':name,
                'description':description,
                'hide_controls':hide_controls,
                'callback_url':callback_url,
                'status':status,
                'codec':codec,
                'credits':credits,
                'keyword':keyword,

            }
        }
        return self.make_call('media','POST',payload=payload)

    def search_media(self,params=None):
        return self.make_call('media','GET',params=params)

