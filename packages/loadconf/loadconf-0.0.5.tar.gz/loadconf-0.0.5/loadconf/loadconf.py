#!/usr/bin/env python3
# Copyright (C) 2022 John Dovern
#
# This file is part of loadconf <https://codeberg.org/johndovern/loadconf>.
#
# loadconf is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation version 3 of the License
#
# loadconf is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# loadconf.  If not, see <http://www.gnu.org/licenses/>.

import csv
import json
import os
import pathlib
import re
import sys
from argparse import ArgumentParser
from typing import Optional, Iterable, List, Dict


class Config:

    def __init__(
        self,
        program: str,
    ):
        self._program = program
        platform = sys.platform
        linux = ["linux", "linux2"]
        if platform in linux:
            self._platform = "linux"
        elif platform == "darwin":
            self._platform = "macos"
        else:
            self._platform = "windows"
        self.config_dir = None
        self.files = {}
        self.settings = {}
        self.stored = {}

    def create_files(
        self,
        create_files: List,
    ):
        """
        Test if config files exist and create them if needed.
        """
        if self.config_dir is not None:
            dir = pathlib.Path(self.config_dir)
            if not dir.is_dir():
                dir.mkdir(parents=True, exist_ok=True)
        files = []
        for file in create_files:
            if file in self.files.keys():
                files.append(self.files[file])
            elif os.path.isabs(file):
                files.append(file)
        for file in files:
            f = pathlib.Path(file)
            if not f.is_file():
                f.touch()

    def define_files(
        self,
        user_files: Dict,
        config_dir: Optional[str] = None,
    ):
        """
        Define files and automatically find where they should go
        """
        path = ""
        # If program wants to use it's own dir then ensure it exists
        if config_dir is not None and os.path.isdir(config_dir):
            self.config_dir = config_dir
        # Else define the locations where config files should get stored
        elif self._platform == "linux":
            path = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        elif self._platform == "macos":
            path = os.path.expanduser("~/Library/Preferences/")
        else:
            user_name = os.getlogin()
            path = f"C:\\Users\\{user_name}\\AppData\\Local"
        if not self.config_dir:
            self.config_dir = os.path.join(path, self._program)
        for key, value in user_files.items():
            file = os.path.join(self.config_dir, value)
            self.files[key] = file

    def define_settings(
        self,
        settings: Dict,
    ):
        """
        Users may not provide all settings that are relevant to your program.
        If you want to set some defaults, this makes it easy.
        """
        for key, value in settings.items():
            self.settings[key] = value

    def read_conf(
        self,
        user_settings: List,
        read_files: List,
        delimiter: str = "=",
        comment_char: str = "#",
    ):
        """
        Read a config file
        """
        files = []
        # File may be an actual file or a key value from defined_files
        for file in read_files:
            if self.files:
                files.append(self.files[file])
            elif os.path.isfile(file):
                files.append(file)
        # Regex object for subbing delimiter
        r = re.compile(rf"\\{delimiter}")
        # Read the desired files
        for file in files:
            if not os.path.isfile(file):
                continue
            i = 0
            with open(file) as f:
                reader = csv.reader(
                    f,
                    delimiter=delimiter,
                    escapechar="\\",
                    quoting=csv.QUOTE_NONE,
                )
                for row in reader:
                    i += 1
                    # User did not properly escape their file
                    if len(row) > 2:
                        raise csv.Error(f"Too many fields on line {i}: {row}")
                    # Skip settings with no value
                    elif len(row) < 2:
                        continue
                    # Skip comments
                    elif row[0].startswith(comment_char):
                        continue
                    # Strip white space and sub delimiter if needed
                    setting_name = row[0].strip()
                    setting_name = r.sub(delimiter, setting_name)
                    setting_value = row[1].strip()
                    setting_value = r.sub(delimiter, setting_value)
                    # Try turning qualifying strings into bools and ints
                    try:
                        setting_value = eval(setting_value.capitalize())
                    except (NameError, SyntaxError):
                        pass
                    # Ignore user defined settings that program doesn't care about
                    if setting_name in user_settings:
                        self.settings[setting_name] = setting_value

    def store_files(
        self,
        files: Iterable,
        json_file: bool = False,
    ):
        """
        Store an entire file line by line in a list or load a json file.
        """
        # Temp dict to store at self.dict_name
        temp_dict = {}
        # Check if user gave a dict
        if isinstance(files, dict):
            read_dict = files
            read_files = files.values()
        # If user didn't give a dict ensure they have run define_files()
        else:
            read_dict = self.files
            read_files = files
        # User has passed a list that does not have any meaning
        else:
            return
        # Begin reading files that user wants stored
        for key, file in read_dict.items():
            if not os.path.isfile(file):
                continue
            if not key in read_files:
                continue
            if json_file:
                with open(file, 'r') as data:
                    jdata = json.load(data)
                setattr(self, key, jdata)
                temp_dict[key] = jdata
            else:
                with open(file) as f:
                    temp_dict[key] = []
                    for line in f:
                        temp_dict[key].append(line.rstrip())
        self.stored.update(temp_dict)
