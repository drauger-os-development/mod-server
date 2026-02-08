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
import subprocess as subproc

if "--base" in sys.argv:
    try:
        index = sys.argv.index("--base")
        path = sys.argv[index + 1]
    except (IndexError, ValueError):
        print("No path specified with --base")
        sys.exit(1)
else:
    print("Base directory not passed via --base, assuming base directory is current directory.")
    path = "."

if "--key" in sys.argv:
    try:
        index = sys.argv.index("--key")
        key = sys.argv[index + 1]
    except (IndexError, ValueError):
        print("No key specified with --key")
        sys.exit(1)
else:
    print("No key specified. Please specify a key with the --key argument.")
    sys.exit(1)


data = subproc.check_output(["gpg", "--list-keys", "--with-colons"]).decode()
if key not in data:
    print("Key provided is not valid. Please try a new key.")
    sys.exit(1)

try:
    os.mkdir(f"{path}/mods")
except FileExistsError:
    pass

try:
    os.mkdir(f"{path}/mods/pool")
except FileExistsError:
    pass

print("Directory structure successfully created!")

settings = {
        "base": path,
        "create_sig_file": True,
        "create_hash_file": True,
        "key": key
    }

with open("mod_server_settings.json", "w") as file:
    json.dump(settings, file, indent=2)

print("Settings file successfully created!")
