#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import simplejson as json
import os

meta_blacklist = ['viewport', 'apple-mobile-web-app-capable', 'robots', 'level']

class GettyObject(object):

    def __init__(self, objid):
        self.valid = True
        self.metadata = {}
        self.objid = objid
        self.r = requests.get(self.url)
        self.metadata['canonical_url'] = self.url

        if self.r.status_code == 200:
            self.mine()
        else:
            print('error: ', self.r.status_code)
            self.valid = False

    def __str__(self):
        return 'obj#{}'.format(self.objid)

    @property
    def url(self):
        if self.valid:
            return 'http://www.getty.edu/art/collection/objects/{}'.format(self.objid)
        else:
            return None

    @property
    def filename(self):
        if self.valid:
            return '{0:08d}.json'.format(self.objid)
        else:
            return None

    def dump(self, parent):
        if self.valid is False:
            return False
        with open(os.path.join(parent, self.filename), 'w') as f:
            json.dump(self.metadata, f, ensure_ascii=False)
        return True
    
    def mine(self):
        soup = BeautifulSoup(self.r.content, 'html.parser')

        for meta in soup.findAll("meta"):
            name = meta.get('name', '')
            if name is not '' and name not in meta_blacklist:
                self.metadata[name] = meta.get('content', '')

        if 'image' in self.metadata and self.metadata['open_content'] == 'yes':
            self.metadata['image_full'] = self.metadata['image'].replace('/enlarge/', '/download/')

        if 'name' in self.metadata and self.metadata['name'] == 'Collection':
            self.valid = False
        else:
            self.valid = True

def get(objid):
    return GettyObject(objid)