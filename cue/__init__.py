
from ctypes import *

lc = cdll.LoadLibrary("golibcue.so")

if sizeof(c_void_p) == 4:
  ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
  ptrdiff_t = c_int64
class GoString(Structure):
  _fields_ = [("p", c_char_p), ("n", ptrdiff_t)]

lc.Compile.argtypes = [GoString]
lc.Compile.restype = c_longlong
lc.ToString.argtypes = [c_longlong]
lc.ToString.restype = c_char_p
lc.Print.argtypes = [c_longlong]
lc.Print.restype = None
lc.Unifies.argtypes = [c_longlong, c_longlong]
lc.Unifies.restype = c_int8

lc.Test.argtypes = [POINTER(c_longlong)]
lc.Test.restype = None

a = c_longlong(1)
lc.Test(byref(a))
print(a.value)

lc.Fields.argtypes = [c_longlong]
lc.Fields.restype = c_longlong
lc.Next.argtypes = [c_longlong]
lc.Next.restype = c_int8
lc.Label.argtypes = [c_longlong]
lc.Label.restype = c_char_p
lc.Value.argtypes = [c_longlong]
lc.Value.restype = c_longlong

def compile(s):
  return CueInstance(s)

class CueInstance:
  def __init__(self, s):
    bs = s.encode('UTF-8')
    self._cue_instance = lc.Compile(GoString(bs, len(s)))

  def unifies_with(self, other):
    return bool(lc.Unifies(self._cue_instance, other._cue_instance))

  def __str__(self):
    return lc.ToString(self._cue_instance).decode('UTF-8')

  def __iter__(self):
    self._iter = lc.Fields(self._cue_instance)
    return self

  def __next__(self):
    more = lc.Next(self._iter)
    if not more:
      raise StopIteration
    label = lc.Label(self._iter).decode('UTF_8')
    value = CueInstance('')
    value._cue_instance = lc.Value(self._iter)
    return label, value
