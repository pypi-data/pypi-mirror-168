# 🐴 sheval

Safely evaluate mathematical and logical expressions. Most operations are supported.

### Whitelisted data types
For security, only certain data types are allowed:<br>
`str`, `int`, `float`, `complex`, `list`, `tuple`, `set`, `dict`, `bool`, `bytes`, `NoneType`

## Example

```py
from sheval import sheval

_locals = dict(x=3, y=1, z=4)

sheval('x > y <= z', _locals)
```