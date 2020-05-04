
from ctypes import *

golibcue = cdll.LoadLibrary("golibcue.so")

if sizeof(c_void_p) == 4:
  ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
  ptrdiff_t = c_int64
class GoString(Structure):
  _fields_ = [("p", c_char_p), ("n", ptrdiff_t)]

_cue_value_id_t = c_longlong

golibcue.Compile.argtypes = [POINTER(_cue_value_id_t), GoString]
golibcue.Compile.restype = c_char_p
Compile = golibcue.Compile

golibcue.ToString.argtypes = [c_longlong]
golibcue.ToString.restype = c_char_p
ToString = golibcue.ToString

golibcue.Print.argtypes = [c_longlong]
golibcue.Print.restype = None
Print = golibcue.Print

golibcue.Unifies.argtypes = [c_longlong, c_longlong]
golibcue.Unifies.restype = c_int8
Unifies = golibcue.Unifies

golibcue.Int.argtypes = [POINTER(c_longlong), _cue_value_id_t]
golibcue.Int.restype = c_char_p
Int = golibcue.Int

golibcue.Float.argtypes = [POINTER(c_double), _cue_value_id_t]
golibcue.Float.restype = c_char_p
Float = golibcue.Float

golibcue.IsBottom.argtypes = [c_longlong]
golibcue.IsBottom.restype = c_int8
IsBottom = golibcue.IsBottom

golibcue.IsNull.argtypes = [c_longlong]
golibcue.IsNull.restype = c_int8
IsNull = golibcue.IsNull

golibcue.IsBool.argtypes = [c_longlong]
golibcue.IsBool.restype = c_int8
IsBool = golibcue.IsBool

golibcue.IsInt.argtypes = [c_longlong]
golibcue.IsInt.restype = c_int8
IsInt = golibcue.IsInt

golibcue.IsFloat.argtypes = [c_longlong]
golibcue.IsFloat.restype = c_int8
IsFloat = golibcue.IsFloat

golibcue.IsString.argtypes = [c_longlong]
golibcue.IsString.restype = c_int8
IsString = golibcue.IsString

golibcue.IsBytes.argtypes = [c_longlong]
golibcue.IsBytes.restype = c_int8
IsBytes = golibcue.IsBytes

golibcue.IsStruct.argtypes = [c_longlong]
golibcue.IsStruct.restype = c_int8
IsStruct = golibcue.IsStruct

golibcue.IsList.argtypes = [c_longlong]
golibcue.IsList.restype = c_int8
IsList = golibcue.IsList

golibcue.Fields.argtypes = [c_longlong]
golibcue.Fields.restype = c_longlong
Fields = golibcue.Fields

golibcue.Elems.argtypes = [c_longlong]
golibcue.Elems.restype = c_longlong
Elems = golibcue.Elems

golibcue.Next.argtypes = [c_longlong]
golibcue.Next.restype = c_int8
Next = golibcue.Next

golibcue.Label.argtypes = [c_longlong]
golibcue.Label.restype = c_char_p
Label = golibcue.Label

golibcue.Value.argtypes = [c_longlong]
golibcue.Value.restype = c_longlong
Value = golibcue.Value
