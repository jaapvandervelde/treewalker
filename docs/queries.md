## Running Queries

There is an [explanation of the commandline options for running queries](../configuration/#queries) in the Configuration and CLI section. This section goes into a bit more detail on how to construct queries and how to get the most out of the file system database.

### CLI Queries

#### Some examples

A few examples to serve as a recap of what's possible:

To list all files in a database that are in a folder with `'python'` in the path, formatted as JSON. 
```commandline
treewalker -db files.sqlite -qf "in python" -qo json
```

To list the 10 largest directories with `'temp'` in their path:
```commandline
treewalker -db files.sqlite -qd temp -ql 10
```
!!! note
    for a query like this, selecting the largest folders, it's likely that data is counted twice. For example, say you have a very large folder `C:\Temp`, and inside it is a very large folder `C:\Temp\Disk Images` - if the latter is one of the largest folders on your disk, then `C:\Temp` will obviously be as large, but perhaps only a little bit larger if there's not a lot more in it. As a result, both might show up in the top 10. The `size` for a directory in a Treewalker file system database includes the size of all its subdirectories.

To run any SQL query directly from the command line, for example to find the total size of files in `__pycache__` folders:
```commandline
treewalker -db files.sqlite -qc "SELECT SUM(files.size) AS nice_sum FROM files JOIN dirs ON files.parent_dir = dirs.id WHERE dirs.name LIKE '%\__pycache__'"  
```
!!! note
    The SQLite dialect allows either single or double quotes around strings, which is convenient on the command line as you need to enclose the query in double quotes. You could of course still escape double quotes by doubling them, as for any command in the shell. However, for more complicated queries, it is probably better to save the query as a file like `query.sql` anyway and run it with `treewalker -db files.sqlite -qs query.sql`

#### Formatting sizes in output

Any field named `nice_<something>` will be passed to `nice_size()` before getting written to output. The default queries (`-qf` for files and `-qd` for directories don't include those) but this example does:
```commandline
treewalker -db files.sqlite -qc "SELECT size AS nice_size, * FROM files WHERE name LIKE '%.py'" -ql 20 -qn si 3
```
It lists all the fields for Python source files in the database, preceded by the size field renamed as `nice_size`. In the output, lines will look like this:
```none
3.100 kB,17231,prime.py,3100,1640784890,1640827083
49.791 kB,17242,_config.py,49791,1630049071,1630049071
24 B,17242,_version.py,24,1630049071,1630049071
```

#### Integration with other shell programs

To integrate `treewalker` with other shell programs, picking `csv` or `json` as the `query_output` format is probably most suitable. You can then pipe the text output into other command line applications. 

For example, on a Windows PowerShell command line:
```powershell
PS C:\Users\user> treewalker -db files.sqlite -qc "SELECT * FROM files WHERE name LIKE '%.py'" -ql 3 -qo json | ConvertFrom-Json | Select-Object -Property size, name

size name
---- ----
 557 DialogBox.py
1311 example.py
1433 file_manager.py
```

Similarly, on a Linux command line (with `jq` installed):
```shell
[root@MACHINE grismar] treewalker -db files.sqlite -qc "SELECT * FROM files WHERE name LIKE '%.py'" -ql 3 -qo json | jq .size,.name
557
"DialogBox.py"
1311
"example.py"
1433
"file_manager.py"
```

If you're integrating with programs where you need the output in a file, `treewalker` currently doesn't have options for output directly to file, but of course you can just redirect the output of the command to file:
```commandline
C:\Users\user> treewalker -db files.sqlite -qc "SELECT * FROM files WHERE name LIKE '%.py'" -ql 3 -qo csv > top3.csv
```

#### Integration with Python scripts

If you're looking to use the output from Treewalker directly in a Python script, you could use the above method and capture the standard out from an external process (using `Popen` or something of the sort). But a far simpler solution would be to access the SQLite database directly from your script, and use the TreeWalker object if you want to perform other operations:
```python
from treewalker import TreeWalker

tw = TreeWalker('files.sqlite')
tw.walk(r'C:\Temp')
```
The `treewalker.py` source code itself provides ample examples of how to use the class - keep in mind that Treewalker was written primarily as a commandline utility. The class does all the work, but hasn't been optimised for user-friendliness from a developer's point of view. Future versions *may* include a shell class that accepts configuration similar to the shell script.

One feature of the current Python class however is the possibility to pass a callback to the `.walk()` method, which allows you to exclude files and directories on whatever criterium you like. 

For example, say you want to exclude any folder that contains a file called `.ignore`:
```python
from treewalker import TreeWalker
from pathlib import Path


def check_ignore(p):
    return p.is_file() or not (Path(p) / '.ignore').is_file()


tw = TreeWalker('files.sqlite')
tw.walk(r'C:\Temp')
```
The callback returns `True` when passed a filename, or when passed a directory name of a directory that does not contain a `.ignore` file - that's all that's needed.

!!! note 
    Some options can be set on the `TreeWalker()` constructor, including `override` which would allow running mixed [rewrite](../configuration/#rewrite) and [rewrite_admin](../configuration/#rewrite) walks - this is not recommended, but mentioned here because it is the only way to do so. Without `override` set to `True` (which is impossible from the commandline), mixing these modes will cause an error. 

Accessing the SQLite database is straightforward:
```python
from sqlite3 import connect, Row

conn = connect(r'C:\Users\grism\files.sqlite')
conn.row_factory = Row
c = conn.execute('SELECT * FROM files WHERE name LIKE "%.py"')

for row in c.fetchall():
    print(row['name'])
```

As long as you are familiar with the standard `sqlite3` module, and know what the structure of the underlying SQLite database is, this should be self-explanatory.

If you need to run many SQLite queries against a database, or want to explore the database contents, the free and open source (GPL) SQLiteStudio is recommended, available from https://sqlitestudio.pl/ (no affiliation).

### SQLite database structure

The Treewalker SQLite database consists of the following tables and fields:

- `dirs`<br/>Contains metadata of directories found during a walk. 
    - `id`<br/>a unique identifier, effectively the primary key for the `dirs` table (although no primary key is defined)
    - `parent_dir`<br/>a reference to `dirs.id` of another, existing record in `dirs`
    - `name`<br/>the full path of the directory
    - `size`<br/>the size of the directory and all its contents (including subdirectories)
    - `total_file_count`<br/>the number of files in the directory and all its subdirectories
    - `file_count`<br/>the number of files in this directory alone
    - `min_mtime`<br/>the minimum last (stat) modification time of files in the directory and all its subdirectories
    - `min_atime`<br/>the minimum last (stat) access time of files in the directory and all its subdirectories

- `files`<br/>Contains metadata of files found during a walk.
    - `parent_dir`<br/>a reference to `dirs.id` of an existing record in `dirs`
    - `name`<br/>the name of the file
    - `size`<br/>the size of the file
    - `mtime`<br/>the last (stat) modification time of the file
    - `atime`<br/>the last (stat) access time of the file

- `no_access`<br/>Contains metadata of objects that could not be accessed during a walk
    - `id`<br/>a unique identifier (mutually exclusive with `dirs` records), if it's a directory
    - `parent_dir`<br/>a reference to `dirs.id` of an existing record in `dirs`
    - `name`<br/>the name or path of of the object
    - `problem`<br/>the text of an error message, hopefully indicating why the object could not be accessed

- `options`<br/>Treewalker retains the value of options [rewrite](../configuration/#rewrite) and [rewrite_admin](../configuration/#rewrite_admin)
    - `name`<br/>the name of the option
    - `value`<br/>the value of the option for this database

- `runs`<br/>Contains metadata of a walk
    - `root`<br/>the root folder of the walk
    - `start`<br/>when the walk was started (UTC)
    - `end`<br/>when the walk ended (UTC)

The values in the `options` table are only checked at startup. The values in the `runs` table are never checked or used, and serve only as a log of walks added to the database. However, this can be very useful when trying to analyse the currency and consistency of the data in the database.

All tables are included in a merge, except options - which are currently also not checked before a merge. The merged database retains the options it had previously.