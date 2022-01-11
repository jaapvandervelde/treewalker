## Getting started

Although you don't need to know any Python to use Treewalker, you do need Python installed. Also, `pip` is recommended for installing Treewalker and keeping it up to date. Standard installations of Python include `pip`.

### Installation

It is strongly recommended you install Treewalker in its own virtual environment, or an environment that you reserve for system-wide commandline tools, but outside of environments you need for development that don't rely on Treewalker. If you do create a separate virtual environment, remember that it will need to be (re)activated prior to using Treewalker. 

You can install Treewalker from PyPI using `pip` like this:
```commandline
python -m pip install treewalker
```

If you already have Treewalker installed and just need the latest version:
```commandline
python -m pip install treewalker --upgrade
```

To uninstall:
```commandline
python -m pip uninstall treewalker
```

However, note that (as with any Python package installed in this way) this will only uninstall Treewalker itself. Any dependencies that were downloaded and installed will remain. If you created a separate virtual environment for Treewalker, you can simply remove the created virtual environment directory entirely.

After installation, you can check that treewalker runs with:
```commandline
treewalker --help
```

### Creating a file system database

For a first try, it is recommended you create a Treewalker database of a relatively small folder on your system. For example:
```commandline
treewalker --database test.sqlite --walk C:\Temp
```
This would create a database called `test.sqlite` in the current working directory, unless you specific a specific directory as part of the name. Treewalker will collect all the files and directories in `C:\Temp` (including the contents of all subdirectories) and store records in the database.

If you prefer shorter commands, note that the help (`treewalker -h`) shows the shorthand version of each switch. Also note that you can use either Linux (using `-`) or Windows (using `/`) syntax for switches:
```commandline
treewalker -db C:\Documents\User\test.sqlite /w C:\Temp
```

Note that running the same command again will create an up to date record of the files and folders in the database, but it won't be significantly faster than creating a new one. However, if you add multiple locations to a single database, this can still be very useful:
```commandline
treewalker -db my_files.sqlite -w python/ rust/ 
```
This would add all the files and folders in the folders `python/` and `rust/` to the database. If you would later run:
```commandline
treewalker -db my_files.sqlite -w python/ 
```
Then all the records for files in `python/` folder will be up to date, but the records for files and folders in the `rust/` folder won't be touched. 

### Using a file system database

Once you've created a Treewalker database, you can quickly query it. For example for a list of all the files containing the word `report` in their name:
```commandline
treewalker -db test.sqlite -qf report
```
If there are more than 1,000 records that match, Treewalker will show you the first 1,000.

Similarly, to list all the directories with `temp` in their name:
```commandline
treewalker -db test.sqlite -qd temp
```

And finally, to list all the files with the word `report` in their name, that are in some subfolder of a directory with `temp` in their name:
```commandline
treewalker -db test.sqlite -qf report in temp
```
All three examples order their results by size, with the largest result first. If you want to see fewer results, you can pass the `query_limit`/`ql` option:
```commandline
treewalker -db test.sqlite -qf -ql 10
```
This would show you (up to) the 10 largest files in the database.

### More options

If you need more control over how Treewalker collects data, or you want to combine or manipulate existing databases, look at [Configuration and CLI](../configuration).

If you want to get more specific data from the database, or use the data in your own scripts and applications, read [Running Queries](../queries).
