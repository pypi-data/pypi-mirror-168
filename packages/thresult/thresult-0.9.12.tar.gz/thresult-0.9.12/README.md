[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][bsd3-image]][bsd3-url]


# thresult

## Overview

TangledHub library for handling returned values from functions/methods and handling errors.


## Installation

```bash
pip install thresult
```


## Examples

### Traditional Python try-except example

```python
def div(x: float, y: float) -> float:
    z: float = x / y
    return z


z0: float = div(1.0, 2.0) # 0.5
z1: float = div(1.0, 0.0) # raises "ZeroDivisionError: division by zero" exception
```

### Manually create Result value, and Structural Pattern Matching

```python
from thresult import Result, Ok, Err


def div(x: float, y: float) -> Result[float, Exception]:
    res: Result[float, Exception]

    try:
        # can raise "ZeroDivisionError: division by zero" exception
        z: float = x / y
        res = Ok[float](z)
    except Exception as e:
        res = Err[Exception](e)

    return res


r0: Result = div(1.0, 2.0) # Ok
r1: Result = div(1.0, 0.0) # Err

match r0:
    case Ok(v):
        print('Ok, value:', v)
    case Err(e):
        print('Err, error:', e) # "ZeroDivisionError: division by zero"

match r1:
    case Ok(v):
        print('Ok, value:', v)
    case Err(e):
        print('Err, error:', e) # "ZeroDivisionError: division by zero"

z0: float = r0.unwrap() # 0.5
z1: float = r1.unwrap_or(float('inf')) # inf
z1: float = r1.unwrap() # raises "ZeroDivisionError: division by zero" exception
```

### Decorate function with Result, and Structural Pattern Matching

```python
from thresult import Result, Ok, Err


@Result[float, Exception]
def div(x: float, y: float) -> float:
    # can raise "ZeroDivisionError: division by zero" exception
    z: float = x / y
    return z


r0: Result = div(1.0, 2.0) # Ok
r1: Result = div(1.0, 0.0) # Err

match r0:
    case Ok(v):
        print('Ok, value:', v)
    case Err(e):
        print('Err, error:', e) # "ZeroDivisionError: division by zero"

match r1:
    case Ok(v):
        print('Ok, value:', v)
    case Err(e):
        print('Err, error:', e) # "ZeroDivisionError: division by zero"

z0: float = r0.unwrap() # 0.5
z1: float = r1.unwrap_or(float('inf')) # inf
z1: float = r1.unwrap() # raises "ZeroDivisionError: division by zero" exception
```

### Using Result as context manager (with statement)

```python
from thresult import Result, Ok, Err


@Result[float, Exception]
def div(x: float, y: float) -> float:
    z: float = x / y
    return z


try:
    with div(1.0, 0.0) as z:
        # unreachable 
        pass
except ZeroDivisionError as e:
    # exception happened
    pass
```

### Decorate function with auto_unwrap and Result

```python
from thresult import Result, Ok, Err, auto_unwrap


@auto_unwrap
@Result[float, Exception]
def div(x: float, y: float) -> float:
    z: float = x / y
    return z


z0: float = div(1.0, 2.0) # 0.5
z1: float = div(1.0, 0.0) # raises "ZeroDivisionError: division by zero" exception
```


## Testing

```bash
docker-compose build thresult-test ; docker-compose run --rm thresult-test
```


## Building

```bash
docker-compose build thresult-build ; docker-compose run --rm thresult-build
```


## Run examples from docker

```bash
docker run -it -v $PWD/examples:/code -v $PWD/thresult:/deps/thresult -e PYTHONPATH=/deps python:3.10 /bin/bash

cd /code

python -B example_0.py
python -B example_1.py
python -B example_2.py
python -B example_3.py
```


## Licensing

`thresult` is licensed under the BSD license.

Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details


<!-- Badges -->
[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause
[build-image]: https://img.shields.io/badge/build-success-brightgreen
[coverage-image]: https://img.shields.io/badge/Coverage-99%25-green

[pypi-project-url]: https://pypi.org/project/thresult/
[stable-ver-image]: https://img.shields.io/pypi/v/thresult?label=stable
[python-ver-image]: https://img.shields.io/pypi/pyversions/thresult.svg?logo=python&logoColor=FBE072
[status-image]: https://img.shields.io/pypi/status/thresult.svg
