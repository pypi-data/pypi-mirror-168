# Copyright 2022 David Harcombe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple
from pprint import pprint
from absl import app
import urllib.request
from contextlib import closing, suppress
from urllib.request import urlopen
import urllib.parse
import json


def main(unused):
  del unused

  Components = namedtuple(
      typename='Components',
      field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
  )

  apis = {}

  url = urllib.parse.urlunparse(
      Components(
          scheme='https',
          netloc='www.googleapis.com',
          query=urllib.parse.urlencode({'fields': 'items.name,items.version',
                                        'preferred': 'true'}),
          path='',
          url='/discovery/v1/apis',
          fragment=None
      )
  )

  r = urllib.request.Request(url)
  with closing(urlopen(r)) as _api_list:
    api_list = json.loads(_api_list.read())
    if items := api_list.get('items', None):
      for api in items:
        apis[api['name'].upper()] = (api['name'], api['version'])

  pprint(apis)


if __name__ == '__main__':
  with suppress(SystemExit):
    app.run(main)
