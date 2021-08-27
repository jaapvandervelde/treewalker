from re import match
from sys import version_info
if version_info[0] == 3 and version_info[1] <= 4:
    from scandir import scandir
else:
    from os import scandir
from platform import node
from sqlite3 import connect
from logging import info, basicConfig, INFO, error
from pathlib import Path
from conffu import Config


# noinspection SqlResolve
class TreeWalker:
    lines = 0
    node = node()

    @classmethod
    def rewrite_path(cls, p, rewrite_admin=True):
        p = str(Path(p).resolve())
        return r'\\{}\{}$\{}'.format(cls.node, p[0].lower(), p[2:]) \
            if rewrite_admin and len(p) > 1 and p[1] == ':' else p

    def __init__(self, fn, overwrite=True):
        self._conn = connect(fn)
        self.c = self._conn.cursor()

        # always drop no_access, will only ever contain data about last run
        self.c.execute('DROP TABLE IF EXISTS no_access')
        self.c.execute('CREATE TABLE no_access (id int, parent_dir int, name text, problem int)')

        if overwrite:
            self.c.execute('DROP TABLE IF EXISTS dirs')
            self.c.execute('CREATE TABLE dirs (id int, parent_dir int, name text, size int, total_file_count int, '
                           'file_count int, min_mtime int, min_atime int)')
            self.c.execute('DROP TABLE IF EXISTS files')
            self.c.execute('CREATE TABLE files (parent_dir int, name text, size int, mtime int, atime int)')
            self.next_dir_id = 0
        else:
            self.c.execute('SELECT MAX(id) FROM dirs')
            x = self.c.fetchone()[0]
            self.next_dir_id = 0 if x is None else x

    def log_1k(self, *args):
        if self.lines % 1000 == 0:
            info(*args)
        self.lines += 1

    def walk(self, path, parent_dir=-1, top_match='.*'):
        dir_id = self.next_dir_id
        self.next_dir_id += 1
        self.log_1k('Processing {}, {}'.format(path, dir_id))
        total_size, min_mtime, min_atime, total_count, count, size = 0, 10000000000, 10000000000, 0, 0, 0
        try:
            for entry in scandir(path):
                # inspection required due to PyCharm issue PY-46041
                # noinspection PyUnresolvedReferences
                if parent_dir > -1 or match(top_match, entry.name):
                    # noinspection PyUnresolvedReferences
                    if entry.is_dir(follow_symlinks=False):
                        # noinspection PyUnresolvedReferences
                        size, sub_count, mtime, atime = self.walk(entry.path, dir_id)
                        total_count += sub_count
                    else:
                        # noinspection PyUnresolvedReferences
                        stat = entry.stat(follow_symlinks=False)
                        size = stat.st_size
                        mtime = int(stat.st_mtime)
                        atime = int(stat.st_atime)
                        total_count += 1
                        count += 1
                        # noinspection PyUnresolvedReferences
                        self.c.execute('INSERT INTO files VALUES(?, ?, ?, ?, ?)',
                                       [dir_id, entry.name, size, mtime, atime])
                    total_size += size
                    min_mtime = min(min_mtime, mtime)
                    min_atime = min(min_atime, atime)
        except PermissionError:
            print('Permission error trying to process: {}'.format(path))
            self.c.execute('INSERT INTO no_access VALUES(?, ?, ?, 0)',
                           [dir_id, parent_dir, path])
        except FileNotFoundError:
            print('File not found error trying to process: {}'.format(path))
            self.c.execute('INSERT INTO no_access VALUES(?, ?, ?, 1)',
                           [dir_id, parent_dir, path])

        self.c.execute('INSERT INTO dirs VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                       [dir_id, parent_dir, path, total_size, total_count, count, min_mtime, min_atime])
        return total_size, total_count, min_mtime, min_atime

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    def commit(self):
        self.c.execute('COMMIT')

    def close(self):
        self._conn.close()

    def add_db(self, fn):
        def do_add(dir_id, parent_dir):
            nonlocal ca
            ca.execute('SELECT * FROM dirs WHERE id = ?', [dir_id])
            self.c.execute('INSERT INTO dirs VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                           (self.next_dir_id, parent_dir) + ca.fetchone()[2:])
            ca.execute('SELECT * FROM files WHERE parent_dir = ?', [dir_id])
            for f in ca.fetchall():
                self.c.execute('INSERT INTO files VALUES(?, ?, ?, ?, ?)',
                               (self.next_dir_id,) + f[1:])
            ca.execute('SELECT id FROM dirs WHERE parent_dir = ?', [dir_id])
            new_dir_id = self.next_dir_id
            self.next_dir_id += 1
            for d in ca.fetchall():
                do_add(d[0], new_dir_id)

        conn_add = connect(fn)
        try:
            ca = conn_add.cursor()
            ca.execute('SELECT name, id FROM dirs WHERE parent_dir = -1')
            for r in ca.fetchall():
                self.remove(r[0])
                do_add(r[1], -1)
        finally:
            conn_add.close()

    def remove(self, p):
        def do_remove(dir_id):
            self.c.execute('SELECT id FROM dirs WHERE parent_dir = ?', [dir_id])
            children = self.c.fetchall()
            for c in children:
                do_remove(c[0])
            self.c.execute('DELETE FROM files WHERE parent_dir = ?', [dir_id])
            self.c.execute('DELETE FROM dirs WHERE id = ?', [dir_id])

        self.c.execute('SELECT name, id FROM dirs WHERE parent_dir = -1')
        for r in self.c.fetchall():
            if Path(r[0]).is_relative_to(p):
                do_remove(r[1])
            elif Path(p).is_relative_to(r[0]):
                self.c.execute('SELECT id FROM dirs WHERE name = ?', [p])
                _id = self.c.fetchone()[0]
                if _id is None:
                    error('Attempt to remove "{p}", not in database')
                    exit(3)
                do_remove(_id)

    def get_tree(self, p=None, d=None):
        if d is None:
            if p is None:
                self.c.execute('SELECT name, id FROM dirs WHERE parent_dir = -1')
                return {r[0]: self.get_tree(d=r[1]) for r in self.c.fetchall()}
            self.c.execute('SELECT id FROM dirs WHERE name = ?', [p])
            d = self.c.fetchone()[0]
        if d is None:
            return False
        self.c.execute('SELECT name, id FROM dirs WHERE parent_dir = ?', [d])
        result = {Path(r[0]).name: self.get_tree(d=r[1]) for r in self.c.fetchall()}
        self.c.execute('SELECT name FROM files WHERE parent_dir = ?', [d])
        return result | {r[0]: None for r in self.c.fetchall()}


def cli_entry_point():
    main()


def print_help():
    print(
        'Treewalker traverses a directory tree from a starting path, adding files and folders to a SQLite3 database.\n'
        '\n'
        'Usage: `treewalker [options] --output filename --path path(s) | --merge filename\n'
        '\n'
        'Options:\n'
        '-h/--help                     : This text.\n'
        '-o/--output filename          : Filename for the SQLite3 database to write to. (required)\n'
        '-p/--path path [path [..]]    : Path(s) to `walk` and add to the database.\n'
        '-m/--merge filename           : Filename of a 2nd database to merge into output.\n'
        '-rm/--remove path [path [..]] : Path(s) to recursively remove from the database.\n'
        '                                (--path, --merge or --remove required)\n'
        '-ow/--overwrite               : Overwrite (wipe) the output database (or to add to it). (default False)\n'
        '-rw/--rewrite                 : Rewrite paths to resolved paths. (default True, set to False or 0 to change)\n'
        '-ra/--rewrite_admin           : Rewrite local drive letters to administrative shares. (default True)\n'
        '-t/--top_match                : Regular expression to match items in the path(s) root to. (deprecated)\n'
        '\n'
        'Examples:\n'
        '\n'
        'Create a new database with the structure and contents of two temp directories:\n'
        '   treewalker --overwrite --output temp_files.sqlite --path c:/temp d:/temp e:/temp\n'
        'Remove a subset of files already in a database:\n'
        '   treewalker --remove d:/temp/secret --output temp_files.sqlite\n'
        'Add previously generated files to the database:\n'
        '   treewalker --merge other_tmp_files.sqlite --output temp_files.sqlite\n'
        'Run treewalker with options from a .json configuration file:\n'
        '   treewalker -cfg options.json\n'
    )


def main():
    basicConfig(level=INFO)

    cfg = Config.from_file(require_file=False).update_from_arguments(
        aliases={'o': 'output', 'p': 'path', 'm': 'merge',
                 'ow': 'overwrite', 'rm': 'remove', 'h': 'help', '?': 'help',
                 'rw': 'rewrite', 'ra': 'rewrite_admin', 't': 'top_match'})

    if cfg.get('help', False):
        print_help()
        exit(0)

    overwrite = cfg.get('overwrite', False)
    remove = cfg.get('remove', False)

    if 'path' not in cfg:
        if 'merge' not in cfg:
            error('Provide "path" or "merge" in configuration file, or on the command line as "--path <some folder>"')
            print_help()
            exit(1)
        fn = cfg.merge
        if not Path(fn).is_file():
            error('File to merge not found: {}'.format(fn))
            exit(2)
        info('Merging "{}" into "{}" (not processing further options)'.format(cfg.merge, cfg.output))
        with TreeWalker(cfg.output, overwrite=overwrite) as tree_walker:
            tree_walker.add_db(cfg.get('merge'))
        exit(0)
    if 'output' not in cfg:
        error('Provide "output" in configuration file, or on the command line as "--output <some filename>"')
        print_help()
        exit(1)

    info('Writing tree info for "{}" to "{}"'.format(cfg.path, cfg.output))

    with TreeWalker(cfg.output, overwrite=overwrite) as tree_walker:
        if not isinstance(cfg.path, list):
            cfg.path = [cfg.path]
        for path in cfg.path:
            if cfg.get('rewrite', True):
                path = tree_walker.rewrite_path(path, cfg.get('rewrite_admin', True))
            tree_walker.remove(path)
            # if not just removing
            if not remove:
                tree_walker.walk(path, top_match=cfg.get('top_match', '.*'))


if __name__ == '__main__':
    main()
