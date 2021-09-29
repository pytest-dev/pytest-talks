def test_assertions():
  x = y = 0
  assert x
  assert x == 1
  assert x != 2
  assert not x
  assert 3 < x < 5 and y < 5
  s = 'the quick fox ...'
  assert 'fox' in s