# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flickr_download']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3,<6.0',
 'flickr-api>=0.7.4,<0.8.0',
 'pathvalidate>=2.5.2,<3.0.0',
 'python-dateutil==2.8.1']

entry_points = \
{'console_scripts': ['flickr_download = flickr_download.flick_download:main']}

setup_kwargs = {
    'name': 'flickr-download',
    'version': '0.3.0',
    'description': 'Download photos from Flickr',
    'long_description': '# Flickr Download\n\n## Introduction\n\n[![Build Status](https://app.travis-ci.com/beaufour/flickr-download.svg?branch=master)](https://app.travis-ci.com/github/beaufour/flickr-download)\n\nSimple script to download a [Flickr](http://flickr.com) set.\n\nTo use it you need to get your own Flickr API key here:\n<https://www.flickr.com/services/api/misc.api_keys.html>\n\n    flickr_download -k <api key> -s <api secret> -d <set id>\n\nIt can also list the public set ids for a given user:\n\n    flickr_download -k <api key> -s <api secret> -l <user name>\n\nGet a public set using the title and id to name the downloaded files:\n\n    flickr_download -k <api key> -s <api secret> -d <set id> -n title_and_id\n\nDownload private or restricted photos by authorizing against the users account. (see below)\n\n## Installation\n\nTo install this script use the Python pip utility bundled with your Python distribution:\n\n    pip install flickr_download\n\n## API key\n\nGet your [Flickr API key](http://www.flickr.com/services/api/).\n\nYou can also set your API key and secret in `~/.flickr_download`:\n\n    api_key: my_key\n    api_secret: my_secret\n\n## User Authentication Support\n\nThe script also allows you to authenticate as a user account. That way you can download sets that\nare private and public photos that are restricted. To use this mode, initialize the authorization by\nrunning the script with the `t` parameter to authorize the app.\n\n    flickr_download -k <api key> -s <api secret> -t\n\nThis will save `.flickr_token` containing the authorization. Subsequent calls with `-t` will use the\nstored token. For example using\n\n    flickr_download -k <api key> -s <api secret> -l <USER>\n\nwith _USER_ set to your own username, will only fetch your publicly available sets, whereas adding `-t`\n\n    flickr_download -k <api key> -s <api secret> -l <USER> -t\n\nwill fetch all your sets including private restricted sets.\n\n## Optional arguments\n\n    -h, --help            show this help message and exit\n    -k API_KEY, --api_key API_KEY\n                            Flickr API key\n    -s API_SECRET, --api_secret API_SECRET\n                            Flickr API secret\n    -t, --user_auth       Enable user authentication\n    -l USER, --list USER  List photosets for a user\n    -d SET_ID, --download SET_ID\n                            Download the given set\n    -p USERNAME, --download_user_photos USERNAME\n                            Download all photos for a given user\n    -u USERNAME, --download_user USERNAME\n                            Download all sets for a given user\n    -i PHOTO_ID, --download_photo PHOTO_ID\n                            Download one specific photo\n    -q SIZE_LABEL, --quality SIZE_LABEL\n                            Quality of the picture\n    -n NAMING_MODE, --naming NAMING_MODE\n                            Photo naming mode\n    -m, --list_naming     List naming modes\n    -o, --skip_download   Skip the actual download of the photo\n',
    'author': 'Allan Beaufour',
    'author_email': 'allan@beaufour.dk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/beaufour/flickr-download',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
