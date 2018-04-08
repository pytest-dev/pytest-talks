:title: Pytest Intro
:author:  `Floris Bruynooghe <flub@devork.be>`
:author:  `Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>`




Overview
--------- 

* py.test

  .. image:: ./pytest1.png

* `<http://pytest.org>`_
* `<http://github.com/pytest-dev/pytest>`_ 


.. 
  #+BEGIN_NOTES
  - py.test vs pytest
  - Do not get confused with pylint/logilab-common!
  - Been around very long
    - transformed quite a bit
  #+END_NOTES

Introduction
------------

- no-boilerplate test
- discovery
- plain assert
- nice exception formatting
- pdb integration
- output capture
- parametrisation
- markers
- xdist
- plugins
- runs unittest & nose tests too
- ...


Simple Tests
------------

.. code:: python

  def test_int_casting():
      assert int('5') == 5


  class TestFloats:

      def test_dot(self):
          assert float('3.3') == 3.3

      def test_e(self):
          assert float('3.1e3') == 3100.0

output
------

.. code::

  $ py.test
  ========================= test session starts =========================
  platform linux -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy-0.3.1
  rootdir: /tmp/sandbox, inifile:
  collected 3 items

  test.py ...

  ====================== 3 passed in 0.01 seconds =======================

..
  #+BEGIN_NOTES
  - classes mostly for structures
  - discovery
  #+END_NOTES

Detailed Failure Reports
------------------------

.. code:: python

  def test_wrong():
      assert 'Some test about spam' == 'Some blurb about ham'

.. code::


  $ py.test -q
  ========================= test session starts =========================
  platform linux -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy-0.3.1
  rootdir: /tmp/sandbox, inifile:
  collected 1 items

  test_ex.py F

  ============================== FAILURES ===============================
  _____________________________ test_wrong ______________________________

      def test_wrong():
  >       assert 'Some text about spam' == 'Some text about ham'
  E       assert 'Some text about spam' == 'Some text about ham'
  E         - Some text about spam
  E         ?                 ^^
  E         + Some text about ham
  E         ?                 ^

  test.py:2: AssertionError
  ====================== 1 failed in 0.01 seconds =======================


..
  #+BEGIN_NOTES
  - can be customised
  #+END_NOTES

Assertions
==========

..code:: python

  def test_assertions():
      x = y = 0
      assert x
      assert x == 1
      assert x != 2
      assert not x
      assert 3 < x < 5 and y < 5
      s = 'the quick fox ...'
      assert 'fox' in s

..
  #+BEGIN_NOTES
  - native assert for everything
  #+END_NOTES

Expected Exceptions
-------------------

.. code:: python

  import pytest

  def divide(x, y):
      return x / y

  def test_raises():
      with pytest.raises(ZeroDivisionError):
          divide(3, 0)

  def test_exc_args():
      with pytest.raises(Exception) as exc:
          raise Exception(42, 'msg')
      assert exc.value.args = (42, 'msg')
      assert exc.type is Exception
      assert exc.tb

Output Capture
--------------

.. code:: python

  def func(a):
      print('input was: {!r}'.format(a))
      return a + 42

  def test_func():
      assert func(5) < 5

.. code::

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

..
  #+BEGIN_NOTES
  - can be disabled using ~-s~
  #+END_NOTES

Common Options
--------------

- ~-s~ disable output capture
- ~-x~ exit on first failure
- ~-k~ only run matching tests
- ~-l~ show locals
- ~--pdb~ enter debugger on errors
- ~-rsxXw~ ~-ra~ report skipped, xfailed, ...
- defaults in ~pytest.ini~

** showlocals

.. code::

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


Selecting Tests
===============

..code:: python

  def test_foo():
      assert True

  def test_bar():
      assert True

..code::

  $ py.test -v -k foo
  ===================== test session starts =====================
  platform linux -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy
  cachedir: .cache
  rootdir: /tmp/sandbox, inifile:
  collected 2 items

  test_ex.py::test_foo PASSED

  ================ 1 tests deselected by '-kfoo' ================
  =========== 1 passed, 1 deselected in 0.12 seconds ============

Skipping, xfail & marks
-----------------------

.. code:: python

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
      assert 1

- Select tests by mark: ~-m 'not mymark'~
- Marks also useful in plugins

Output
------

.. code::

  > py.test -ra
  ===================== test session starts =====================
  platform linux -- Python 3.4.3, pytest-2.8.0, py-1.4.30, pluggy-0.3.1
  rootdir: /tmp/sandbox, inifile:
  collected 3 items

  test_ex.py sx.
  =================== short test summary info ===================
  SKIP [1] test_ex.py:2: Not supported
  XFAIL test_ex.py::test_oops

  ======= 1 passed, 1 skipped, 1 xfailed in 0.07 seconds ========

Fixtures
---------

- Dependecy injection
- Isolation
- (~.setUp()~ ~.tearDown()~)

.. code:: python

  import pytest

  @pytest.fixture
  def somevalue():
      return 42

  def test_value(somevalue):
      assert somevalue == 42

Fixture finalizer
------------------

.. code:: python

  import pytest

  @pytest.fixture
  def db(request):
      conn = create_conn()

      def fin():
          destroy_db(conn)

      request.addfinalizer(fin)
      return conn

  def test_something_with_db(db):
      assert func(db)

Builtin fixture: tmpdir
------------------------

.. code:: python

  def write(fname):
      with open(fname, 'w') as fp:
          fp.write('hello world')

  def test_output(tmpdir):
      out_txt = tmpdir.join('out.txt')
      write(str(out_txt))
      assert out_txt.read() == 'hello world'

Builtin fixture: monkeypatch
----------------------------

.. code:: python

  import sys

  def test_platform_win(monkeypatch):
      monkeypatch.setattr(sys, 'platform', 'win32')
      assert sys.platform == 'win32'

  def test_platform():
      assert sys.platform == 'posix'

More
----

- parametrization
- fixtures
  - parametrization
  - scopes
- local plugins: ~conftest.py~
  - command line options
  - extra config setup


Questions?
----------