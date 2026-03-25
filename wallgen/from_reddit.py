#!/usr/bin/python3

import re
import json
from http import client
from random import randint
from wand.image import Image
from wallgen import __util__

class RedditGenerator:
    def __init__(self, subreddit='earthporn'):
        self.subreddit = subreddit
        self.reset()

    def get_image(self, width=1920, height=1080, dark_mode=False) -> Image:
        p = re.compile(r"\.(?:jpg|jpeg|png)$", re.IGNORECASE)
        valid_urls = []
        
        for post in self.posts:
            data = post.get("data", {})
            url = data.get("url", "")
            
            if not p.search(url):
                continue
                
            preview = data.get("preview", {})
            images = preview.get("images", [])
            
            if images:
                source = images[0].get("source", {})
                img_w = source.get("width", 0)
                img_h = source.get("height", 0)
                
                if img_w >= width and img_h >= height and url not in self.used_images:
                    valid_urls.append(url)

        if not valid_urls:
            print("Warnung: Keine Bilder in der passenden Größe gefunden. Ignoriere Auflösungs-Filter...")
            valid_urls = [post["data"]["url"] for post in self.posts if p.search(post.get("data", {}).get("url", ""))]
            
        rnd = randint(0, len(valid_urls) - 1)
        final_url = valid_urls[rnd]
        self.used_images.append(final_url)

        return __util__.create_image(final_url, width, height)

    def reset(self):
        con = client.HTTPSConnection('www.reddit.com')
        con.request('GET', '/r/%s.json' % self.subreddit, headers={ 'User-Agent': 'linux:wallgen (by /u/hobbypunk90)'})
        response = con.getresponse()
        json_string = response.read()
        con.close()
        
        struct = json.loads(json_string.decode('utf-8'))
        self.posts = struct.get("data", {}).get("children", [])
        
        self.used_images = []
