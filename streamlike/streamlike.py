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
        if r.headers['content-type'] == 'application/json':
            return r.json()
        else:
            return r.text

    def add_media(self,media_url,permalink,media_type,name,status,
                    description,credits,keywords,codec='h264',hide_controls=True,callback_url=None,
                    ):
        payload = {
            'media':{
                'media_type':media_type,
                'permalink':permalink,
                'media_files':{
                'for_encoding':{
                    'media_url':media_url,
                    'codec':codec,
                    'callback_url':callback_url
                    }
                },
                'name':name,
                'description':description,
                'hide_controls':hide_controls,
                'status':status,
                'credits':credits,
                'keywords':keywords,

            }
        }
        return self.make_call('media','POST',payload=payload)
    
    def update_media(self, media_id, updated_fields=None):
        payload = {
            'media':updated_fields
        }
        endpoint = 'media/{0}'.format(media_id)
        return self.make_call(endpoint, 'PUT', payload=payload)

    def delete_media(self,media_id):
        endpoint = 'media/{0}'.format(media_id)
        return self.make_call(endpoint, 'DELETE')

    def search_media(self, media_id=None, params=None):
        if media_id:
            endpoint = 'media/{0}'.format(media_id)
        else:
            endpoint = 'media'

        return self.make_call(endpoint,'GET',params=params)

    def create_tag(self,name,tag_type,color,parent_tag_id=None):
        payload = {
           "tag":{
              "name":name,
              "type":tag_type,
              "color":color,
              "parent_tag_id":parent_tag_id
           }
        }
        return self.make_call('tag','POST',payload=payload)

    def search_tag(self, tag_id=None, params=None):
        if tag_id:
            endpoint = 'tag/{0}'.format(tag_id)
        else:
            endpoint = 'tag'

        return self.make_call(endpoint,'GET',params=params)
