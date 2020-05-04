
import pytest

import cue

def test_basic():
  cue.compile('')
  assert '1' == str(cue.compile('1'))
  assert ['1', '2', '3', '{\n\ta: 1\n}'] == [str(v) for v in cue.compile('[1,2,3,{a:1}]')]
  assert [('a', '1'), ('b', '2')] == [(str(k), str(v)) for k, v in cue.compile('{a: 1, b: 2}')]
  with pytest.raises(ValueError):
    cue.compile('a')
  v1 = cue.compile('{a: 1}')
  v2 = cue.compile('{a: 2}')
  v3 = cue.compile('{a: <3}')
  assert False == v1.unifies_with(v2)
  assert True == v1.unifies_with(v3)
  assert True == v1.unifies_with(v3)
  assert True == v2.unifies_with(v3)
  with pytest.raises(ValueError):
    iter(cue.compile('1'))
