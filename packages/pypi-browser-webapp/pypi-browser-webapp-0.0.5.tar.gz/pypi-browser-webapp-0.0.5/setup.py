# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_browser']

package_data = \
{'': ['*'],
 'pypi_browser': ['static/*',
                  'templates/_base.html',
                  'templates/_base.html',
                  'templates/_base.html',
                  'templates/_base.html',
                  'templates/_base.html',
                  'templates/_base.html',
                  'templates/_macros.html',
                  'templates/_macros.html',
                  'templates/_macros.html',
                  'templates/_macros.html',
                  'templates/_macros.html',
                  'templates/_macros.html',
                  'templates/home.html',
                  'templates/home.html',
                  'templates/home.html',
                  'templates/home.html',
                  'templates/home.html',
                  'templates/home.html',
                  'templates/package.html',
                  'templates/package.html',
                  'templates/package.html',
                  'templates/package.html',
                  'templates/package.html',
                  'templates/package.html',
                  'templates/package_file.html',
                  'templates/package_file.html',
                  'templates/package_file.html',
                  'templates/package_file.html',
                  'templates/package_file.html',
                  'templates/package_file.html',
                  'templates/package_file_archive_path.html',
                  'templates/package_file_archive_path.html',
                  'templates/package_file_archive_path.html',
                  'templates/package_file_archive_path.html',
                  'templates/package_file_archive_path.html',
                  'templates/package_file_archive_path.html']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'MarkupSafe>=2.1.1,<3.0.0',
 'Pygments>=2.13.0,<3.0.0',
 'aiofiles>=22.1.0,<23.0.0',
 'fluffy-code>=0.0.2,<0.0.3',
 'httpx>=0.23.0,<0.24.0',
 'identify>=2.5.5,<3.0.0',
 'packaging>=21.3,<22.0',
 'starlette']

setup_kwargs = {
    'name': 'pypi-browser-webapp',
    'version': '0.0.5',
    'description': 'PyPI package browsing web application',
    'long_description': "PyPI Browser\n============\n\n**PyPI Browser** is a web application for browsing the contents of packages on\n[the Python Package Index](https://pypi.org/).\n\nYou can view a live version which provides information about packages from pypi.org:\n\n* [Search page](https://pypi-browser.org/)\n* [Package page for the `django` package](https://pypi-browser.org/package/django)\n* [Archive browse page for the `Django-4.1.1-py3-none-any.whl` file](https://pypi-browser.org/package/django/Django-4.1.1-py3-none-any.whl)\n* [File viewing page for a random file from the same archive](https://pypi-browser.org/package/django/Django-4.1.1-py3-none-any.whl/django/forms/boundfield.py)\n\nIt can also be deployed with a private PyPI registry as its target in order to\nbe used for a company's internal registry.\n\n\n## Features\n\n![Search page](https://i.fluffy.cc/0lzgf46zcHZs90BZfMKp7cvspnk7QrZk.png)\n\n\n### Browse uploaded package archives\n\n![Browse uploaded archives](https://i.fluffy.cc/MnRscjgHrVw7DfnsrM3DV2rVQBB3SGNw.png)\n\nYou can see all uploaded package archives for a given package.\n\n\n### Inspect package archive metadata and contents\n\n![Inspect package archives](https://i.fluffy.cc/skXvnlvvhP8NwSN7RrjHBKrV1xMxKzqv.png)\n\nYou can inspect a package archive's metadata and its contents.\n\n\n### Easily view files from package archives\n\n![View file](https://i.fluffy.cc/6hp4VQmDF4pF6l54QWMfwjXdTpVGk27m.png)\n\nYou can display text files directly in your browser, with syntax highlighting\nand other features like line selection provided by\n[fluffy-code](https://github.com/chriskuehl/fluffy-code).\n\nBinary files can also be downloaded.\n\n\n## Deploying PyPI Browser\n\nTo run your own copy, install\n[`pypi-browser-webapp`](https://pypi.org/project/pypi-browser-webapp/) using\npip, then run the `pypi_browser.app:app` ASGI application using any ASGI web\nserver (e.g. uvicorn).\n\nYou can set these environment variables to configure the server:\n\n* `PYPI_BROWSER_PYPI_URL`: URL for the PyPI server to use (defaults to\n  `https://pypi.org`)\n* `PYPI_BROWSER_PACKAGE_CACHE_PATH`: Filesystem path to use for caching\n  downloaded files. This will grow forever (the app does not clean it up) so\n  you may want to use `tmpreaper` or similar to manage its size.\n\npypi-browser is an ASGI app, and while it performs a lot of I/O (downloading and\nextracting packages on-demand), some effort has been made to keep all blocking\noperations off of the main thread. It should be fairly performant.\n\n\n## Contributing\n\nTo build this project locally, you'll need to [install\nPoetry](https://python-poetry.org/docs/) and run `poetry install`.\n\nOnce installed, you can run\n\n```bash\n$ make start-dev\n```\n\nto run a copy of the application locally with hot reloading enabled.\n",
    'author': 'Chris Kuehl',
    'author_email': 'ckuehl@ckuehl.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
