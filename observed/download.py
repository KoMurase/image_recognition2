# -*- coding: utf-8 -*-
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os , time ,sys

#APIキーの情報　
key ="beabc03763137de13be1d009a7aaf2dd"
secret = "7982a41097311bf8"
wait_time = 1

#保存フォルダの指定
observed_thing = sys.argv[1]
savedir = './' + observed_thing

flickr = FlickrAPI(key,secret,format = 'parsed-json')
result = flickr.photos.search(
    text = observed_thing,
    per_page = 500,
    media ='photos',
    sort = 'relevance',
    safe_search = 1,
    extras = 'url_q ,licence'   #ここが一番大事　写真のurlとライセンス
)

photos = result['photos']
#返り値を表示していたpprint(photos)

for i, photos in enumerate(photos['photo']):
    try:
        url_q = photos['url_q']
    except:
        continue
    filepath = savedir + '/' + photos['id'] + '.jpg'
    if os.path.exists(filepath):continue
    urlretrieve(url_q,filepath)
    time.sleep(wait_time)
