# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_recaptcha']

package_data = \
{'': ['*'], 'google_recaptcha': ['templates/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'google-recaptcha',
    'version': '2.0.1',
    'description': "Google recaptcha helps you protect your web form by using google's latest recaptcha (Completely Automated Public Turing test to tell Computers and Humans Apart) technology.",
    'long_description': '# Standalone Google Recaptcha for Python\nGoogle recaptcha helps you protect your web form by using google\'s latest recaptcha \n(Completely Automated Public Turing test to tell Computers and Humans Apart) technology.\n\n[![PyPi](https://github.com/jpraychev/google-recaptcha/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jpraychev/google-recaptcha/actions/workflows/python-publish.yml)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/google-recaptcha.svg)](https://pypistats.org/packages/google-recaptcha)\n\n# Documentation\n\n# Installation\n```\npip install google-recaptcha\n```\n\n# Introduction\nCurrent version of the library works by placing the {{ recaptcha }} object in the form you want to protect. It searches automatically for the form that the object is placed in.\n\nFrom version 2.0.0, you can use the "Checkbox" version of Google\'s recaptcha. By default, the library is using v3, so if you want to use v2 you have to explicitly set it when initializing the ReCaptcha object (See below).\n\nSite\'s and secret\'s keys can be either passed to the object in your views file or export them as environment variables respectively RECAPTCHA_SITE_KEY and RECAPTCHA_SECRET_KEY.\n\n```\n# With environment variables\n\nfrom google_recaptcha import ReCaptcha\napp = Flask(__name__)\nrecaptcha = ReCaptcha(app) # Uses version 3 by default\nrecaptcha = ReCaptcha(app, version=3) # Explicitly set version 3 (same as above, just for brevity)\nrecaptcha = ReCaptcha(app, version=2) # Excplicitly set version 2\n\n@app.route("/contact/", methods=["GET", "POST"])\ndef home():\n\n    if recaptcha.verify():\n        print(\'Recaptcha has successded.\')\n    else:\n        print(\'Recaptcha has failed.\')\n```\n\n```\n# Without environment variables\nfrom google_recaptcha import ReCaptcha\napp = Flask(__name__)\nrecaptcha = ReCaptcha(\n    app=app,\n    site_key="your-site-key",\n    secret_key="your-secret-key"\n)\n\n@app.route("/contact/", methods=["GET", "POST"])\ndef home():\n\n    if recaptcha.verify():\n        print(\'Recaptcha has successded.\')\n    else:\n        print(\'Recaptcha has failed.\')\n```\nIn your HTML template file:\n```\n<form id="contact-form" method="post" class="control-form">\n    <div class="row">\n        <div class="col-xl-6">\n            <input type="text" name="name" placeholder="Name" required="" id="id_name">\n        </div>\n        <div class="col-xl-6">\n            <input type="text" name="email" placeholder="Email" required="" id="id_email">\n        </div>\n        <div class="col-xl-12">\n            <input type="text" name="subject" placeholder="Subject" required="" id="id_subject">\n        </div>\n        <div class="col-xl-12">\n            <textarea name="message" cols="40" rows="10" placeholder="Message" required="" id="id_message"></textarea>\n        </div>\n        <div class="col-xl-12">\n            <button id="form-btn" type="submit" class="btn btn-block btn-primary">Send now</button>\n        </div>\n    </div>\n    {{ recaptcha }}\n</form>\n```',
    'author': 'Jordan Raychev',
    'author_email': 'jpraychev@gmail.com',
    'maintainer': 'Jordan Raychev',
    'maintainer_email': 'jpraychev@gmail.com',
    'url': 'https://github.com/jpraychev/google-recaptcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
