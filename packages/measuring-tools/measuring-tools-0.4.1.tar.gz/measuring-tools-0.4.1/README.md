# Measuring Tools
__A Python Module to help deal with measurments in an object oriented way.__

---
An Object can be converted from one measurment to another.

```python
from measuring_tools.length import Length

# Convert From One Length To Another
length1 = Length(value=1, measurement='yard')
length2 = length1.to_meter()

print(length2)

# Output
Length(value=0.9144, measurement='meter')
```

---
Two objects are designed to interact with one another even if measurments are different.

Example:
``` python
from measuring_tools.length import Length

# Two Lengths - One In Meters, One In Yards
length1 = Length(value=1, measurement='meter')
length2 = Length(value=1, measurement='yard')

print(length1 + length2)

# Output
Length(value=1.9144, measurement='meter')
```

In the example above, length two is converted from yard to meter and then added to length1. The output is a new object separate from length1 and length2.

---

Inplace operations are also available.

```python
from measuring_tools.length import Length

# Inplace Subtraction
football_field = Length(value=100, measurement='yard')
football_field -= 25

print(football_field)

# Output
Length(value=75, measurement='yard')
```
In the example above, the value of football_field is modified directly. The output is the same as object.

---