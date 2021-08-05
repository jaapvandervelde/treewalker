import os
import re
from setuptools import setup

__name__ = 'python_package'

version_fn = os.path.join(__name__, "_version.py")
__version__ = "unknown"
try:
    version_line = open(version_fn, "rt").read()
except EnvironmentError:
    pass  # no version file
else:
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    m = re.search(version_regex, version_line, re.M)
    if m:
        __version__ = m.group(1)
    else:
        print(f'unable to find version in {version_fn}')
        raise RuntimeError(f'If {version_fn} exists, it is required to be well-formed')

with open("README.md", "r") as rm:
    long_description = rm.read()

setup(
    name=__name__,
    packages=['python_package'],
    version=__version__,
    # TODO: update license
    license='',
    # TODO: update description
    description='No description.',
    # long description will be the contents of project/README.md
    long_description=long_description,
    long_description_content_type='text/markdown',
    # TODO: update author
    author='BMT Commercial Australia Pty Ltd, <optional author(s)>',
    # TODO: update email
    author_email='',
    # TODO: update Git repository URL
    url='',
    # TODO: update keywords
    keywords=[],
    # TODO: update requirements (typically matches requirements.txt)
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)
