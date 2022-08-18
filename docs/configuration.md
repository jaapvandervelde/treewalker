## Configuration and CLI

Every option available on the command-line interface can be provided using a configuration file. When an option is both on the command-line and in the configuration, the command-line wins.

### CLI Options

For any option that acts as a simple on/off switch, you can either just specify the option to imply turning it on, or explicitly pass `0` or `false` to turn it off, or `1` or `true` to turn it on. This may be useful if you want to be very clear in a batch file or log about what happens. 

For example, the default is for [overwrite](#overwrite) to be off (`False`) and for [rewrite](#rewrite) to be on (`True`). So, this:
```commandline
treewalker --database files.sqlite --walk C:\Temp --overwrite false --rewrite true
```
Would be the same as:
```commandline
treewalker --database files.sqlite --walk C:\Temp
```

#### help

```commandline
--help | -h
```

Shows a help text for CLIU parameters on the console (including the installed Treewalker version number at the top). You can get more help on query-specific parameters with [query_help](#query_help) 

Example:
```commandline
treewalker --help
```

!!! note
    The same help text is shown if the user makes a mistake in providing command-line options. The difference is that in that case, an non-zero errorlevel will be set and an error message will also be shown at the top.

#### database

```commandline
--database | -db filepath
```

Selects a specific Treewalker database to work on. There is no default value. Note that the path will be relative to the current working directory, unless you provide an absolute path like `C:\Temp` or `/home/user/`.    

!!! note
    With the exception of [help](#help) and [query_help](#query_help), every Treewalker command requires the [database](#database) option, unless you provide a configuration file that specifies it, which amounts to the same.

#### walk

```commandline
--walk | -w path [path [..]]
```

Specifies a path (or several paths) to 'walk', i.e. to traverse all the subdirectories of and add every file and directory found to the database. Prior to 'walking', Treewalker will perform a [remove](#remove) on the same path. This means that after the run, the information for a given path will be entirely up-to-date.

Example:
```commandline
treewalker --database files.sqlite --walk c:\ d:\
```

!!! Note
    Paths will be added in order, so there is no real performance advantage from specifying multiple paths over running Treewalker multiple times.

#### merge

```commandline
--merge | -m filepath [filepath [..]]
```

Specifies other Treewalker databases to be added to the database specified with the [database](#database) option. Every record in the specified databases get added, in the order the databases are specified. If the current database already contained a record for some directory or file, it gets overwritten. Other than that, no existing data gets deleted.

Example:
```commandline
treewalker --database files.sqlite --merge more_files.sqlite and_more.sqlite
```

!!! warning
    In specific cases, unless used carefully, this can lead to inconsistent results. For example, if you created a database containing a folder `sub`, which at the time had files `1.txt` and `2.txt` in it. But later on, `2.txt` was deleted, `3.txt` was created and then a new database containing `sub` was created. This new database would contain no record of `2.txt`, while the original database would contain no record of `3.txt`. However, if you merge the new database into the old one, the resulting database will show all three files in `sub`, even though there was no point in time at which all three files existed there. 

    This may be confusing to a user who expects similar behaviour to running `walk` again, which would update the folder to the current state, instead of merging the current situation into the earlier state. 

!!! warning
    (to developers:) To make the merge possible, the unique identifiers of files and folders in the databases being merged into the target database may be updated, to avoid conflicts. This is important to note if you access the database from other software and create relationships using those identifiers. There are currently no outputs available that provide information about the mapping from old to new identifiers.

#### remove

```commandline
--remove | -rm path [path [..]]
```

Specifies a path (or paths) be removed from the database specified with the [database](#database) option. Each path is assumed to refer to a folder and that folder, including all its contents, will be removed from the database. This is particularly useful if you want to add some large folder, but don't want to keep around specific subfolders, for example a temporary files or cache folder.

Example:
```commandline
treewalker --database files.sqlite --walk projects
treewalker --database files.sqlite --remove projects/_old projects/temp
```

!!! Note
    If you [walk](#walk) some location, then [remove](#remove) some of its subfolders from the database, and then [walk](#walk) the same location again, those subfolders will be added again if they still exists and you will need to remove them again. Treewalker does not *currently* keep track of exclusions.

#### overwrite

```commandline
--overwrite | -ow
```

If you specify this option, an entirely new database will be written instead of adding to the existing database. This option is primarily useful if you would otherwise delete the database file before starting a new walk.

Example:
```commandline
treewalker --database files.sqlite --walk C:\ --overwrite
```

!!! Warning
    Just in case it wasn't clear already: this *erases all the data* that was previously in the database you are overwriting! If you just want to overwrite existing data with new data, you don't have to specify a switch - that is the default behaviour for [walk](#walk).

#### rewrite

```commandline
--rewrite | -rw  False | 0
```

By default, this option is on. It causes every directory path that is written to the database during a walk to be rewritten to a full network path. Mapped drive letters are resolved to their hostname and share, local paths are rewritten to their absolute paths.

The advantage of this is that it does not matter what the working directory is for the database, the paths are all absolute and in principle relative to a specific network host. (see [rewrite_admin](#rewrite_admin) for rewriting local paths to network paths)

However, if you need the paths that are written to remain relative, as they are while running the walk - you can set `--rewrite False`. Keep in mind that if you do, running multiple walks from different locations, or merging other databases can cause issues because relative paths for different locations may overlap.

Example:
```commandline
treewalker --database files.sqlite --walk projects --rewrite False
```
(in this example, paths in all records will start with `projects\some_path\etc.` instead of their absolute path)

!!! tip
    Give it a try by running Treewalker on some existing subfolder and running a query afterward; try `treewalker -db on.sqlite folder --overwrite` and `treewalker -db off.sqlite folder --rewrite_admin False --overwrite` and compare `treewalker -db on.sqlite -qf -ql 10` vs. `treewalker -db off.sqlite -qf -ql 10`

!!! note
    Since mixing walks with `rewrite` both on and off in a single database is likely to lead to very confusing data (either it should all be relative to the same working directory, or it should be absolute), this setting and `rewrite_admin` are both written to the database. Future runs will use that value if none is provided, or cause an error message if they are mixed.

#### rewrite_admin

```commandline
--rewrite_admin | -ra  False | 0
```

Similar to [rewrite](#rewrite), but applying to local paths. By default, any local path will be rewritten to the local administrator's share. For example, a path like `C:\Temp` on a computer with name `computer01` would be rewritten to `\\computer01\c$\Temp`.

The advantage of this is that the database will provide paths that work just as well from another computer on the network, provided they are accessed by a user with administrative privileges. 

However, on some older operating systems, administrative shares will not work. Also, if you need the paths from your database to work for all users, you may not want to use them. In that case you would set `--rewrite_admin False`.

!!! Note
    See [set_host](#set_host) to convert a database written with `--rewrite_admin False` to have a specific hostname later. This can also be useful if you create a database on a computer and then want to set it to a specific other hostname.

Example:
```commandline
treewalker --database files.sqlite --walk C:\Temp --rewrite_admin False
```
(this would write directories as `C:\Temp\etc.` instead of `\\computer01\c$\Temp\etc.`)

!!! tip
    Give it a try by running Treewalker on a small folder and running a query afterward; try `treewalker -db on.sqlite C:\Temp --overwrite` and `treewalker -db off.sqlite C:\Temp --rewrite_admin False --overwrite` and compare `treewalker -db on.sqlite -qf -ql 10` vs. `treewalker -db off.sqlite -qf -ql 10`

#### set_host

```commandline
--set_host | -sh hostname
```

If you write to a database with [rewrite_admin](#rewrite_admin) set to `False`, you can convert the local paths to become relative to administrative shares on a specific host later.

Example:
```commandline
treewalker --database files.sqlite --set_host computer01
```
This would change every local path in `files.sqlite` to become relative to `computer01`, for example `C:\Temp` would be rewritten as `\\computer01\c$\Temp`.

!!! tip
    This option was initially added to allow for conversion of older Treewalker databases, which never wrote paths relative to administrative shares, to be compatible with newer ones. If you have older Treewalker databases, you may want to convert them for that reason. 

#### Queries

The rest of the command-line options are all intended for querying an existing database.

##### query_help

```commandline
--query_help | -qh
```

Shows a help text on the console specific to query command-line parameters for Treewalker.

Example:
```commandline
treewalker --query_help
```

##### query_dir

```commandline
--query_dir | -qd [term [..]] [in [term[..]] [a_asc|a_desc|s_asc|s_desc]
```
Runs a query to list directories in the database. If terms are provided immediately after the option, any directories with any of those terms (logical `OR`) will be included in the results. If you include `in` with some term(s), then only results inside a folder matching any of those terms will be included.

And if you add any of the `a_asc|a_desc|s_asc|s_desc` at the end, the results will be sorted alphabetically (`a_`) or by size of the object (`s_`) in either ascending (`_asc`) or descending (`_desc`) order. The default is `s_desc`.

Example:
```commandline
treewalker -db files.sqlite -qd python in projects work a_asc
```
This will list all folders with a path containing the phrase `'python'` in any folder containing the phrase `projects` or `work` and order the result in ascending alphabetical order.

Example result:
```commandline
C:\Users\user>treewalker -db test.sqlite -qd color test in frame color
nice_size,size,name
20.9 KiB,21378,\\HOST\c$\work\treewalker\Lib\site-packages\pip\_vendor\colorama\__pycache__
20.8 KiB,21330,\\HOST\c$\work\pz\Lib\site-packages\pip\_vendor\colorama\__pycache__
16.8 KiB,17162,\\HOSTL\c$\work\torch_test\Lib\site-packages\torch\utils\data\datapipes\dataframe\__pycache__

Total rows: 3
```

!!! warning
    In the current implementation, note (visible in the example) that the term that applies to the folder doesn't necessarily apply to its name, but to its entire path. As a result, a term that should apply to the directory can appear *before* a term that applies to the folder it is in. E.g. `__pycache__` is in `dataframe`, but matches itself because of `torch_test`, which comes before `dataframe` in its path!

!!! note
    If you need to use characters with special meaning on the command-line, like `-` or `/` denoting a new switch, put the entire value of `-qd` in quotes, for example `treewalker -db files.sqlite -qd "__pycache__ in -python"` for any directory that has `'-python'` in its name.

##### query_file

```commandline
--query_file | -qf [term [..]] [in [term[..]] [a_asc|a_desc|s_asc|s_desc]
```
This command is very similar to [query_dir](#query_dir), except that it won't list directories but files. Terms after `in` will still apply to directories the files should be in.

!!! note
    unlike directories, there is no conflict in the order, as the terms apply to the name of the file, not the full path. 

##### query_limit

```commandline
--query_limit | -ql number_of_records
```
By default, a query will return up to 1,000 results. You can have it more or fewer records by changing this option.

Example:
```commandline
treewalker -db files.sqlite -qf -ql 10
```
This will show the top 10 (or fewer, if there are fewer) largest files in the database.

##### query_nice

```commandline
--query_nice | -qn [bin|si] n
```
By default, when fields in a query are named `nice_<something>`, they will be formatted using `nice_size`, using binary units (KiB, MiB, GiB, etc., powers of 1024) and 1 decimal precision (e.g. `'63.4 MiB'`). You can specify whether binary or SI units (KB, MB, GB, etc., powers of 1000) should be used and what the decimal precision should be.

Example:
```commandline
treewalker -db files.sqlite -qc "SELECT size AS nice_size, * FROM files WHERE name LIKE '%.py'" -ql 20 -qn si 3
```
This will show the top 20 (or fewer, if there are fewer) of the largest Python source files in the database, with a precision of 3 decimals and using SI units (e.g. 66.480 MiB).

##### query_output

```commandline
--query_output | -qo txt|csv|json
```
By default, Treewalker will write the result of a query as .csv records, followed by a message reporting the total number of records - this corresponds to `--query_output txt`. If you specify `csv`, it will omit that messages, writing only a valid .csv (with header). If you specify `json`, the output will be formatted to be syntactically correct JSON.

For example:
```commandline
treewalker -db files.sqlite -qf -qo json
```
This will show the names of all the files in the database, formatted as JSON. Some example output:
```json
{"size": 21378, "name": "\\\\HOST\\c$\\work\\treewalker\\Lib\\site-packages\\pip\\_vendor\\colorama\\__pycache__"}
{"size": 21330, "name": "\\\\HOST\\c$\\work\\pz\\Lib\\site-packages\\pip\\_vendor\\colorama\\__pycache__"}
{"size": 17162, "name": "\\\\HOST\\c$\\work\\torch_test\\Lib\\site-packages\\torch\\utils\\data\\datapipes\\dataframe\\__pycache__"}
```

##### query_cli

```commandline
--query_cli | -qc "<valid SQL query>"
```
You can also just write SQL queries directly on the command-line interface. Of course this requires that you are familar with the (simple) database structure of a Treewalker file system database. 

Example:
```commandline
treewalker -db files.sqlite -qc "SELECT * FROM files WHERE name LIKE '%.py' ORDER BY size DESC" -ql 10
```
This will select the 10 largest Python source files in the database. More examples and more on the structure of the database in [Running Queries](../queries)

##### query_sql

```commandline
--query_sql | -qs filepath
```
Instead of providing the SQL directly on the command-line, you can also save a query in a text file and have Treewalker load and run it. As with `query_cli`, you can provide other regular options.

Example:
```commandline
treewalker -db files.sqlite -qs my_query.sql
```

### Configuration with .json

All the options presented above can also be provided to Treewalker in a configuration file. This file is a conffu configuration file, more about those in the documentation of [conffu](https://pypi.org/project/conffu/) itself.

Example `run_walk.json`:
```json
{
  "database": "C:/Documents/User/files.sqlite",
  "walk": ["C:/", "D:/", "E:/"],
  "remove": ["C:/Temp", "D:/Trash", "E:/Cache", "E:/_old"],
  "rewrite_admin": false,
  "overwrite": true
}
```
Which could be executed with:
```commandline
treewalker -cfg run_walk.json
```

This is particularly convenient if you need to run walks on a schedule, or want the walks to be started by other users  and cannot or do not want to use a batchfile to keep track of all the options. Similarly, if you load Treewalker as a class from a Python script, you can provide a dictionary to configure the `Treewalker` object.
