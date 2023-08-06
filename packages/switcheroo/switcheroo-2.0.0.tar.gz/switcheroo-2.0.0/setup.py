# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['switcheroo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'switcheroo',
    'version': '2.0.0',
    'description': 'Efficient dispatch-based calling, that might be a switch statement in another language.',
    'long_description': "|CircleCI|_\n\n.. |CircleCI| image:: https://circleci.com/gh/simplistix/switcheroo/tree/master.svg?style=shield\n.. _CircleCI: https://circleci.com/gh/simplistix/switcheroo/tree/master\n\nSwitcheroo\n==========\n\nEfficient dispatch-based calling, that might be a switch statement in another language.\n\nshort usage\n~~~~~~~~~~~\n\n.. code-block:: python\n\n    from switcheroo import Switch\n\n    switch = Switch({\n        'foo': lambda x: x+1,\n    })\n\n>>> switch['foo'](1)\n2\n\n>>> switch['bar'](1)\nTraceback (most recent call last):\n...\nKeyError: 'bar'\n\n.. code-block:: python\n\n    from switcheroo import Switch, default\n\n    switch = Switch({\n        'foo': lambda x: x+1,\n        default: lambda x: x-1,\n    })\n\n>>> switch['foo'](1)\n2\n\n>>> switch['bar'](1)\n0\n\nexplicit usage\n~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    from switcheroo import Switch\n\n    def handle_foo(x):\n        return x+1\n\n    def handle_others(x):\n        return x-1\n\n    switch = Switch()\n    switch.register('foo', handler=handle_foo)\n    switch.default(handle_others)\n\n>>> switch.lookup('foo')(1)\n2\n\n>>> switch.lookup('bar')(1)\n0\n\n>>> switch.override('foo', lambda x: x+2)\n>>> switch.lookup('foo')(1)\n3\n\ndecorator usage\n~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    from switcheroo import Switch\n\n    switch = Switch()\n\n    @switch.handles('foo')\n    def handle_foo(x):\n        return x+1\n\n    @switch.default\n    def handle_others(x):\n        return x-1\n\n>>> switch['foo'](1)\n2\n\n>>> switch['bar'](1)\n0\n\n.. code-block:: python\n\n    @switch.overrides('foo')\n    def new_handle_foo(x):\n        return x+2\n\n>>> switch['foo'](1)\n3\n\nclass helper usage\n~~~~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    class MoarThingz(object):\n\n        switch = Switch()\n\n        def __init__(self, state):\n            self.state = state\n\n        @switch.handles('foo')\n        def handle_foo(self, x):\n            return self.state - x\n\n        @switch.default\n        def handle_foo(self, x):\n            return self.state + x\n\n        def dispatch(self, case, factor, x):\n            return factor * self.switch[case](self, x)\n\n>>> things = MoarThingz(3)\n>>> things.dispatch('foo', factor=1, x=1)\n2\n>>> things.dispatch('bar', factor=-1, x=2)\n-5\n\nsubclass usage\n~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    from switcheroo import Switch, handles, default\n\n    class MySwitch(Switch):\n\n        @handles('foo')\n        def handles(x):\n            return x+1\n\n        @default\n        def default(x):\n            return x-1\n\n>>> MySwitch['foo'](1)\n2\n>>> MySwitch['bar'](1)\n0\n\n\nchanges\n~~~~~~~\n\n2.0.0 (20 Sep 2022)\n-------------------\n\n- Drop Python 2 support.\n\n1.1.0 (26 Nov 2020)\n-------------------\n\n- Add support for overrides.\n\n- Add support for more explicit usage.\n\n1.0.0 (27 Feb 2019)\n-------------------\n\n- 100% coverage checking and automated releases.\n\n0.2.0 (13 Dec 2018)\n-------------------\n\n- Handle subclasses when using the subclass pattern.\n\n0.1.0 (24 Nov 2018)\n-------------------\n\n- Initial release.\n",
    'author': 'Chris Withers',
    'author_email': 'chris@withers.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simplistix/switcheroo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
