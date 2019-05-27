import cookielib
import hashlib
import urllib2
import sys
import urllib.request
import requests
import base64
import time
import json
import re
import os
import rsa
import binascii
import random
from PIL import Image
from urllib.parse import urlencode
import urllib

USERNAME = 'liuyt49@163.com'
PASSWORD = '123123789'


body = {
    '__rnd': '',
    '_k': '',
    '_t': '0',
    'count': '50',
    'end_id': '',
    'max_id': '',
    'page': 1,
    'pagebar': '',
    'pre_page': '0',
    'uid': '1742439305'
}

uuid = None
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

#获取 servertime noce pubkey rsakv


def get_info():
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=woshigaolin@sina.cn&rsakt=mod&client=ssologin.js(v1.4.4)'
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        publicKey = data['pubkey']
        rsakey = data['rsakv']
        return servertime, nonce, publicKey, rsakey
    except:
        print ('error')
        return None


st, non, pubkey, rsakv = get_info()

#用户名加密


def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

#密码加密


def get_pwd(pwd):
    rsaPublicKey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublicKey, 65537)
    message = str(st) + '\t' + str(non) + '\n' + str(pwd)
    pwd_1 = rsa.encrypt(message, key)
    pwd_2 = binascii.b2a_hex(pwd_1)
    return pwd_2


def login(username, pwd):
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv': rsakv,
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    postdata['servertime'] = st
    postdata['nonce'] = non
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd)
    postdata_url = urllib.urlencode(postdata)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}
    req = urllib2.Request(url=url, data=postdata_url, headers=headers)
    result = urllib2.urlopen(req)
    text = result.read()
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        url_login = p.search(text).group(1)
        content = urllib2.urlopen(url_login).read()
        p = re.compile('uniqueid\"\:\"(.*?)\"')
        uuid = p.search(content).group(1)
    except:
        print ('error')


if __name__ == '__main__':

    login(USERNAME, PASSWORD)

    url = 'http://weibo.com/%s?from=otherprofile&wvr=3.6&loc=tagweibo' % (uuid)
    url = url + urllib.urlencode(body)
    req = urllib2.Request(url)
    result = urllib2.urlopen(req).read()
    print (result)
