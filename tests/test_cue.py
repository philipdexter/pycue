
import pytest

import cue

def test_test():
  assert '1' == str(cue.compile('1'))
