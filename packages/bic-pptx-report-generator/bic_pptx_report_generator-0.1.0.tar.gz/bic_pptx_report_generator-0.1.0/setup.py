# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bic_pptx_report_generator']
install_requires = \
['PyAutoGUI>=0.9.53,<0.10.0', 'python-pptx>=0.6.21,<0.7.0']

setup_kwargs = {
    'name': 'bic-pptx-report-generator',
    'version': '0.1.0',
    'description': 'Input folder with pictures and text files where the text files describe the pictures and are named to match the picture they describe. The folders are named what you want the slides to be named, and the names of the pictures match what you would want in the labels.',
    'long_description': None,
    'author': 'Heather-BIC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
