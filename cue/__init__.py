
from ctypes import *

lc = cdll.LoadLibrary("golibcue.so")

if sizeof(c_void_p) == 4:
  ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
  ptrdiff_t = c_int64
class GoString(Structure):
  _fields_ = [("p", c_char_p), ("n", ptrdiff_t)]

_cue_value_id_t = c_longlong

lc.Compile.argtypes = [POINTER(_cue_value_id_t), GoString]
lc.Compile.restype = c_char_p
lc.ToString.argtypes = [c_longlong]
lc.ToString.restype = c_char_p
lc.Print.argtypes = [c_longlong]
lc.Print.restype = None
lc.Unifies.argtypes = [c_longlong, c_longlong]
lc.Unifies.restype = c_int8

lc.IsStruct.argtypes = [c_longlong]
lc.IsStruct.restype = c_int8
lc.IsList.argtypes = [c_longlong]
lc.IsList.restype = c_int8

lc.Test.argtypes = [POINTER(c_longlong)]
lc.Test.restype = None

a = c_longlong(1)
lc.Test(byref(a))
print(a.value)

lc.Fields.argtypes = [c_longlong]
lc.Fields.restype = c_longlong
lc.Elems.argtypes = [c_longlong]
lc.Elems.restype = c_longlong
lc.Next.argtypes = [c_longlong]
lc.Next.restype = c_int8
lc.Label.argtypes = [c_longlong]
lc.Label.restype = c_char_p
lc.Value.argtypes = [c_longlong]
lc.Value.restype = c_longlong


# TODO raise exceptions on errors

def compile(s):
  return CueValue(s)

class CueValue:
  def __init__(self, s):
    if isinstance(s, str):
      bs = s.encode('UTF-8')
      out_cue_value_id = _cue_value_id_t()
      res = lc.Compile(byref(out_cue_value_id), GoString(bs, len(s)))
      if res != None:
        res = res.decode('UTF-8')
        raise ValueError(res)
      self._cue_value_id = out_cue_value_id.value
    elif isinstance(s, int):
      self._cue_value_id = s
    else:
      raise ValueError('argument to CueValue.__init__ must be a string or integer')
      # TODO throw exception
      ...

  def unifies_with(self, other):
    return bool(lc.Unifies(self._cue_value_id, other._cue_value_id))

  def is_struct(self):
    return bool(lc.IsStruct(self._cue_value_id))

  def is_list(self):
    return bool(lc.IsList(self._cue_value_id))

  def __str__(self):
    return lc.ToString(self._cue_value_id).decode('UTF-8')

  def __iter__(self):
    if self.is_struct():
      self._iter = lc.Fields(self._cue_value_id)
    elif self.is_list():
      self._iter = lc.Elems(self._cue_value_id)
    else:
      # TODO raise exception
      ...
    return self

  def __next__(self):
    more = lc.Next(self._iter)
    if not more:
      raise StopIteration

    if self.is_struct():
      label = lc.Label(self._iter).decode('UTF_8')
      value = CueValue(lc.Value(self._iter))
      return label, value
    elif self.is_list():
      value = CueValue(lc.Value(self._iter))
      return value
    else:
      # TODO raise exception
      ...
