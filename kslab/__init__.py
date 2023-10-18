"""
A collection of frequently used tools, for convenience. https://github.com/Kshora/kslab

"""

from .graph_tools import *
from .langmuirprobe import *
from .qms import *
from .spectrum import *
from .raspi import *

__all__ = ["graph_tools", "langmuirprobe", "qms", "spectrum", "raspi"]

# Copyright 2023 Kurokawa
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__version__ = "1.2.5"

"""
    Release notes:
    1.2.5
        - Fixed a bug in the scraping tool
    1.2.4
        - Fixed a bug in the scraping tool
    1.2.3
        - Fixed a bug in the scraping tool
    1.2.2
        - Add Scraping tool
    1.2.1
        - Update a tool below
    1.2.0
        - Add NIST Atomic Spectra visualization tool
    1.1.2
        - Update raspi parser
    1.1.1
        - Updata raspi parser for new data format
    1.1.0
        - Update raspi.py for new data format
    1.0.0
        - Initial release
"""
