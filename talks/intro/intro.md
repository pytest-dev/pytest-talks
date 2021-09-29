Pytest Intro
------------

First version

[Floris Bruynooghe](mailto:flub@devork.be)

retouch and new content

[Ronny Pfannschmidt](mailto:opensource@ronnypfannschmidt.de)


---

where to get/contribute
------------------------

![pytest logo](./pytest1.png)

* http://pytest.org
* http://github.com/pytest-dev/pytest


-----


## introduction
### basic features

- no-boilerplate test
- test discovery
- plain assert
- lovely exception formatting
- output capture
- runs unittest tests too

---

## introduction
### really nice features
- parametrisation
- markers
- pdb integration
- xdist
- plugins


-----

## Simple Tests
### code

```python
# content of simple_tests.py
def test_int_casting():
    assert int('5') == 5


class TestFloats:

    def test_dot(self):
        assert float('3.3') == 3.3

    def test_e(self):
        assert float('3.1e3') == 3100.0
```

---


## Simple Tests
### output

```text
$ pytest simple_tests.py 
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/ronny/Projects/pytest-dev/pytest-talks/talks, configfile: pytest.ini
collected 3 items                                                              

simple_tests.py ...                                                      [100%]

============================== 3 passed in 0.00s ===============================
```

-----

## Detailed Failure Reports
### code
```python
# content of test_failure_report.py
def test_wrong():
    assert 'Some test about spam' == 'Some blurb about ham'
```

---


## Detailed Failure Reports
### output

```
$ pytest -q test_failure_report.py 
F                                          [100%]
==================== FAILURES ====================
___________________ test_wrong ___________________

    def test_wrong():
>       assert 'Some test about spam' == 'Some blurb about ham'
E       AssertionError: assert 'Some test about spam' == 'Some blurb about ham'
E         - Some blurb about ham
E         + Some test about spam

test_failure_report.py:2: AssertionError
============ short test summary info =============
FAILED test_failure_report.py::test_wrong - Ass...
1 failed in 0.01s
```

-----


## Assertions
## code

```python
# content of test_assertions.py
def test_assertions():
  x = y = 0
  assert x
  assert x == 1
  assert x != 2
  assert not x
  assert 3 < x < 5 and y < 5
  s = 'the quick fox ...'
  assert 'fox' in s
```


---


## Assertions
### output

```
$ pytest test_assertions.py 
============== test session starts ===============
platform linux -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/ronny/Projects/pytest-dev/pytest-talks/talks, configfile: pytest.ini
collected 1 item                                 

test_assertions.py F                       [100%]

==================== FAILURES ====================
________________ test_assertions _________________

    def test_assertions():
      x = y = 0
>     assert x
E     assert 0

test_assertions.py:3: AssertionError
============ short test summary info =============
FAILED test_assertions.py::test_assertions - as...
=============== 1 failed in 0.01s ================
```

-----
## Expected Exceptions
### code

```python
# content of test_expected_exceptions.py
import pytest

def divide(x, y):
    return x / y

def test_raises():
    with pytest.raises(ZeroDivisionError):
        divide(3, 0)

def test_exc_args():
    with pytest.raises(Exception) as exc:
        raise Exception(42, 'msg')
    assert exc.value.args == (42, 'msg')
    assert exc.type is Exception
    assert exc.tb
```
---
## Expected Exceptions
### output



```
$ pytest test_expected_exceptions.py 
============== test session starts ===============
platform linux -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/ronny/Projects/pytest-dev/pytest-talks/talks, configfile: pytest.ini
collected 2 items                                

test_expected_exceptions.py ..             [100%]

=============== 2 passed in 0.00s ================
```


-----

## Output Capture
### code
```python

  def func(a):
      print('input was: {!r}'.format(a))
      return a + 42

  def test_func():
      assert func(5) < 5
```

---


## Output Capture
### output

