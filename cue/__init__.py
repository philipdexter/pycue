
import cue.golibcue as lc

class CueError(Exception):
  ...

class CueValue:
  def __init__(self, s):
    if isinstance(s, str):
      bs = s.encode('UTF-8')
      out_cue_value_id = lc._cue_value_id_t()
      res = lc.Compile(lc.byref(out_cue_value_id), lc.GoString(bs, len(s)))
      if res is not None:
        raise CueError(res.decode('UTF-8'))
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

  def to_bool(self):
    if not self.is_bool():
      raise ValueError('can only convert cue boolean values to bools')
    out_bool = lc._go_bool()
    res = lc.Bool(lc.byref(out_bool), self._cue_value_id)
    if res is not None:
      raise CueError(res.decode('UTF-8'))
    return bool(out_bool.value)

  def __bool__(self):
    return self.to_bool()

  def to_int(self):
    if not self.is_int():
      raise ValueError('can only convert cue integer values to ints')
    out_int = lc._go_int_64()
    res = lc.Int(lc.byref(out_int), self._cue_value_id)
    if res is not None:
      raise CueError(res.decode('UTF-8'))
    return out_int.value

  def __int__(self):
    return self.to_int()

  def to_float(self):
    if not self.is_float():
      raise ValueError('can only convert cue float values to floats')
    out_float = lc._go_float_64()
    res = lc.Float(lc.byref(out_float), self._cue_value_id)
    if res is not None:
      raise CueError(res.decode('UTF-8'))
    return out_float.value

  def to_string(self):
    if not self.is_string():
      raise ValueError('can only convert cue string values to strings')
    out_string = lc.c_char_p()
    res = lc.String(lc.byref(out_string), self._cue_value_id)
    if res is not None:
      raise CueError(res.decode('UTF-8'))
    return out_string.value.decode('UTF-8')

  def __float__(self):
    return self.to_float()

  def to_dict(self):
    if not self.is_struct():
      raise ValueError('can only convert cue struct values to dicts')
    return {k: v.to_python() for k, v in self}

  def to_list(self):
    if not self.is_list():
      raise ValueError('can only convert cue struct values to dicts')
    return [v.to_python() for v in self]

  def to_python(self):
    if self.is_bool():
      return self.to_bool()
    if self.is_int():
      return self.to_int()
    if self.is_float():
      return self.to_float()
    if self.is_string():
      return self.to_string()
    if self.is_struct():
      return self.to_dict()
    if self.is_list():
      return self.to_list()
    raise ValueError(f'cannot convert \'{str(self)}\' to python')

def compile(s):
  return CueValue(s)

def loads(s):
  return CueValue(s).to_python()

def dumps(d):
  out = ''
  if isinstance(d, dict):
    out += '{'
    for k, v in d.items():
      if isinstance(k, str):
        out += k
      else:
        out += str(k)
      out += ':'
      out += dumps(v)
    out += '}'
  elif isinstance(d, list):
    out += '['
    for i, v in enumerate(d):
      out += dumps(v)
      if i != len(d) - 1:
        out += ','
    out += ']'
  elif isinstance(d, bool):
    if d:
      out += 'true'
    else:
      out += 'false'
  elif isinstance(d, str):
    out += f'"{d}"'
  else:
    out += str(d)
  return out
