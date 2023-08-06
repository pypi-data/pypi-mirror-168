# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nornir_inspect']
install_requires = \
['nornir>=3.3.0,<4.0.0', 'rich>=12.5.1,<13.0.0']

setup_kwargs = {
    'name': 'nornir-inspect',
    'version': '1.0.3',
    'description': 'Nornir inspection tool',
    'long_description': '# Nornir Inspect\nNornir inspect is a Python library for inspecting the Nornir result structure.\n\n## Install\n\n```\npip install nornir-inspect\n\nor\n\npoetry add nornir-inspect\n```\n\n## Usage\n\n<details>\n  <summary>Nornir setup steps</summary>\n\n```python\nfrom nornir import InitNornir\nfrom nornir.core.task import Result, Task\n\nnr = InitNornir(\n     runner={\n         "plugin": "threaded",\n         "options": {\n             "num_workers": 10,\n         },\n     },\n     inventory={\n         "plugin": "SimpleInventory",\n         "options": {"host_file": "tests/hosts.yaml"},\n     },\n     logging={"enabled": False},\n )\n\n\ndef task_1(task: Task, number: int) -> Result:\n     n = number + 1\n     return Result(host=task.host, result=f"{n}")\n\n\nresult = nr.run(task=task_1, number=1)\n```\n</details>\n\n\n```python\nfrom nornir_inspect import nornir_inspect\n\nnornir_inspect(result)\n\n<class \'nornir.core.task.AggregatedResult\'>\n├── failed = False\n├── failed_hosts = {}\n├── name = task_1\n├── <class \'nornir.core.task.MultiResult\'> [\'node1\']\n│   ├── failed = False\n│   ├── failed_hosts = {}\n│   ├── name = task_1\n│   └── <class \'nornir.core.task.Result\'> [0]\n│       ├── changed = False\n│       ├── diff =\n│       ├── exception = None\n│       ├── failed = False\n│       ├── host = node1\n│       ├── name = task_1\n│       ├── result = 2\n│       ├── severity_level = 20\n│       ├── stderr = None\n│       └── stdout = None\n├── <class \'nornir.core.task.MultiResult\'> [\'node2\']\n│   ├── failed = False\n│   ├── failed_hosts = {}\n│   ├── name = task_1\n│   └── <class \'nornir.core.task.Result\'> [0]\n│       ├── changed = False\n│       ├── diff =\n│       ├── exception = None\n│       ├── failed = False\n│       ├── host = node2\n│       ├── name = task_1\n│       ├── result = 2\n│       ├── severity_level = 20\n│       ├── stderr = None\n│       └── stdout = None\n└── <class \'nornir.core.task.MultiResult\'> [\'node3\']\n    ├── failed = False\n    ├── failed_hosts = {}\n    ├── name = task_1\n    └── <class \'nornir.core.task.Result\'> [0]\n        ├── changed = False\n        ├── diff =\n        ├── exception = None\n        ├── failed = False\n        ├── host = node3\n        ├── name = task_1\n        ├── result = 2\n        ├── severity_level = 20\n        ├── stderr = None\n        └── stdout = None\n```\n\n### Addtional Options\n* `vals` (bool): If True, the values of the attributes will be printed. Defaults to True.\n* `headings`(bool): If True, the first line of the output will include the objects key name or list postion. Defaults to True.\n\n\n',
    'author': 'Packet Coders',
    'author_email': 'contact@packetcoders.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
