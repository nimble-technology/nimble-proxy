# The MIT License (MIT)
# Copyright © 2023 Nimble Labs LTD

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import re
import os
import codecs
from os import path
from io import open
from setuptools import setup, find_packages
from pkg_resources import parse_requirements


def read_requirements(path):
    with open(path, "r") as f:
        requirements = f.read().splitlines()
        processed_requirements = []
        for req in requirements:
            if req.startswith("git+") or "@" in req:
                if "egg=" in req:
                    pkg_name = re.search(r"egg=([a-zA-Z0-9_-]+)", req.strip())
                    if pkg_name:
                        pkg_name = pkg_name.group(1)
                        processed_requirements.append(
                            pkg_name + " @ " + req.strip()
                        )
                else:
                    pkg_name = re.search(r"/([a-zA-Z0-9_-]+)(\.git)?(@|$)", req)
                    if pkg_name:
                        pkg_name = pkg_name.group(1)
                        processed_requirements.append(
                            pkg_name + " @ " + req.strip()
                        )
            else:
                processed_requirements.append(req)
        return processed_requirements


requirements = read_requirements("requirements.txt")
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# loading version from setup.py
with codecs.open(
    os.path.join(here, "src/nimproxy/__init__.py"), encoding="utf-8"
) as init_file:
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M
    )
    version_string = version_match.group(1)

setup(
    # package names and code path config
    name="nimproxy",
    packages=['nimproxy'],
    package_dir={'':'src'},
    # metadata like version etc.
    description="Nimble proxy",
    author="nimble.technology",
    include_package_data=True,
    license="MIT",
    python_requires=">=3.9",
    install_requires=requirements,
)
