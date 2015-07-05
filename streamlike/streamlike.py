"""The streamlike module"""
from xml.etree import ElementTree
from streamlike.helpers import raise_errors_on_failure
import requests
import json

class Streamlike:
    """
        The wrapper class for the streamlike api.

        Note that all API calls can return an exception from streamlike.exceptions.
    """
    def __init__(self, login, password, api_key):
        """
            initializes streamlike;
            Throws exception if session token cannot be obtained.

            login    -- login name for streamlike
            password -- password for streamlike login
            api key  -- api key for streamlike
        """
        self.login = login
        self.password = password
        self.api_key = api_key
        self.api_url = 'https://api.streamlike.com/'
        self.token = self.get_token()

    def get_token(self):
        """
            helper that tries to obtain a session token.

            returns -- token content
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Streamlike-Authorization': 'streamlikeAuth certificate="{0}"'.format(self.api_key),
        }
        payload = {
            'login': self.login,
            'password': self.password
        }
        req = requests.post("https://api.streamlike.com/streamlikeAuthToken",
                            data=payload,
                            headers=headers
                           )
        auth_token = ElementTree.fromstring(req.text).find('token').text
        headers['X-Streamlike-Authorization'] = 'streamlikeAuth token="{0}"'.format(auth_token)
        headers['Content-Type'] = 'application/xml'
        req = requests.post("https://api.streamlike.com/streamlikeAuthSessionToken",
                            headers=headers
                           )
        return ElementTree.fromstring(req.text).find('token').text

    def make_call(self, endpoint, method, payload=None, params=None):
        """
            helper that performs a request to a specified endpoint.

            endpoint -- the endpoint to request
            method   -- the request type
            payload  -- the request payload (optional)
            params   -- the request params (optional)
        """
        headers = {
            'Accept':'application/json',
            'Content-Type': 'application/json',
            'X-Streamlike-Authorization': 'streamlikeAuth token="{0}"'.format(self.token)
        }
        if method == 'GET':
            req = requests.get(self.api_url + endpoint, headers=headers, params=params)
        if method == 'DELETE':
            req = requests.delete(self.api_url + endpoint,
                                  headers=headers,
                                  data=json.dumps(payload)
                                 )
        if method == 'POST':
            req = requests.post(self.api_url + endpoint,
                                headers=headers,
                                data=json.dumps(payload)
                               )
        if method == 'PUT':
            req = requests.put(self.api_url + endpoint,
                               headers=headers,
                               data=json.dumps(payload)
                              )
        raise_errors_on_failure(req)
        if req.headers['content-type'] == 'application/json':
            return req.json()
        return req.text

    #TODO: Find decent way to strip some of the arguments or let them default
    def add_media(self, media_url, permalink, media_type, name,
                  status, description, creds, keywords, codec='h264',
                  hide_controls=True, callback_url=None
                 ):
        """
            adds a medium to streamlike.

            media_url     -- the url under which the medium is to be found
            permalink     -- the medium's permalink
            metia_type    -- the medium's type
            name          -- the medium's name
            status        -- the medium's status
            description   -- a description for the medium
            creds         -- the medium's credits (so called because there is
                             a lesser-known Python builtin of the same name)
            keywords      -- keywords for the medium
            codec         -- the medium's codec (optional, defaults to h264)
            hide_controls -- toggles whether controls are shown (optional,
                             defaults to True)
            callback_url  -- the medium's callback url (optional)
        """
        payload = {
            'media': {
                'media_type': media_type,
                'permalink': permalink,
                'media_files': {
                    'for_encoding': {
                        'media_url': media_url,
                        'codec': codec,
                        'callback_url': callback_url
                    }
                },
                'name': name,
                'description': description,
                'hide_controls': hide_controls,
                'status': status,
                'credits': creds,
                'keywords': keywords,

            }
        }
        return self.make_call('media', 'POST', payload=payload)

    def update_media(self, media_id, updated_fields=None):
        """
            updates a streamlike medium.

            media_id -- the mediums' id
        """
        payload = {'media': updated_fields}
        endpoint = 'media/{0}'.format(media_id)
        return self.make_call(endpoint, 'PUT', payload=payload)

    def delete_media(self, media_id):
        """
            deletes a streamlike medium by its' id.

            media_id -- the mediums' id.
        """
        endpoint = 'media/{0}'.format(media_id)
        return self.make_call(endpoint, 'DELETE')

    def search_media(self, media_id=None, params=None):
        """
            searches for a medium on streamlike.
            If no id is provided, all media are returned.

            media_id -- the medium's id (optional)
            params   -- params for the call (optional)
        """
        endpoint = 'media'
        if media_id:
            endpoint += '/{0}'.format(media_id)

        return self.make_call(endpoint, 'GET', params=params)

    def create_tag(self, name, tag_type, color, parent_tag=None):
        """
            creates a tag on streamlike.

            name       -- the tag's name
            tag_type   -- the tag's type
            color      -- the tag's color
            parent_tag -- the parent tag's id (optional)
        """
        payload = {
            "tag": {
                "name": name,
                "type": tag_type,
                "color": color,
                "parent_tag_id": parent_tag
            }
        }
        return self.make_call('tag', 'POST', payload=payload)

    def search_tag(self, tag_id=None, params=None):
        """
            searches for a tag on streamlike.
            if no id is provided, all tags are returned.

            tag_id -- the tag's id (optional)
            params -- params for the call (optional)
        """
        endpoint = 'tag'
        if tag_id:
            endpoint += '/{0}'.format(tag_id)

        return self.make_call(endpoint, 'GET', params=params)
