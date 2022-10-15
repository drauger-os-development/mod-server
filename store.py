#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  store.py
#
#  Copyright 2022 Thomas Castleman <contact@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""Explain what this program does here!!!"""
import sys
from flask import Flask, request, redirect, render_template
import urllib3
import json
import multiprocessing
import os
import time


def eprint(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    eprint("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)

APP = Flask(__name__)

# import settings
if not os.path.exists("settings.json"):
    eprint("Settings file not found.")
    sys.exit(2)

with open("settings.json", "r") as file:
    SETTINGS = json.load(file)


# import packages
if not os.path.exists("packages.json"):
    eprint("Package List not found.")
    sys.exit(2)

with open("packages.json", "r") as file:
    PACK = json.load(file)


@APP.route("/")
def root():
    """Handle the root directory"""
    home_page = {"mod_list": f"{ SETTINGS['base_url'] }/mod_list"}
    return home_page


@APP.route("/mod_list")
def list_mods():
    """Provide full mod list"""
    mods = {}
    for each in PACK:
        print(each)
        mods[PACK[each]["Name"]] = f"{ SETTINGS['base_url'] }/mod/{ PACK[each]['Name'] }"
    return mods


@APP.route("/mod/<mod_name>")
def get_mod(mod_name: str):
    """Provide mod data"""
    for each in PACK:
        if PACK[each]["Name"].lower() == mod_name.lower():
            return PACK[each]
    return {"Error": "Mod Not Found"}


# Start in safe debug mode
if __name__ == "__main__":
    APP.run(host="0.0.0.0", debug=False)