```

  $ py.test
  ========================= test session starts =========================
  platform linux -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy-0.3.1
  rootdir: /tmp/sandbox, inifile:
  collected 1 items

  test_ex.py F

  ============================== FAILURES ===============================
  ______________________________ test_func ______________________________

      def test_func():
  >       assert func(5) < 5
  E       assert 47 < 5
  E        +  where 47 = func(5)

  test_ex.py:6: AssertionError
  -------------------------- Captured stdout call -----------------------
  input was: 5
  ======================== 1 failed in 0.05 seconds =====================
```

-----

## Common Options

- `-s` disable output capture
- `-x` exit on first failure
- `-k` only run matching tests
- `-l` show locals
- `--pdb` enter debugger on errors
- `-rsxXw` `-ra` report skipped, xfailed, ...
- defaults in `pytest.ini`

---

## Common Options
### showlocals

```python
  $ py.test -ql
  F
  ========================== FAILURES ===========================
  __________________________ test_func __________________________

      def test_func():
  >       func(3)


  test_ex.py:8:
  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

  b = 3

      def func(b):
          a = 1
          a += b
          c = a * b
  >       return c / 0
  E       ZeroDivisionError: division by zero

  a          = 4
  b          = 3
  c          = 12

  test_ex.py:5: ZeroDivisionError
```

---

## Common Options
### Selecting Tests
#### code

```python
def test_foo():
    assert True

def test_bar():
    assert True
```

---


## Common Options
### Selecting Tests
#### output


```
  $ py.test -v -k foo
  ===================== test session starts =====================
  platform linux -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy
  cachedir: .cache
  rootdir: /tmp/sandbox, inifile:
  collected 2 items

  test_ex.py::test_foo PASSED

  ================ 1 tests deselected by '-kfoo' ================
  =========== 1 passed, 1 deselected in 0.12 seconds ============
```

---

## Skipping, xfail & marks

```python
import os, pytest

@pytest.mark.skipif(os.name != 'posix', reason='Not supported')
def test_pipe():
  r, w = os.pipe()
  assert 1

@pytest.mark.xfail
def test_oops():
  assert 0

@pytest.mark.mymark
def test_foo():
  assert 1</code></pre>
```

Note:
- Select tests by mark: `-m 'not mymark'`
 - Marks also useful in plugins

---


## Output

```
   py.test -ra
  ===================== test session starts =====================
  platform linux -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy-0.3.1
  rootdir: /tmp/sandbox, inifile:
  collected 3 items

  test_ex.py sx.
  =================== short test summary info ===================
  SKIP [1] test_ex.py:2: Not supported
  XFAIL test_ex.py::test_oops

  ======= 1 passed, 1 skipped, 1 xfailed in 0.07 seconds ========
```

-----

## Fixtures
### about


- Dependency injection
- Isolation
- (`.setUp()` `.tearDown()`)


---

## Fixtures
### basic usage

```python
import pytest

@pytest.fixture
def somevalue():
    return 42

def test_value(somevalue):
    assert somevalue == 42
```

---

## Fixtures
### finalization

```python
import pytest

@pytest.fixture
def db(request):
    conn = create_conn()
    yield conn
    destroy_db(conn)

def test_something_with_db(db):
    assert func(db)
```

-----

## Builtin fixture
### tmp_path

```python
from pathlib import path

def write(fname):
    with open(fname, 'w') as fp:
        fp.write('hello world')

def test_output(tmp_path: Path):
    out_txt = tmp_path / "out.txt"
    write(str(out_txt))
    assert out_txt.read() == 'hello world'
```

---


## Builtin fixture
### monkeypatch

```python

import sys

def test_platform_win(monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'win32')
    assert sys.platform == 'win32'

def test_platform():
    assert sys.platform == 'posix'
```



-----

More
----

- parametrization
- fixtures
  - parametrization
  - scopes
- local plugins: **conftest.py**
  - command line options
  - extra config setup

---


Questions?
----------
