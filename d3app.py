# -*- coding: utf-8 -*-
"""
    This little bit of code powers my d3Sever!!!
"""
import os
import analytics
from flask import Flask, jsonify, render_template, request, abort
from jinja2 import TemplateNotFound
from flask.ext.assets import Environment, Bundle
import logging
import conf.config as config
logger = config.globalLogger(logging.DEBUG)
analytics.init('82cl6i9bo6h4cnptal9b')
from pull_json import writeStations, pullingJson
import random
import json
from pprint import pformat

#instatntiate the web app
app = Flask(__name__)


@app.context_processor
def isItTitan():
    #determines if I am using this on Titan and turns of analytics
    if 'COMPUTERNAME' in os.environ.keys():
        t = os.environ['COMPUTERNAME'] == 'TITAN'
    else:
        t = False
    return dict(Titan=t)

#sets the asset environment to allow for scss compiling :)
app.debug = True

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('stylyn.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)


@app.route('/')
def index():
    #define the route for the index page
    height = random.randint(80, 130)
    width = random.randint(300, 900)
    return render_template('index.html', height=height, width=width)


@app.route('/api_call/<api_name>')
def callCiti(api_name=None):
    """
    define the route for the streaming page
    """
    if api_name == "station":
        global station, count_of_calls
        json_object = pullingJson(api_name)
        station_dict = json.loads(json_object, station)
        station = {g["id"]: g for g in station_dict['features']}
        count_of_calls = 1
    elif api_name == "update":
        json_object = pullingJson(api_name, station)
        count_of_calls += 1
        # logger.info(json_object[:1000])
        station_dict = json.loads(json_object)
        station = {g["id"]: g for g in station_dict['features']}
        # logger.info(str(station)[:1000])
        # station = "Moo Moo is a Moo Moo %s" % count_of_calls
        # logger.info(station)
    return json_object


# @app.route('/api_call/update', methods=['POST', "GET"])
# def updateCiti():
#     """
#     define the route for the streaming page
#     """
#     if request.method == 'POST':
#         try:
#             post_request = request
#             # json_object = pullingJson("update", post_request)
#             logger.info(pformat(post_request))
#             return "something"
#         except Exception as error:
#             logger.exception("Hitting the right place")
#             error_dict = {'error': str(error)}
#             return json.dumps(error_dict)
#     else:
#         return json.dumps("we dont all hit requests here")


@app.route('/data/us-states.json')
def openJson():
    """
    define the route for the json
    """
    with open("data/us-states.json", "r") as open_json:
        json_object = json.load(open_json)
    return jsonify(json_object)


# @app.route('/update')
# def updateCiti():
#     """
#     define the route for the streaming page
#     """
#     json_object = pullingJson("update")
#     return json_object


@app.route('/<page>')
def show(page):
    """
    this nifty code just makes it so routes will be queried based on what
    the user enters in the URI if the page exists it is displayed :)
    """
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)

#this makes the app initiate
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    # PORT = 5000 if len(sys.argv)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    callCiti()
