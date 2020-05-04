
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
