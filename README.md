
# PyCUE

```sh
$ python
Python 3.8.2 (default, Apr  8 2020, 14:31:25)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cue
>>> cue.loads('''
... spec :: {
...   a: int
...   b: <3
... }
... one: spec & {
...   a: 3
...   b: 2
... }
... two: spec & {
...   a: 11 + 12
...   b: 1
... }
... ''')
{'one': {'a': 3, 'b': 2}, 'two': {'a': 23, 'b': 1}}
```

## Running

```sh
$ make golibcue
$ pip install requirements.txt
$ python example.py
$ python -m pytest
```
