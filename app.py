#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

#import PIL
# PIL import Image
# PIL import ImageFont
#from PIL import ImageDraw

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    #baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    #numindex= makeimage(1)
    #if yql_query is None:
        #return {}
    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    #result = urlopen(yql_url).read()
    #result = yql_query //////////////
    #data = json.loads(result)/////////
    #res = makeWebhookResult(data)
    res = makeWebhookResult(yql_query)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    #city = parameters.get("geo-city")
    age = parameters.get("number")
    #if city is None:
        #return None
    age = int(age)
    age -= 8
    age = str(age)
    #return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
    return age

def makeWebhookResult(data):
    #query = data.get('query')
    #if query is None:
       # return {}

    #result = query.get('results')
    #if result is None:
        #return {}

    #channel = result.get('channel')
    #if channel is None:
        #return {}

    #item = channel.get('item')
    #location = channel.get('location')
    #units = channel.get('units')
    #if (location is None) or (item is None) or (units is None):
       # return {}

    #condition = item.get('condition')
    #if condition is None:
        #return {}

    # print(json.dumps(item, indent=4))

    #speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             #", the temperature is " + condition.get('temp') + " " + units.get('temperature')
    speech = "Your are "+data+" years old, my friend. Thank you for playing. What's in your mind now?"
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeimage(numindex):
    font = ImageFont.truetype("adventpro-regular.ttf", 25)
    img = Image.new("RGBA", (200,200), (120,20,20))
    draw = ImageDraw.Draw(img)
    draw.text((0,0), "This is a test", (255,255,0), font=font)
    draw = ImageDraw.Draw(img)
    img.save("a_test.png")
    return numindex

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
