simpleweixin
============

a simple weixin public platform sdk of python

how to use:
---------------------------

1. pip install simpleweixin

2. from simpleweixin import weixinsdk

3. use weixinsdk.check_signature to check if it is a valid request

4. use weixinsdk.process_request to process the request data

example:
---------------------------

#-*- coding:utf-8 -*-
__author__ = 'Alexander.Li'
import logging
from flask import Flask, request
from simpleweixin import weixinsdk

app = Flask(__name__)

TOKEN = "123456"

def on_message(msg_type, data):
    """
    when got a request from weixin public platform,this method willbe fired
    """
    if msg_type == weixinsdk.TEXT: #if it is a text request
        return weixinsdk.response_text("text content") #response a text response
        # or there a more type of request such as IMAGE,LOCATION,LINK,EVENT
        # and more response such as response_music and response_html
        #


@app.route("/interface",methods=["GET","POST"])
def message_interface():
    if request.method == "POST":
        if weixinsdk.check_signature(TOKEN, request.args)
            data =  ''.join(request.environ['wsgi.input'].readlines()) # get request.data
            xml =  weixinsdk.process_request(data,on_message)
            return xml
        return "invalid request"
    else:
        return weixinsdk.check_signature(settings.TOKEN, request.args)

if __name__ == "__main__":
    app.run()
