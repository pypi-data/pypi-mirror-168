# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thresult']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'thresult',
    'version': '0.9.12',
    'description': 'TangledHub Result',
    'long_description': '[![Build][build-image]]()\n[![Status][status-image]][pypi-project-url]\n[![Stable Version][stable-ver-image]][pypi-project-url]\n[![Coverage][coverage-image]]()\n[![Python][python-ver-image]][pypi-project-url]\n[![License][bsd3-image]][bsd3-url]\n\n\n# thresult\n\n## Overview\n\nTangledHub library for handling returned values from functions/methods and handling errors.\n\n\n## Installation\n\n```bash\npip install thresult\n```\n\n\n## Examples\n\n### Traditional Python try-except example\n\n```python\ndef div(x: float, y: float) -> float:\n    z: float = x / y\n    return z\n\n\nz0: float = div(1.0, 2.0) # 0.5\nz1: float = div(1.0, 0.0) # raises "ZeroDivisionError: division by zero" exception\n```\n\n### Manually create Result value, and Structural Pattern Matching\n\n```python\nfrom thresult import Result, Ok, Err\n\n\ndef div(x: float, y: float) -> Result[float, Exception]:\n    res: Result[float, Exception]\n\n    try:\n        # can raise "ZeroDivisionError: division by zero" exception\n        z: float = x / y\n        res = Ok[float](z)\n    except Exception as e:\n        res = Err[Exception](e)\n\n    return res\n\n\nr0: Result = div(1.0, 2.0) # Ok\nr1: Result = div(1.0, 0.0) # Err\n\nmatch r0:\n    case Ok(v):\n        print(\'Ok, value:\', v)\n    case Err(e):\n        print(\'Err, error:\', e) # "ZeroDivisionError: division by zero"\n\nmatch r1:\n    case Ok(v):\n        print(\'Ok, value:\', v)\n    case Err(e):\n        print(\'Err, error:\', e) # "ZeroDivisionError: division by zero"\n\nz0: float = r0.unwrap() # 0.5\nz1: float = r1.unwrap_or(float(\'inf\')) # inf\nz1: float = r1.unwrap() # raises "ZeroDivisionError: division by zero" exception\n```\n\n### Decorate function with Result, and Structural Pattern Matching\n\n```python\nfrom thresult import Result, Ok, Err\n\n\n@Result[float, Exception]\ndef div(x: float, y: float) -> float:\n    # can raise "ZeroDivisionError: division by zero" exception\n    z: float = x / y\n    return z\n\n\nr0: Result = div(1.0, 2.0) # Ok\nr1: Result = div(1.0, 0.0) # Err\n\nmatch r0:\n    case Ok(v):\n        print(\'Ok, value:\', v)\n    case Err(e):\n        print(\'Err, error:\', e) # "ZeroDivisionError: division by zero"\n\nmatch r1:\n    case Ok(v):\n        print(\'Ok, value:\', v)\n    case Err(e):\n        print(\'Err, error:\', e) # "ZeroDivisionError: division by zero"\n\nz0: float = r0.unwrap() # 0.5\nz1: float = r1.unwrap_or(float(\'inf\')) # inf\nz1: float = r1.unwrap() # raises "ZeroDivisionError: division by zero" exception\n```\n\n### Using Result as context manager (with statement)\n\n```python\nfrom thresult import Result, Ok, Err\n\n\n@Result[float, Exception]\ndef div(x: float, y: float) -> float:\n    z: float = x / y\n    return z\n\n\ntry:\n    with div(1.0, 0.0) as z:\n        # unreachable \n        pass\nexcept ZeroDivisionError as e:\n    # exception happened\n    pass\n```\n\n### Decorate function with auto_unwrap and Result\n\n```python\nfrom thresult import Result, Ok, Err, auto_unwrap\n\n\n@auto_unwrap\n@Result[float, Exception]\ndef div(x: float, y: float) -> float:\n    z: float = x / y\n    return z\n\n\nz0: float = div(1.0, 2.0) # 0.5\nz1: float = div(1.0, 0.0) # raises "ZeroDivisionError: division by zero" exception\n```\n\n\n## Testing\n\n```bash\ndocker-compose build thresult-test ; docker-compose run --rm thresult-test\n```\n\n\n## Building\n\n```bash\ndocker-compose build thresult-build ; docker-compose run --rm thresult-build\n```\n\n\n## Run examples from docker\n\n```bash\ndocker run -it -v $PWD/examples:/code -v $PWD/thresult:/deps/thresult -e PYTHONPATH=/deps python:3.10 /bin/bash\n\ncd /code\n\npython -B example_0.py\npython -B example_1.py\npython -B example_2.py\npython -B example_3.py\n```\n\n\n## Licensing\n\n`thresult` is licensed under the BSD license.\n\nCheck the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details\n\n\n<!-- Badges -->\n[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg\n[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause\n[build-image]: https://img.shields.io/badge/build-success-brightgreen\n[coverage-image]: https://img.shields.io/badge/Coverage-99%25-green\n\n[pypi-project-url]: https://pypi.org/project/thresult/\n[stable-ver-image]: https://img.shields.io/pypi/v/thresult?label=stable\n[python-ver-image]: https://img.shields.io/pypi/pyversions/thresult.svg?logo=python&logoColor=FBE072\n[status-image]: https://img.shields.io/pypi/status/thresult.svg\n',
    'author': 'TangledHub',
    'author_email': 'info@tangledgroup.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tangledlabs/thresult',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
