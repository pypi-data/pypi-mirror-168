# loadconf

Config files make it easy for users to use your program the way they
want to. With loadconf you can easily give users that power.

## Install

The usual way:

`pip install loadconf`

Requires python3

# Usage

I think this module is best explained through example, so here you go!

## c = Config("my_program")

``` python
>>> from loadconf import Config
>>> c = Config("my_program")
>>> c._program
'my_program'
>>> c._platform
'linux'
```

To initialize the `Config` object you only need to give the name of your
program, or whatever name you like. As you can see there are some
reserved values after initialization.

## c.define_files()

``` python
>>> user_files = { "conf": "my_program.conf" }
>>> c.define_files(user_files)
>>> c.files["conf"]
'/home/user/.config/my_program/my_program.conf'     # on Linux
'/home/user/Library/Preferences/my_program.conf'    # on MacOS
'C:\\Users\\user\\AppData\\Local\\my_program.conf'  # on Windows
>>> c.files # on Linux
{'conf': '/home/user/.config/my_program/my_program.conf'}
```

Why you might use this:

- Finds where config files should get installed by default
- Gives a quick way to access a file by it's key
- Allows for access via keys when calling other methods like:
  - `create_files()`
  - `read_conf()`
  - `store_files()`

## c.create_files()

``` python
>>> file_list = ["conf", "/path/to/file/to/create.txt"]
>>> c.create_files(file_list)
```

If you've run `c.define_files` then you can pass a key that is relevant
to `c.defined_files`. That will create the file value of that key. If an
item in the given list is not a key then it will get created if it is an
absolute file path.

## c.define_settings()

``` python
>>> settings = { "fav_color": "Orange" }
>>> c.define_settings(settings)
>>> c.settings["fav_color"]
'Orange'
```

Users may not provide all settings that are relevant to your program. If
you want to set some defaults, this makes it easy.

## c.read_conf()

Let's assume the config file we are reading looks like this:

``` conf
# my_program.conf
setting_name = setting value
fav_color = Blue
int_val = 10
bool_val = true
good_line = My value with escaped delimiter \= good time
```

To read the file we run this:

``` python
>>> settings = ["fav_color", "good_line", "int_val", "bool_val"]
>>> files = ["conf"]
>>> c.read_conf(settings, files)
>>> c.settings["fav_color"]
'Blue'
>>> c.settings["good_line"]
'My value with escaped delimiter = good time'
>>> c.settings["int_val"]
10
>>> c.settings["bool_val"]
True
```

Things to note:

- `read_conf()` will make effort to determine int and bool values for
  settings instead of storing everything as a string.
- If the user has a value that has an unescaped delimiter then
  `csv.Error` will get raised with a note about the line number that
  caused the error.
- The default delimiter is the equal sign `=` but you can set something
  different
- The default comment character is pound `#` but you can set it to
  something different
- For users to escape the delimiter character they can use a backslash.
  That backslash will not get included in the stored value.

## c.store_files()

``` python
>>> c.store_files({"other": "/path/to/unknown_file.txt"})
>>> c.stored["other"]
['line1', 'line2 with some text', 'line3', 'etc.']
>>> c.store_files(["conf"])
>>> c.stored["conf"]
['conf_line1', 'conf_line2 with some text', 'conf_line3', 'etc.']
```

The purpose of this method is to allow you to store each line of a file
in a list accessible through `c.stored["key"]`. Why might you want this?
Instead of forcing a brittle syntax on the user you can give them an
entire file to work with. If a variable is useful as a list then this
gives users an easy way to define that list.

If you've run `c.define_files()` then you can give `c.store_files()` a
list of keys that correspond to a defined file. If you haven't defined
any files then you can give a dict of files to store and a key to store
them under.

Storing json data can be nice too though:

``` python
>>> c.store_files({"json_file": "/path/to/data.json"}, json_file=True)
>>> c.stored["json_file"]
{'my_json_info': True}
```
