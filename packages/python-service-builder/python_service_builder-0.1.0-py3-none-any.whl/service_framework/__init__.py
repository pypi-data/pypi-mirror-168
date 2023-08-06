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
import dataclasses
from typing import Any, Callable, Mapping

import dataclasses_json


def lazy_property(f: Callable):
  """Decorator that makes a property lazy-evaluated.

  Args:
    f: the function to convert to a lazy property.
  """
  attr_name = '_lazy_' + f.__name__

  @property
  def _lazy_property(self) -> Any:
    if not hasattr(self, attr_name):
      setattr(self, attr_name, f(self))
    return getattr(self, attr_name)
  return _lazy_property


def metadata(base: Mapping[str, Any], **custom) -> Mapping[str, Any]:
  for key in custom:
    if not custom[key] and key in base:
      del base[key]

    elif custom[key]:
      base.update({key: custom[key]})

  return base


def field(default: Any = None, default_factory: Any = None, **kwargs):
  base = {
      'letter_case': dataclasses_json.LetterCase.CAMEL,
      'exclude': lambda x: not x
  }

  if kwargs:
    exclude = kwargs.get('exclude', lambda x: not x)
  else:
    def exclude(x): return not x

  if default_factory:
    f = dataclasses.field(default_factory=default_factory,
                          metadata=dataclasses_json.config(
                              **metadata(base=base, **kwargs)))
  else:
    f = dataclasses.field(default=default,
                          metadata=dataclasses_json.config(
                              **metadata(base=base, **kwargs)))

  return f
