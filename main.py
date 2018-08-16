#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import random
from google.appengine.api import urlfetch
import urllib

import json
import logging


URL = 'https://www.googleapis.com/customsearch/v1?'
KEY = 'AIzaSyCye1u_1ZCkmzhgR2oo-NyCcIe7SNa74m4'
CX = '004479840736541492748:cdrngnnwyss'


#remember, you can get this by searching for jinja2 google app engine

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SearchItHandler(webapp2.RequestHandler):
    def get(self):
	# todo: add try
	#        query = 'fun brooklyn 2018'
	template = jinja_current_directory.get_template('templates/search-query.html')
	self.response.write(template.render())

    def post(self):
	# todo: add try
        #query = 'fun brooklyn 2018'
        queryit = self.request.get('queryit')

        query_params = {'key': KEY, 'cx': CX, 'q': queryit + " Brooklyn NY" + " 2018 "}
        result = urlfetch.fetch(URL + urllib.urlencode(query_params))
	# if success, i.e http status code 200 means success
        if result.status_code == 200:
            #self.response.write(result.status_code)
            # a = json.load(result.content)
            template = jinja_current_directory.get_template('templates/search-results.html')

            # logging.info(result.content)
            a = json.loads(result.content)
            # logging.info(type(a))
            # self.response.write(a)
            self.response.write(template.render(a))
            # for i in result.content:
            #     self.response.write(i)
        else:
            self.response.status_code = result.status_code

class HelloHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('My response is Goodbye World.')

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_directory.get_template('templates/index.html')
        self.response.write(template.render())

class MenuHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_directory.get_template('templates/menu.html')
        self.response.write(template.render())

class BlogHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_directory.get_template('templates/blog.html')
        self.response.write(template.render())

class ContactHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_directory.get_template('templates/contact.html')
        self.response.write(template.render())


#the route mapping
app = webapp2.WSGIApplication([
    #this line routes the main url ('/')  - also know as
    #the root route - to the Fortune Handler
    ('/', IndexHandler),
    ('/index', IndexHandler),
    ('/menu', MenuHandler),
    ('/blog', BlogHandler),
    ('/contact', ContactHandler),
    ('/searchit',SearchItHandler)
], debug=True)
