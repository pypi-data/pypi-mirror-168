# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django',
 'django.env_helper',
 'django.env_helper.management',
 'django.env_helper.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django[argon2]>=4.1,<4.2',
 'coloredlogs>=15.0,<15.1',
 'dj-database-url>=0.5,<0.6',
 'django-postgres-extra>=2.0,<2.1',
 'django-wailer>=1.0.0-beta.2,<1.1.0',
 'djangorestframework-gis>=1.0,<1.1',
 'djangorestframework>=3.13,<3.14',
 'modelw-env-manager>=1.0.0-alpha.5,<1.1.0',
 'psycopg2>=2.9,<2.10',
 'rich>=12.5,<12.6',
 'sentry-sdk>=1.9,<1.10',
 'whitenoise>=6.2,<6.3']

extras_require = \
{'celery': ['celery[redis,tblib]>=5.2,<5.3', 'django-celery-results>=2.4,<2.5'],
 'channels': ['channels>=4.0.0b1,<4.1.0', 'channels-redis>=4.0.0b2,<4.1.0']}

setup_kwargs = {
    'name': 'modelw-preset-django',
    'version': '2022.10.0b4',
    'description': 'Model W preset for Django',
    'long_description': "# Model W &mdash; Django Preset\n\nThis Django preset for Model W's Env Manager provides a basic Django\nconfiguration that is fit to work in PaaS platforms such as DigitalOcean's PaaS.\n\n## Documentation\n\n[✨ **Documentation is there** ✨](http://modelw-django-preset.rtfd.io/)\n",
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ModelW/preset-django',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
