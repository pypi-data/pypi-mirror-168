#!/usr/bin/env python3
import csv
import json
import os
import pathlib
import re
import sys
from argparse import ArgumentParser
from typing import Optional, Iterable, List, Dict


class Config:
    """
    Initilization example:

        >>> from loadconf import Config
        >>> c = Config("my_program")
        >>> c._program
        'my_program'
        >>> c._platform
        'linux'
        >>> print(c.config_dir)
        None
        >>> print(c.files)
        None
    """

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

    def create_files(
        self,
        create_files: List,
    ):
        """
        Example usage:

            >>> file_list = ["conf", "/path/to/file/to/create.txt"]
            >>> c.create_files(file_list)

        Test if config files exist and create them if needed.
        """
        if self.config_dir is not None:
            dir = pathlib.Path(self.config_dir)
            if not dir.is_dir():
                dir.mkdir(parents=True, exist_ok=True)
        files = []
        for file in create_files:
            if file in self.defined_files.keys():
                files.append(self.defined_files[file])
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
        Example usage:

            >>> user_files = { "conf": "my_program.conf" }
            >>> c.define_files(user_files)
            >>> c.conf
            '/home/user/.config/my_program/my_program.conf'     # on Linux
            '/home/user/Library/Preferences/my_program.conf'    # on MacOS
            'C:\\Users\\user\\AppData\\Local\\my_program.conf'  # on Windows
            >>> c.defined_files # on Linux
            {'conf': '/home/user/.config/my_program/my_program.conf'}

        Why you might use this:

        - Finds where config files should get installed by default
        - Gives a quick way to access a file by it's key
        - Allows for access via keys when calling other methods like:
            - create_files()
            - read_conf()
            - store_files()
        """
        self.config_dir = None
        path = ""
        # If program wants to use it's own dir then ensure it exists
        if config_dir is not None and os.path.isdir(config_dir):
            self.config_dir = config_dir
        # Else define the locations where config files should be stored
        elif self._platform == "linux":
            path = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        elif self._platform == "macos":
            path = os.path.expanduser("~/Library/Preferences/")
        else:
            user_name = os.getlogin()
            path = f"C:\\Users\\{user_name}\\AppData\\Local"
        if not self.config_dir:
            self.config_dir = os.path.join(path, self._program)
        self.defined_files = {}
        for key, value in user_files.items():
            file = os.path.join(self.config_dir, value)
            self.defined_files[key] = file
            setattr(self, key, file)

    def define_settings(
        self,
        settings: Dict,
    ):
        """
        Example usage:

            <<define_files_ex>>

        Users may not provide all settings that are relevant to your program.
        If you want to set some defaults, this makes it easy.
        """
        for key, value in settings.items():
            setattr(self, key, value)

    def read_conf(
        self,
        user_settings: List,
        read_files: List,
        delimiter: str = "=",
        comment_char: str = "#",
    ):
        """
        Example conf file:

            # my_program.conf
            setting_name = setting value
            fav_color = Blue
            int_val = 10
            bool_val = true
            good_line = My value with escaped delimiter \\= good time

        Example usage:

            >>> settings = ["fav_color", "good_line", "int_val", "bool_val"]
            >>> files = ["conf"]
            >>> c.read_conf(settings, files)
            >>> c.good_line
            'My value with escaped delimiter = good time'
            >>> c.fav_color
            'Blue'
            >>> c.bool_val
            True
            >>> c.int_val
            10

        Things to note:

            - read_conf() will make effort to determine int and bool values
              for settings instead of storing everything as a string.
            - If the user has a value that has an unescaped delimiter then csv.Error will
              get raised with a note about the line number that caused the error.
            - The default delimiter is the equal sign "=" but you can set something
              different
            - The default comment character is pound "#" but you can set it to something
              different
            - For users to escape the delimiter character they can use a backslash. That
              backslash will not get included in the stored value.
        """
        files = []
        # File may be an actual file or a key value from defined_files
        for file in read_files:
            if hasattr(self, "defined_files") and file in self.defined_files.keys():
                files.append(self.defined_files[file])
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
                        setattr(self, setting_name, setting_value)

    def store_args(
        self,
        user_args: ArgumentParser,
    ):
        """
        This module aims to make cli style packages more flexible. As a convenience,
        you can store an ~ArgumentParser~ object under ~c.args~.
        """
        self.args = user_args

    def store_files(
        self,
        files: Iterable,
        dict_name: str = "stored",
        json_file: bool = False,
    ):
        """
        Example usage:

            <<store_files_ex>>

        The purpose of this method is to allow you to store each line of a file in a
        list accessible through c.stored["key"]. Why might you want this? Instead of
        forcing a brittle syntax on the user you can give them an entire file to work
        with. If a variable is useful as a list then this gives users an easy way to
        define that list.

        If you've run c.define_files() then you can give c.store_files() a list of
        keys that correspond to a defined file. If you haven't defined any files then
        you can give a dict of files to store and a key to store them under.

        Storing json data can be nice too though:

            <<store_json_ex>>
        """
        # Temp dict to store at self.dict_name
        temp_dict = {}
        # Check if user gave a dict
        if isinstance(files, dict):
            read_dict = files
            read_files = files.values()
        # If user didn't give a dict ensure they have run define_files()
        elif hasattr(self, "defined_files"):
            read_dict = self.defined_files
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
                with open(file, "r") as data:
                    jdata = json.load(data)
                setattr(self, key, jdata)
                temp_dict[key] = jdata
            else:
                with open(file) as f:
                    temp_dict[key] = []
                    for line in f:
                        temp_dict[key].append(line.rstrip())
        setattr(self, dict_name, temp_dict)
