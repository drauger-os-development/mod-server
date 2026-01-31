#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  remove_file.py
#
#  Copyright 2026 Thomas Castleman <batcastle@draugeros.org>
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
import os
import subprocess as subproc
import sys
import json


with open("mod_server_settings.json", "r") as file:
    settings = json.load(file)


if len(sys.argv) == 1:
    print("No files passed!")
    sys.exit(1)

files = sys.argv[1:]

for each in files:
    location = f"{settings["base"]}/mods/pool/{each[0]}"
    os.remove(f"{location}/{each}")
    if os.listdir(location) == []:
        os.rmdir(location)

subproc.check_call(["./sign_files.py"])
