#-*- coding:utf-8 -*-
__author__ = 'Alexander.Li'
import logging

TEXT = u'text'
IMAGE = u'image'
LOCATION = u'location'
LINK = u'link'
EVENT = u"event"

def check_signature(token, params):
    import hashlib
    signature = params.get("signature")
    timestamp = params.get("timestamp")
    nonce = params.get("nonce")
    echostr = params.get("echostr")
    src = "".join([token, timestamp, nonce])
    m = hashlib.sha1()
    m.update(src)
    agro = m.hexdigest()
    if agro == signature:
        return echostr
    output = "%s is not %s"%(agro,signature)
    logging.debug(output)
    return output

def __parseContent(xml):
    from xml.dom.minidom import parseString
    dom = parseString(xml)
    root = dom.childNodes[0]
    return dict([(node.tagName, node.firstChild.nodeValue) for node in root.childNodes if node.nodeType==1])


def __generateContent(data):
    sequence = []
    if isinstance(data,dict):
        for key,value in data.iteritems():
            if isinstance(value,str) or isinstance(value,unicode):
                sequence.append("<%(tag)s><![CDATA[%(v)s]]></%(tag)s>"%dict(tag=key,v=value))
                continue
            if isinstance(value,list):
                sequence.append("<%(tag)s>%(v)s</%(tag)s>"%dict(tag=key,v=__generateContent(value)))
                continue
            if isinstance(value,dict):
                sequence.append("<%(tag)s>%(v)s</%(tag)s>"%dict(tag=key,v=__generateContent(value)))
                continue
            sequence.append("<%(tag)s>%(v)s</%(tag)s>"%dict(tag=key,v=value))
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                sequence.append("<item>%s</item>"%__generateContent(item))
                continue
            if isinstance(item, list):
                sequence.append("<item>%s</item>"%__generateContent(item))
                continue
            if isinstance(value,str) or isinstance(value,unicode):
                sequence.append("<item><![CDATA[%s]]></item>"%item)
                continue
            sequence.append("<item>%s></item>"%item)
    return "".join(sequence)

def __generateXml(data):
    return "".join(['<xml>',__generateContent(data),'</xml>'])


def response_text(content):
    return dict(Content=content)


def response_music(title,description,url,hd_url):
    return dict(Music = dict(Title = title, Description = description, MusicUrl = url, HQMusicUrl = hd_url))


class Article(object):
    def __init__(self, title, description, picurl, url):
        self.title = title
        self.description = description
        self.picurl = picurl
        self.url = url

def response_html(articles):
    if articles and isinstance(articles[0],type(Article)):
        return dict(
            Articles = [
                dict(Title = article.title, Description = article.description, PicUrl = article.picurl, Url = article.url)
                for article in articles
            ]
        )
    raise TypeError, u"Must be the list of Article class"


def process_request(data, callback):
    params = __parseContent(data)
    logging.debug("get params %s"%params)
    reply = dict(
            ToUserName = params["FromUserName"],
            FromUserName = params["ToUserName"],
            CreateTime = params["CreateTime"],
            MsgType = params['MsgType'],
            FuncFlag = 0
    )
    reply.update(callback(params['MsgType'],params))
    return __generateXml(reply)
