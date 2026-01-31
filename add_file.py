#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  add_file.py
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
import tarfile as tar


with open("mod_server_settings.json", "r") as file:
    settings = json.load(file)


def get_metadata(path: str) -> dict:
    """Get metadata from a local file"""
    with tar.open(path, "r:*") as file:
        data = file.extractfile("meta.json").read()
    output = json.loads(data)
    return output


if len(sys.argv) == 1:
    print("No files passed!")
    sys.exit(1)

files = sys.argv[1:]

for each in files:
    try:
        meta = get_metadata(each)
    except Exception as e:
        print("Not a valid Mod package!")
        print(f"Error: {e}")
        sys.exit(1)
    name = meta["mod_name"]
    version = meta["mod_version"]["version_code"]
    if name[0] not in os.listdir(f"{settings["base"]}/mods/pool"):
        os.mkdir(f"{settings["base"]}/mods/pool/{name[0]}")
    with open(each, "rb") as file1:
        with open(f"{settings["base"]}/mods/pool/{name[0]}/{name}_{version}.mod_pak", "wb") as file2:
            file2.write(file1.read())

subproc.check_call(["./sign_files.py"])
