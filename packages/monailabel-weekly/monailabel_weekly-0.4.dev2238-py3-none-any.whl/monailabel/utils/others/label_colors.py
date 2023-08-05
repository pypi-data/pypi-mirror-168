# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from typing import Any, Dict

label_color_map: Dict[str, Any] = dict()


def get_color(label, color_map):
    color = color_map.get(label) if color_map else None
    color = color if color else color_map.get(label.lower()) if color_map and isinstance(label, str) else None
    color = label_color_map.get(label) if not color else color
    if color is None:
        color = [random.randint(0, 255) for _ in range(3)]
        label_color_map[label] = color
    return color


def to_hex(color):
    return "#%02x%02x%02x" % tuple(color) if color else "#000000"


def to_rgb(color):
    return "rgb(" + ",".join([str(x) for x in color]) + ")" if color else "rgb(0,0,0)"
