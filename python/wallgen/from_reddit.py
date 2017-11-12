#!/usr/bin/python3

import re
import json
from http import client
from random import randint
from wand.image import Image
from wallgen import __util__

def get_image(subreddit='earthporn', width=1920, height=1080) -> Image:
    con = client.HTTPSConnection('www.reddit.com')
    con.request('GET', '/r/%s.json' % subreddit)
    json_string = b''
    for line in con.getresponse():
        json_string += line
    
    struct = json.loads(json_string.decode('utf-8'))
    url = ""
    p = re.compile("(?:jpg)|(?:jpeg)|(?:png)$")
    while not p.search(url):
        rnd = randint(0, 24)
        url = struct["data"]["children"][rnd]["data"]["url"]
    con.close()
    return __util__.create_image(url, width, height)
