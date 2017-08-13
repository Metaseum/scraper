#!/usr/bin/env python

from celery import Celery
import getty
from pprint import pprint

app = Celery('tasks', broker='amqp://guest@localhost//')
app.control.time_limit('get_object', soft=10, hard=20, reply=True)


@app.task
def get_object(objid):
    this_obj = getty.get(objid)
    if this_obj.valid:
        this_obj.dump('../data-getty/json/')
        print('valid objid #{}'.format(objid))
        return True
    else:
        print('invalid objid #{}'.format(objid))
        return False
