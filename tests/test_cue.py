
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

  assert True == cue.compile('null').is_null()
  assert True == cue.compile('true').is_bool()
  assert True == cue.compile('1').is_int()
  assert True == cue.compile('1.0').is_float()
  assert True == cue.compile(r"'\x03abc'").is_bytes()
  assert True == cue.compile('"hi"').is_string()
  assert True == cue.compile('{a:1}').is_struct()
  assert True == cue.compile('[1,2]').is_list()

  assert 1 == cue.compile('1').to_int()
  assert 2 == int(cue.compile('2'))
  with pytest.raises(ValueError):
    assert 1 == cue.compile('"hi"').to_int()
  assert 9223372036854775807 == int(cue.compile("9223372036854775807"))
  with pytest.raises(ValueError):
    assert 9223372036854775808 == int(cue.compile("9223372036854775808"))
  assert -9223372036854775807 == int(cue.compile('-9223372036854775807 '))
  with pytest.raises(ValueError):
    assert -9223372036854775808 == int(cue.compile('-9223372036854775808 '))

  assert 1.0 == cue.compile('1.0').to_float()
  assert 2.0 == float(cue.compile('2.0'))
  with pytest.raises(ValueError):
    assert 1.0 == cue.compile('"hi"').to_int()
  assert 4.9 == float(cue.compile('1 + 3.9'))

  assert True == cue.compile('true').to_bool()
  assert False == bool(cue.compile('false && true'))
  with pytest.raises(ValueError):
    assert True == cue.compile('"hi"').to_int()
