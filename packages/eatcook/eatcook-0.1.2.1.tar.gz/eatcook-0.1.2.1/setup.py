# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['eatcook']
install_requires = \
['colorama>=0.4.5,<0.5.0', 'typer[all]>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['eatcook = eatcook:app']}

setup_kwargs = {
    'name': 'eatcook',
    'version': '0.1.2.1',
    'description': 'Mini HTTP Server.',
    'long_description': '<img src="https://u.cubeupload.com/ihavecandy/eatcook.png">\n\n# eatcook.\n```python\npip install eatcook\n```\n\nEatcook is a simple socket HTTP server. With the ablity to run python files at interpret them as html. (Like CGI)\nThe server also provides a extremely easy way to create sub pages. Using `routebook.json` to redirect users to them\n\n`routebook.json:`\n```json\n{\n  "/", "index.html"  \n}\n```\nOR \n```json\n{\n  "/", "index.py"\n}\n```\n\nTo get 404 page, place a file named `404.html` in the folder in which you\'re running in.\n# Running at CLI\n```\npy -m eatcook --host 127.0.0.1 --port 8000 --folder (where http files are located)\n```\nHost & Port will run at 127.0.0.1:8000 by default if none are given.\n\nFolder will also run in the directory of which you\'re working in if none are given: `./`\n\n# Running in python\n```py\nimport eatcook\n\neatcook.run(host, port, folder) # Runs eatcook.\neatcook.add_route("/", "index.html") # Adds to script\'s route dict if no routebook.json is found. Though, it\'s much recommended to just use routebook.json\n```\n\nTo run python scripts as html:\n```py\nimport random\n\ngenerated = random.randint(1,100000)\nprint(f"<h1 align=\'center\'>{generated}</h1>") # Sends a generated number to client\'s browser.\n```\n\n### Information\nEatcook doesn\'t have the ablity to serve `.css` files. Though, I might muster up the courage to try 👀\n\n',
    'author': 'Porplax',
    'author_email': 'saynemarsh9@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
