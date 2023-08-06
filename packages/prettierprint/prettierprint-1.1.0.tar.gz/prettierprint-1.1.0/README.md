# prettierprint
Python module for clean, human-readable printing of data structures.

## Quickstart
### Install
`pip install prettierprint`

### Usage
Basic:
```python
from prettierprint import print

some_data = {'key': 'value', 'list': [{'name': 'Hello', 'attr_A': 'foo', 'attr_B': 'bar'}, {'name': 'World', 'attr_A': 'bar', 'attr_B': 'foo'}]}

print(some_data)
```
Result:
```
key: value
list:
    - name: Hello
      attr_A: foo
      attr_B: bar
    - name: World
      attr_A: bar
      attr_B: foo
```

