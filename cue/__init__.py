
import cue.golibcue as lc

def compile(s):
  return CueValue(s)

class CueValue:
  def __init__(self, s):
    if isinstance(s, str):
      bs = s.encode('UTF-8')
      out_cue_value_id = lc._cue_value_id_t()
      res = lc.Compile(lc.byref(out_cue_value_id), lc.GoString(bs, len(s)))
      if res is not None:
        raise ValueError(res.decode('UTF-8'))
      self._cue_value_id = out_cue_value_id.value
    elif isinstance(s, int):
      self._cue_value_id = s
    else:
      raise ValueError('argument to CueValue.__init__ must be a string or integer')

  def unifies_with(self, other):
    return bool(lc.Unifies(self._cue_value_id, other._cue_value_id))

  def is_bottom(self):
    return bool(lc.IsBottom(self._cue_value_id))

  def is_null(self):
    return bool(lc.IsNull(self._cue_value_id))

  def is_bool(self):
    return bool(lc.IsBool(self._cue_value_id))

  def is_int(self):
    return bool(lc.IsInt(self._cue_value_id))

  def is_float(self):
    return bool(lc.IsFloat(self._cue_value_id))

  def is_string(self):
    return bool(lc.IsString(self._cue_value_id))

  def is_bytes(self):
    return bool(lc.IsBytes(self._cue_value_id))

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
      raise ValueError('can only iterate over a struct or list')
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
      raise ValueError('can only iterate over a struct or list')

  def to_int(self):
    if not self.is_int():
      raise ValueError('can only convert cue integer values to ints')
    out_int = lc.c_longlong()
    res = lc.Int(lc.byref(out_int), self._cue_value_id)
    if res is not None:
      raise ValueError(res.decode('UTF-8'))
    return out_int.value

  def __int__(self):
    return self.to_int()

  def to_python(self):
    ...
