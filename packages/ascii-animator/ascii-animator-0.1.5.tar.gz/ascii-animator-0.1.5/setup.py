#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'ascii-animator',
        version = '0.1.5',
        description = 'A simple ASCII art animator',
        long_description = '# ascii-animator\n[![build](https://github.com/soda480/ascii-animator/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/soda480/ascii-animator/actions/workflows/main.yml)\n[![complexity](https://img.shields.io/badge/complexity-Simple:%205-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/ascii-animator.svg)](https://badge.fury.io/py/ascii-animator)\n[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)\n\nA simple ASCII text animator.\n\nThe `ascii-art-animator` CLI will take as input a GIF image, extract all the frames from it, convert each frame to ASCII art using [ascii-magic](https://pypi.org/project/ascii-magic/), then display each frame to the terminal using [l2term](https://pypi.org/project/l2term/).\n\n### Installation\n```bash\npip install ascii_animator\n```\n\n### Usage\n```\nusage: ascii-art-animator [-h] [-s SPEED] [-f FILE] [-d] [-a] [-m MAX_LOOPS] [-c COLUMNS]\n\nAscii Art Animator from GIF\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s SPEED, --speed SPEED\n                        speed of the animation: very_slow, slow, normal, fast (default normal)\n  -f FILE, --file FILE  the path to a gif file\n  -d, --debug           display debug messages to stdout\n  -a, --show_axis       display the grid axis\n  -m MAX_LOOPS, --max_loops MAX_LOOPS\n                        maximum number of loops, set to 0 to loop through image until keyboard interrupt (default 1)\n  -c COLUMNS, --columns COLUMNS\n                        the number of characters per row (default 150)\n```\n\n### Examples\n\n#### ASCII Art Animator\n\nUse `ascii-art-animator` to convert the following [GIF image](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich.gif) to an ascii animation and demonstrate the use of the optional arguments.\n* show x and y axis\n* loop through the image only once\n* set columns to 130 characters\n\n```bash\nascii-art-animator -f docs/images/marcovich.gif -a -m 3 -c 100\n```\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich-exec.gif)\n\n#### [Equalizer Bars Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example2.py)\n\nCreate an animation by subclassing the `Animation` class to resemble symmetrical equalizer bars and display it to the terminal using the `Animator` class.\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example2.gif)\n\n#### [Matrix Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example3.py)\n\nCreate an animation by subclassing the `Animation` class to resemble the Matrix and display it to the terminal using the `Animator` class.\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example3.gif)\n\n#### [Game-Of-Life](https://github.com/soda480/game-of-life)\n\nA Conway Game-Of-Life implementation that uses `ascii_animator` to display the game to the terminal.\n\n### Development\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```bash\ndocker image build \\\n-t \\\nascii-animator:latest .\n```\n\nRun the Docker container:\n```bash\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nascii-animator:latest \\\nbash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/ascii-animator',
        project_urls = {},

        scripts = [],
        packages = ['ascii_animator'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'console_scripts': ['ascii-art-animator = ascii_animator.cli:main']
        },
        data_files = [],
        package_data = {},
        install_requires = [
            'l2term~=0.1.8',
            'ascii-magic'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
