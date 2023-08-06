# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nexus_bundler', 'nexus_bundler.publishers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hoppr-nexus-bundler',
    'version': '0.3.1',
    'description': 'Plug-in for Hoppr to bundle artifacts into a Nexus Repository',
    'long_description': '# Nexus Bundler for Hoppr\n\nThe Nexus Bundler is a plug-in for [Hoppr](https://gitlab.com/lmco/hoppr/hoppr) to package the collected artifacts into an existing Nexus instance.\n\n## Configuration\n\nThe following fields are supported values for configuring this plugin (in the Hoppr transfer configuration file):\n\n\n| Option | Description | Default |\n| ------ | ------ |------|\n|url| The URL for the Nexus API | Port 8081 on the server specified by the NEXUS_IP environment variable, using an `http://` schema |\n|username| User name to be used to access the Nexus instance | `admin` |\n|password_env| Envirionment variable containing the password to access the Nexus instance with the above username | `NEXUS_PW`|\n|docker_url| URL to be used to access the docker repository on the Nexus instance. | Port 5000 on the server specified by the NEXUS_IP environment variable, using an `http://` schema |\n|docker_port| Port on which the Nexus instance should listen for docker requests | `5000` |\n|force_http| Indicates whether docker requests should be accessed using the `http://` or `https://` url schema.  |`False` (docker requests must be made using `https://`) |\n\n**Note**: At this time, the Nexus Bundler only supports a single Docker repository per Nexus instance\n\n**Note**: The port of the `docker_url` may differ from that specified by `docker_port` because of port forwarding (for example, if Nexus is run as a docker image).  `docker_port` is the port used internally by Nexus.\n\nFor example, if Nexus is run as a docker image via `docker run -p 1701:5000 sonatype/nexus3:3.40.1` then the  `docker_port` would be `5000`, and the `docker_url` would be something like `https://myserver.com:1701/`.\n',
    'author': 'LMCO Open Source',
    'author_email': 'open.source@lmco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hoppr.dev/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
