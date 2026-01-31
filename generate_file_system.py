#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  generate_file_system.py
#
#  Copyright 2025 Thomas Castleman <batcastle@draugeros.org>
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
import sys
import json

if "--base" in sys.argv:
    index = sys.argv.index("--base")
    try:
        path = sys.argv[index + 1]
    except IndexError:
        print("No path specified with --base")
        sys.exit(1)
else:
    path = "."

try:
    os.mkdir(f"{path}/mods")
except FileExistsError:
    pass

try:
    os.mkdir(f"{path}/mods/pool")
except FileExistsError:
    pass

settings = {
        "base": path,
        "create_sig_file": True,
        "create_hash_file": True
    }

with open("mod_server_settings.json", "w") as file:
    json.dump(settings, file, indent=2)
