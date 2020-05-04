
import cue

i1 = cue.compile('{a: 1}')
print(i1)

i2 = cue.compile('{b: 1}')
print(i2)

print(i1.unifies_with(i2))
print(i1.unifies_with(cue.compile('{a: <3}')))
print(i1.unifies_with(cue.compile('{a: >3}')))
print(i1.unifies_with(cue.compile('{a: int, d: int}')))

for key, value in cue.compile('''
spec :: {d:int}
a : 1
b : 2
c : spec & {
  d : a
  d : int
  
}
'''):
  print(f'{key=} {value=!s}')


for val in cue.compile('''
[1,2,{a:3}]
'''):
  print(f'{val=!s}')
