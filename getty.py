#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import simplejson as json
import os

meta_blacklist = ['viewport', 'apple-mobile-web-app-capable', 'robots', 'level']

class GettyObject(object):

    def __init__(self, objid):
        self.metadata = {}
        self.objid = objid
        self.r = requests.get(self.url)

        if self.r.status_code == 200:
            self.mine()
        else:
            print('error: ', self.r.status_code)

    def __str__(self):
        return 'obj#{}'.format(self.objid)

    @property
    def url(self):
        return 'http://www.getty.edu/art/collection/objects/{}'.format(self.objid)

    @property
    def filename(self):
        return '{0:08d}.json'.format(self.objid)

    def dump(self, parent):
        with open(os.path.join(parent, self.filename), 'w') as f:
            json.dump(self.metadata, f, ensure_ascii=False)
    
    def mine(self):
        soup = BeautifulSoup(self.r.content, 'html.parser')

        for meta in soup.findAll("meta"):
            name = meta.get('name', '')
            if name is not '' and name not in meta_blacklist:
                self.metadata[name] = meta.get('content', '')

        if 'image' in self.metadata and self.metadata['open_content'] == 'yes':
            self.metadata['image_full'] = self.metadata['image'].replace('/enlarge/', '/download/')

def get(objid):
    return GettyObject(objid)