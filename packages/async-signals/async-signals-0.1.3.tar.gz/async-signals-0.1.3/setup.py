# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_signals']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-signals',
    'version': '0.1.3',
    'description': 'Async version of the Django signals class - for usage in for example FastAPI.',
    'long_description': '# async-signals\n\nEasy library to implement the observer pattern in async code.\n\n**Note:** This library is a copy of the signals library from \n[Django](https://docs.djangoproject.com/en/4.1/topics/signals/). I always felt\nlike using the observer pattern in Django is pretty well crafted and liked\nthe way Django did implement this. But when switching to\n[FastAPI](https://fastapi.tiangolo.com/) I missed this feature. So I decided\nto copy the signals library from Django and implement it for FastAPI and other\nasync frameworks.  \nA big thanks to the nice people why built Django! And for using a BSD license\nto make this possible.\n\n## Changes from the original Django signals library\n\n* `Signal.send(...)` and `Signal.send_robust(...)` are now async functions 🚀\n* I added type annotations to all functions and classes, mypy is happy now 🧐\n* I created tests for the signals library - without using any Django models 😎\n\n## Installation\n\nJust use `pip install async-signals` to install the library.\n\n## Usage\n\n```python\nfrom async_signals import Signal\n\n# Create a signal\nmy_signal = Signal()\n\n# Connect a function to the signal (can be async or sync, needs to receive **kwargs)\nasync def my_handler(sender, **kwargs):\n    print("Signal received!")\n\nmy_signal.connect(my_handler)\n\n# Send the signal\nawait my_signal.send("sender")\n```\n\n`signal.send(...)` will return a list of all called receivers and their return\nvalues.\n\n## About **kwargs\n\nThe `**kwargs` are mandatory for your receivers. This is because the signal\nwill pass any arguments it receives to the receivers. This is useful if you\nwant to pass additional information to the receivers. To allow adding\nadditional arguments to the signal in the future, the receivers should is\nrequired to accept `**kwargs`.\n\n## About weak signals\n\nThe signal class will automatically remove signals when the receiver is\ngarbage collected. This is done by using weak references. This means that\nyou can use signals in long running applications without having to worry\nabout memory leaks.\n\nIf you want to disable this behaviour you can set the `weak` parameter to\n`False` when connecting the receiver.\n\n```python\nmy_signal.connect(my_handler, weak=False)\n\n# or\n\nmy_signal.connect(my_handler, weak=True)  # the default\n```\n\n## About async signals\n\nThe signal class will automatically await async receivers. If your receiver\nis sync it will be executed normally.\n\n## About the sender\n\nThe sender is the object that sends the signal. It can be anything. It is\npassed to the receiver as the first argument. This is useful if you want to\nhave multiple signals in your application and you want to know which signal\nwas sent. Normally the sender is the object that triggers the signal.\n\nYou may also pass the sender when connecting a receiver. This is useful if\nyou want to connect a receiver to a specific sender. If you do this the\nreceiver will only be called when the sender is the same as the one you\npassed when connecting the receiver.\n\n**Note:** I normally tend to use Pydantic models as the sender in FastAPI. But\nfeel free to use whatever you want.\n\n```python\nmy_signal.connect(my_handler, sender="sender")\n\n# This will not call the receiver\nawait my_signal.send("other_sender")\n```\n\n## Using the receiver decorator\n\nYou can also use the `receiver` decorator to connect a receiver to a signal.\n\n```python\n@receiver(my_signal)\nasync def my_handler(sender, **kwargs):\n    print("Signal received!")\n```\n\nOr if you want to limit the receiver to a specific sender.\n\n```python\n@receiver(my_signal, sender="sender")\nasync def my_handler(sender, **kwargs):\n    print("Signal received!")\n```\n\n## Handle exceptions\n\nBy default the signal class will raise exceptions raised by receivers. If\nyou want the signal to catch the exceptions and continue to call the other\nreceivers you can use `send_robust(..)` instead of `send()`. The return value\nwill be a list of tuples containing the receiver and the return or the\nexception raised by the receiver. You will need to check the type of the\nreturn value to see if it is an exception or not.\n\n```python\nawait my_signal.send_robust("sender")\n```\n\n# Contributing\n\nIf you want to contribute to this project, feel free to just fork the project,\ncreate a dev branch in your fork and then create a pull request (PR). If you\nare unsure about whether your changes really suit the project please create an\nissue first, to talk about this.\n',
    'author': 'TEAM23 GmbH',
    'author_email': 'info@team23.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/team23/async-signals',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
