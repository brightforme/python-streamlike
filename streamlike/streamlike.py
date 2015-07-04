from xml.etree import ElementTree
import requests
import json

class Streamlike:
    def __init__(self,login,password,api_key):
        self.login = login
        self.password = password
        self.api_key = api_key
        self.token = get_token()
        self.api_url = 'https://api.streamlike.com/'

    def get_token(self):
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Streamlike-Authorization': 'streamlikeAuth certificate="{0}"'.format(self.api_key)
                }
        payload = { 
                    'login':self.login,
                    'password':self.password
                    }
        r = requests.post("https://api.streamlike.com/streamlikeAuthToken", 
                            data=payload, headers=headers)
        shitty_xml_response = ElementTree.fromstring(r.text)
        return shitty_xml_response.find('token').text

    def make_call(endpoint, method, payload=None):
        headers = {
        'Content-Type': 'application/json',
        'X-Streamlike-Authorization': 'streamlikeAuth token="{0}"'.format(self.token)
                }
        if method == 'GET':
            r = requests.get(self.api_url + endpoint, headers=headers)
        if method == 'DELETE':
            r = requests.delete(self.api_url + endpoint, headers=headers, 
                            data=json.dumps(payload))
        if method == 'POST':
            r = requests.post(self.api_url + endpoint, headers=headers,
                            data=json.dumps(payload))
        if method == 'PUT':
            r = requests.put(self.api_url + endpoint, headers=headers,
                            data=json.dumps(payload))

        return r.json()

    def add_media(self,media_url,permalink,media_type,name,slug,status,codec='h264',
                    description,credits,keyword,hide_controls=True,callback_url=None,
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
        return make_call('media','POST',payload=payload)


