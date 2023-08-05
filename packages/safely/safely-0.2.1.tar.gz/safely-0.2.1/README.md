<h1 align="center">Safely</h1>
<p align="center">Capture side effects, safely ⚔️</p>
<p align="center">
<a href="https://github.com/lukemiloszewski/safely/actions/workflows/ci.yml/badge.svg" target="_blank">
    <img src="https://github.com/lukemiloszewski/safely/actions/workflows/ci.yml/badge.svg" alt="Continuous Integration">
</a>
<a href="https://pypi.org/project/safely" target="_blank">
    <img src="https://img.shields.io/pypi/v/safely?color=%2334D058&label=pypi%20package" alt="Package Version">
</a>
<a href="https://pypi.org/project/safely" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/safely.svg?color=%2334D058" alt="Supported Python Versions">
</a>
</p>

## Installation

```shell
pip install safely
```

## Usage

As a function (without second-order arguments):

```python
def f(...): ...

result = safely(f)(...)
```

As a function (with second-order arguments):

```python
def f(...): ...

result = safely(f, logger=logger.error, message="{exc_type}: {exc_value}")(...)
```

As a decorator (without second-order arguments):

```python
@safely
def f(...): ...

result = f(...)
```

As a decorator (with second-order arguments):

```python
@safely(logger=logger.error, message="{exc_type}: {exc_value}")
def f(...): ...

result = f(...)
```
