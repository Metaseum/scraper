#!/usr/bin/env python
import getty
from pprint import pprint
from tasks import get_object


if __name__ == '__main__':
    for objid in range(1, 100000):
        get_object.delay(objid)