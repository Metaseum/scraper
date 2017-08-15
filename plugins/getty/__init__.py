#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import simplejson as json
import os
from celery import Task


class Crawler(object):

    def __init__(self):
        self.min = 1
        self.max = 10
        self.urls = self.gen()

    def gen(self):
        for num in range(self.min, self.max + 1):
            yield {'url': 'http://www.getty.edu/art/collection/objects/{}'.format(num), 'num': num}

    def run(self):
        for url in self.urls:
            sc = Scraper()
            sc.scrape(url)


class Scraper(Task):
    ignore_result = True

    meta_blacklist = ['viewport', 'apple-mobile-web-app-capable', 'robots', 'level']

    def run(self, source, *args, **kwargs):
        self.url = source['url']
        self.objid = source['num']

        self.metadata = {}
        self.valid = True
        self.r = requests.get(self.url)
        self.metadata['canonical_url'] = self.url

        if self.r.status_code == 200:
            self.mine()
        else:
            print('error: ', self.r.status_code)
            self.valid = False

        print(self.metadata)



    def scrape(self, source):
        print('scraping', source)
        self.run(source)


    def mine(self):
        soup = BeautifulSoup(self.r.content, 'html.parser')

        for meta in soup.findAll("meta"):
            name = meta.get('name', '')
            if name is not '' and name not in self.meta_blacklist:
                self.metadata[name] = meta.get('content', '')

        if 'image' in self.metadata and self.metadata['open_content'] == 'yes':
            self.metadata['image_full'] = self.metadata['image'].replace('/enlarge/', '/download/')

        if 'name' in self.metadata and self.metadata['name'] == 'Collection':
            self.valid = False
        else:
            self.valid = True


    def __str__(self):
        return 'obj#{}'.format(self.objid)


    @property
    def filename(self):
        if self.valid:
            return '{0:08d}.json'.format(self.objid)
        else:
            return None


    def dump(self, parent):
        if self.valid is False:
            return False

        this_dir = '{}/'.format(parent, self.filename[2:4], self.filename[4:6])
        os.makedirs(this_dir, exist_ok=True)

        with open(os.path.join(this_dir, self.filename), 'w') as f:
            json.dump(self.metadata, f, indent=4, ensure_ascii=False, sort_keys=True)
        return True