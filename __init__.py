# -*- coding: utf-8 -*-

"""Interact with your local Hoogle server.

Search for type definitons and function names. Hold `alt` to bring up a list of
the different modules that function appears in and use the arrow keys to select
the documentation you would like to view.

Synopsis: <trigger> <query>"""

from albert import *
import os
from time import sleep
import time
import json
from urllib import request, parse
from collections import defaultdict


__title__ = "Hoogle"
__version__ = "0.0.1"
__triggers__ = "ho"
__authors__ = "cdaloisio"

iconPath = os.path.dirname(__file__) + "/plugin.svg"
baseUrl = "http://localhost:8080"
limit = 50

# Can be omitted
def initialize():
    pass


# Can be omitted
def finalize():
    pass


def handleQuery(query):
     if query.isTriggered:
        query.disableSort()

        # don't spam the server
        time.sleep(0.1)
        if not query.isValid:
            return

        stripped = query.string.strip()

        if stripped:
            results = []

            params = {
                'mode': 'json',
                'count': limit,
                'hoogle': stripped
            }
            get_url = "%s?%s" % (baseUrl, parse.urlencode(params))
            req = request.Request(get_url)

            with request.urlopen(req) as response:
                objects = json.loads(response.read())

                groupedResults = defaultdict(list)
                for object in objects:
                    key = object['item']
                    groupedResults[key].append(object)

                for k, v in groupedResults.items():
                    title = k
                    summary = v[0]['docs'][0:100] + "..."
                    urlActions = []
                    for item in v:
                        url = item['url']
                        mod = item['module']
                        desc = mod.get('name', "")
                        action = UrlAction(desc, url)
                        urlActions.append(action)

                    results.append(Item(id=__title__,
                                        icon=iconPath,
                                        text=title,
                                        subtext=summary,
                                        completion=title,
                                        actions=urlActions))

            return results
        else:
            return Item(id=__title__,
                        icon=iconPath,
                        text=__title__,
                        subtext="Enter a query to search Hoogle")
