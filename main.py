# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main package for URL routing and the index page."""

__author__ = 'Sean Lip'

import logging
import os
import sys

import webapp2

from controllers import base
from controllers import editor
from controllers import gallery
from controllers import pages
from controllers import reader
from controllers import resources
from controllers import stats
from controllers import widgets
import feconf

# Import the sympy library.
if 'third_party/sympy-0.7.2/sympy-0.7.2' not in sys.path:
    sys.path.insert(0, os.path.join(
        os.getcwd(), 'third_party/sympy-0.7.2/sympy-0.7.2'))


class Error404Handler(base.BaseHandler):
    """Handles 404 errors."""

    def get(self):
        """Redirects users to the main gallery if an invalid URL is entered."""

        logging.error('Invalid URL requested: %s', self.request.uri)
        self.redirect('/gallery')


# Regex for base64 id encoding
r = '[A-Za-z0-9=_-]+'

# Register the URL with the responsible classes
urls = [
    (r'/?', pages.MainPage),
    (r'/about/?', pages.AboutPage),
    (r'/terms/?', pages.TermsPage),

    (r'/lib/(%s)/?' % r, resources.LibHandler),
    (r'/templates/(%s)/?' % r, resources.TemplateHandler),
    (r'/imagehandler/?', resources.ImageHandler),
    (r'/imagehandler/(%s)/?' % r, resources.ImageHandler),

    (r'/gallery/?', gallery.GalleryPage),
    (r'/gallery/data/?', gallery.GalleryHandler),

    (r'/learn/(%s)/?' % r, reader.ExplorationPage),
    (r'/learn/(%s)/data/?' % r, reader.ExplorationHandler),
    # TODO(sll): there is a potential collision here if the state_id is 'data'.
    (r'/learn/(%s)/(%s)/?' % (r, r), reader.ExplorationHandler),
    (r'/learn_random/?', reader.RandomExplorationPage),

    (r'/create_new/?', editor.NewExploration),
    (r'/fork/?', editor.ForkExploration),
    (r'/create/download/(%s)/?' % r, editor.ExplorationDownloadHandler),
    (r'/create/(%s)/?' % r, editor.ExplorationPage),
    (r'/create/(%s)/data/?' % r, editor.ExplorationHandler),
    # TODO(sll): there is a potential collision here if the state_id is 'data'.
    (r'/create/(%s)/(%s)/data/?' % (r, r), editor.StateHandler),

    (r'/widgetrepository/?', widgets.WidgetRepositoryPage),
    (r'/widgetrepository/data/?', widgets.WidgetRepositoryHandler),
    (r'/interactive_widgets/(%s)/?' % r, widgets.InteractiveWidgetHandler),

    (r'/stats/(%s)/?' % r, stats.StatsHandler),

    # 404 error handler.
    (r'/.*', Error404Handler),
]

app = webapp2.WSGIApplication(urls, debug=feconf.DEBUG)
