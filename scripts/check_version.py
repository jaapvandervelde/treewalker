import re
import subprocess
import sys


def get_latest_git_tag():
    try:
        # Get the latest commit that has a tag
        rev = subprocess.check_output(
            ['git', 'rev-list', '--tags', '--max-count=1'],
            text=True
        ).strip()

        # Describe that commit to get the tag
        tag = subprocess.check_output(
            ['git', 'describe', '--tags', rev],
            text=True
        ).strip()

        return tag
    except subprocess.CalledProcessError as e:
        print("Git command failed:", e)
        return None


def get_changelog_version() -> tuple[str, bool]:
    with open('CHANGELOG.md') as f:
        text = f.read()
        xs = re.finditer('\[(.*?)]', text)
        assert next(xs).group(0), '[Unreleased]'
        version = next(xs).group(1)
        return version, (f'[{version}]: /../../../tags/{version}' in text)


def main(arg_version):
    try:
        from treewalker._version import __version__

        if arg_version != __version__:
            print("Version in code does not match stated version: {} != {}".format(__version__, arg_version))
            exit(1)

        try:
            changelog_version, link_found = get_changelog_version()
        except AssertionError:
            print('Changelog expected to start with [Unreleased]')
            exit(1)
        if __version__ != changelog_version:
            print('Code version does not match changelog: {} != {}'.format(__version__, changelog_version))
            exit(1)
        if not link_found:
            print('Changelog version does not have matching link at end of file: [{}]'.format(changelog_version))
            exit(1)

        latest_tag = get_latest_git_tag()
        if latest_tag is None:
            print('No git tag found')
            exit(1)
        if latest_tag == __version__:
            print('Current software version already tagged in Git repo: {}'.format(latest_tag))
            exit(1)
    except (ImportError, AssertionError, IOError) as e:
        print('Something went wrong. {}'.format(e))
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: check_version.py <version>')
        exit(1)
    main(sys.argv[1])
