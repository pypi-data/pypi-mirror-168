# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zninit', 'zninit.core', 'zninit.descriptor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zninit',
    'version': '0.1.0',
    'description': 'Descriptor based dataclass implementation',
    'long_description': '[![Coverage Status](https://coveralls.io/repos/github/zincware/ZnInit/badge.svg?branch=main)](https://coveralls.io/github/zincware/ZnInit?branch=main)\n![PyTest](https://github.com/zincware/ZnTrack/actions/workflows/pytest.yaml/badge.svg)\n[![PyPI version](https://badge.fury.io/py/zninit.svg)](https://badge.fury.io/py/zninit)\n[![code-style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black/)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zincware/ZnInit/HEAD)\n\n# ZnInit - Automatic Generation of ``__init__`` based on Descriptors\n\nThis package provides a base class for ``dataclass`` like structures with the addition of using [Descriptors](https://docs.python.org/3/howto/descriptor.html).\nThe main functionality is the automatic generation of an keyword-only``__init__`` based on selected descriptors.\nThe descriptors can e.g. overwrite ``__set__`` or ``__get__`` or have custom metadata associated with them.\nThe ``ZnInit`` package is used by [ZnTrack](https://github.com/zincware/ZnTrack) to enable lazy loading data from files as well as distinguishing between different types of descriptors such as `zn.params` or `zn.outputs`. An example can be found in the `examples` directory.\n\n# Example\nThe most simple use case is a replication of a dataclass like structure.\n\n```python\nfrom zninit import ZnInit, Descriptor\n\n\nclass Human(ZnInit):\n    name: str = Descriptor()\n    language: str = Descriptor("EN")\n\n\n# This will generate the following init:\ndef __init__(self, *, name, language="EN"):\n    self.name = name\n    self.language = language\n\n\nfabian = Human(name="Fabian")\n# or\nfabian = Human(name="Fabian", language="DE")\n```\n\nThe benefit of using ``ZnInit`` comes with using descriptors. You can subclass the `zninit.Descriptor` class and only add certain kwargs to the `__init__` defined in `init_descriptors: list`. Furthermore, a `post_init` method is available to run code immediately after initializing the class.\n\n````python\nfrom zninit import ZnInit, Descriptor\n\n\nclass Input(Descriptor):\n    """A Parameter"""\n\n\nclass Metric(Descriptor):\n    """An Output"""\n\n\nclass Human(ZnInit):\n    init_descriptors = [Input] # only add Input descriptors to the __init__\n    name: str = Input()\n    language: str = Input("DE")\n    date: str = Metric()  # will not appear in the __init__\n\n    def post_init(self):\n        self.date = "2022-09-16"\n\n\njulian = Human(name="Julian")\nprint(julian) # Human(language=\'DE\', name=\'Julian\')\nprint(julian.date)  # 2022-09-16\n````\nOne benefit of ``ZnInit`` is that it also allows for inheritance.\n\n````python\nfrom zninit import ZnInit, Descriptor\n\nclass Animal(ZnInit):\n    age: int = Descriptor()\n    \nclass Cat(Animal):\n    name: str = Descriptor()\n    \nbilly = Cat(age=4, name="Billy")\n````',
    'author': 'zincwarecode',
    'author_email': 'zincwarecode@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
