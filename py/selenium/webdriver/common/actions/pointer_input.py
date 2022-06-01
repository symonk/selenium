# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.remote.webelement import WebElement

from .input_device import InputDevice
from .interaction import POINTER
from .interaction import POINTER_KINDS


class PointerInput(InputDevice):

    DEFAULT_MOVE_DURATION = 250

    def __init__(self, kind, name):
        super(PointerInput, self).__init__()
        if kind not in POINTER_KINDS:
            raise InvalidArgumentException("Invalid PointerInput kind '%s'" % kind)
        self.type = POINTER
        self.kind = kind
        self.name = name

    def create_pointer_move(self, duration=DEFAULT_MOVE_DURATION, x=0, y=0, origin=None, **kwargs):
        action = dict(type="pointerMove", duration=duration)
        action["x"] = x
        action["y"] = y
        action.update(**kwargs)
        if isinstance(origin, WebElement):
            action["origin"] = {"element-6066-11e4-a52e-4f735466cecf": origin.id}
        elif origin:
            action["origin"] = origin

        self.add_action(self._convert_keys(action))

    def create_pointer_down(self, **kwargs):
        data = dict(type="pointerDown", duration=0)
        data.update(**kwargs)
        self.add_action(self._convert_keys(data))

    def create_pointer_up(self, button):
        self.add_action({"type": "pointerUp", "duration": 0, "button": button})

    def create_pointer_cancel(self):
        self.add_action({"type": "pointerCancel"})

    def create_pause(self, pause_duration):
        self.add_action({"type": "pause", "duration": int(pause_duration * 1000)})

    def encode(self):
        return {
            "type": self.type,
            "parameters": {"pointerType": self.kind},
            "id": self.name,
            "actions": [acts for acts in self.actions],
        }

    def _convert_keys(self, actions):
        out = {}
        for k in actions.keys():
            if actions[k] is None:
                continue
            if k == "x" or k == "y":
                out[k] = int(actions[k])
                continue
            splits = k.split("_")
            new_key = splits[0] + "".join(v.title() for v in splits[1:])
            out[new_key] = actions[k]
        return out
