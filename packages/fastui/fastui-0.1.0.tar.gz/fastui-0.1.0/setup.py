# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastui']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.85.0,<0.86.0', 'uvicorn>=0.18.3,<0.19.0', 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'fastui',
    'version': '0.1.0',
    'description': 'Simple and fast way to create reactive web application in PyPython',
    'long_description': "# Fast UI\n\nFastest way to make User Interfaces in Python\n\n## Design\n\nAll events from HTML will be forwarded from HTML to Python via JS. Python will perform all the required operations and pass the information back to JS, which will update its store. A reactive framework in JS will take the data in store and update the UI. Simple :)\nAll the communication will happen over standard websocket.\n\nI know it's not the fastest and most performant way of doing things. But it works! And requires least amount of knowledge to get started. So why not!\n\n## Tasks\n\n1. HTML Components\n2. Forwarding events\n3. Calling Python code\n4. Updating JS store\n5. Reactively updating the UI\n\n## Goal\n\nMake a simple click to increment app using this construct.\n\n## Draft 1\n\n1. Make a function in JS that sends a message over websocket to execute a particular piece of Python code\n2. Call this function for any event handling that needs to be performed\n3. Execute the python function and make required chnages to the store\n4. Send back a msg to the frontend to update it's store\n5. Assuming the application is reactive, it'll automatically re render the UI to show items.\n",
    'author': 'Apoorva Singh',
    'author_email': 'apoorvasingh157@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
