# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchwork']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'benchwork',
    'version': '0.0.0',
    'description': 'A framework for benchmarking in python',
    'long_description': '# benchwork\n\nA framework for benchmarking in python\n\n## Installation\n\n```python\npip install -U benchwork\n```\n\n## Usage\n\n```python\nfrom benchwork import (\n    BenchAPI,\n    BenchCaseSpeed,\n    BenchSuite,\n    BenchSetSpeed,\n    BenchSetVersion,\n    run_suite,\n)\n\n\nclass BenchAPIPackage1(BenchAPI):\n    name = "package1"\n    version = "0.0.1"\n\n\nclass BenchAPIPackage2(BenchAPI):\n    name = "package2"\n    version = "0.0.2"\n\n\nclass BenchCaseSpeed(BenchCaseSpeed):\n    timeit_number = 10\n\n    def run_core(self):\n        import time\n        time.sleep(.1)\n\n\nclass BenchSetSpeed(BenchSetSpeed):\n    case = BenchCaseSpeed\n\n\nclass BenchSuite(BenchSuite):\n    """Benchmarking suite"""\n    set_classes = [BenchSetVersion, BenchSetSpeed]\n\n\nif __name__ == "__main__":\n    run_suite(BenchSuite, None, "Benchmarking")\n```\n\nOutput:\n\n```markdown\n# Benchmarking\n\nBenchmarking suite\n\n## Versions\n\nShow versions of testing packages\n\n| |Version|\n|-|-----------------------|\n|package1|0.0.1|\n|package2|0.0.2|\n\n## Running speed\n\n| |Speed|\n|-|-----------------------|\n|package1|1.003228693996789|\n|package2|1.0028911930057802|\n```\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
