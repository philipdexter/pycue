
from ctypes import *
import pathlib

try:
  golibcue = cdll.LoadLibrary(pathlib.Path(__file__).parent.absolute().joinpath('_golibcue.so'))
except OSError:
  print('Could not find _golibcue.so, have you run `make golibcue`?')
  exit(1)

if sizeof(c_void_p) == 4:
  ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
  ptrdiff_t = c_int64
class GoString(Structure):
  _fields_ = [("p", c_char_p), ("n", ptrdiff_t)]

_go_int_64 = c_longlong
_go_bool = c_ubyte
_go_float_64 = c_double
_cue_value_id_t = _go_int_64
_cue_iter_id_t = _go_int_64

golibcue.Compile.argtypes = [POINTER(_cue_value_id_t), GoString]
golibcue.Compile.restype = c_char_p
Compile = golibcue.Compile

golibcue.ToString.argtypes = [_cue_value_id_t]
golibcue.ToString.restype = c_char_p
ToString = golibcue.ToString

golibcue.Print.argtypes = [_cue_value_id_t]
golibcue.Print.restype = None
Print = golibcue.Print

golibcue.Unifies.argtypes = [_cue_value_id_t, _cue_value_id_t]
golibcue.Unifies.restype = _go_bool
Unifies = golibcue.Unifies

golibcue.Bool.argtypes = [POINTER(_go_bool), _cue_value_id_t]
golibcue.Bool.restype = c_char_p
Bool = golibcue.Bool

golibcue.Int.argtypes = [POINTER(_go_int_64), _cue_value_id_t]
golibcue.Int.restype = c_char_p
Int = golibcue.Int

golibcue.Float.argtypes = [POINTER(_go_float_64), _cue_value_id_t]
golibcue.Float.restype = c_char_p
Float = golibcue.Float

golibcue.String.argtypes = [POINTER(c_char_p), _cue_value_id_t]
golibcue.String.restype = c_char_p
String = golibcue.String

golibcue.IsBottom.argtypes = [_cue_value_id_t]
golibcue.IsBottom.restype = _go_bool
IsBottom = golibcue.IsBottom

golibcue.IsNull.argtypes = [_cue_value_id_t]
golibcue.IsNull.restype = _go_bool
IsNull = golibcue.IsNull

golibcue.IsBool.argtypes = [_cue_value_id_t]
golibcue.IsBool.restype = _go_bool
IsBool = golibcue.IsBool

golibcue.IsInt.argtypes = [_cue_value_id_t]
golibcue.IsInt.restype = _go_bool
IsInt = golibcue.IsInt

golibcue.IsFloat.argtypes = [_cue_value_id_t]
golibcue.IsFloat.restype = _go_bool
IsFloat = golibcue.IsFloat

golibcue.IsString.argtypes = [_cue_value_id_t]
golibcue.IsString.restype = _go_bool
IsString = golibcue.IsString

golibcue.IsBytes.argtypes = [_cue_value_id_t]
golibcue.IsBytes.restype = _go_bool
IsBytes = golibcue.IsBytes

golibcue.IsStruct.argtypes = [_cue_value_id_t]
golibcue.IsStruct.restype = _go_bool
IsStruct = golibcue.IsStruct

golibcue.IsList.argtypes = [_cue_value_id_t]
golibcue.IsList.restype = _go_bool
IsList = golibcue.IsList

golibcue.Fields.argtypes = [_cue_value_id_t]
golibcue.Fields.restype = _cue_iter_id_t
Fields = golibcue.Fields

golibcue.Elems.argtypes = [_cue_value_id_t]
golibcue.Elems.restype = _cue_iter_id_t
Elems = golibcue.Elems

golibcue.Next.argtypes = [_cue_iter_id_t]
golibcue.Next.restype = _go_bool
Next = golibcue.Next

golibcue.Label.argtypes = [_cue_iter_id_t]
golibcue.Label.restype = c_char_p
Label = golibcue.Label

golibcue.Value.argtypes = [_cue_iter_id_t]
golibcue.Value.restype = _cue_value_id_t
Value = golibcue.Value
