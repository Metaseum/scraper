#!/usr/bin/env python
import getty
from pprint import pprint



if __name__ == '__main__':
    this_obj = getty.get(826)
    pprint(this_obj.metadata)
    pprint(this_obj.filename)
    this_obj.dump('./json')