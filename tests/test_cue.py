
import pytest

import cue

def test_basic():
  assert '1' == str(cue.compile('1'))
  assert ['1', '2', '3', '{\n\ta: 1\n}'] == [str(v) for v in cue.compile('[1,2,3,{a:1}]')]
  assert [('a', '1'), ('b', '2')] == [(str(k), str(v)) for k, v in cue.compile('{a: 1, b: 2}')]
