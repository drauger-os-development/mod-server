#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sign_files.py
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
import json
import hashlib as hash
import subprocess as subproc


with open("mod_server_settings.json", "r") as file:
    settings = json.load(file)

top_level = settings["base"]
files = {}
for each in os.listdir(f"{top_level}/mods/pool"):
    for each1 in os.listdir(f"{top_level}/mods/pool/{each}"):
        path = f"{top_level}/mods/pool/{each}/{each1}"
        with open(path, "rb") as file:
            data = hash.sha3_512(file.read())
        files[path] = data.hexdigest()

output = {"hash_algo": "sha3_512", "files": files}

with open(f"{top_level}/mods/index.json", "w") as file:
    json.dump(output, file, indent=2)

if settings["create_hash_file"]:
    output = bytes(json.dumps(output, indent=2), "utf-8")
    data = hash.sha3_512(output)
    with open(f"{top_level}/mods/index.json.hash", "w") as file:
        file.write(data.hexdigest())

if settings["create_sig_file"]:
    output = subproc.check_output(["gpg", "--detach-sign", f"{top_level}/mods/index.json"], stderr=subproc.STDOUT).decode()
    output = output.split("\n")[0]
    output = output.split(" ")[2][1:-1]
    output = subproc.check_output(["gpg", "--export", "-a", output]).decode()
    with open(f"{top_level}/mods/public.key", "w") as file:
        file.write(output)
