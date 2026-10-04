# Lesson 4: Lists, tuples, dictionaries, and shared objects

[Course home](../../README.md) · [Previous](../03-control-flow/README.md) · [Next: functions](../05-function/README.md)

## What you will learn

- Store ordered measurements in a list and access them by index or slice.
- Represent fixed sequences with tuples and labelled records with dictionaries.
- Iterate over measurements and use `len` to count them.
- Distinguish assignment, mutation, and copying.

Run the complete example from the project root:

```sh
uv run python lesson/04-collection/example.py
```

The inline temperatures are synthetic teaching values, not experimental data.
Their units are degrees Celsius, and their mean is easy to check by hand.

## Store values in a list

```python
temperature_list_c = [20.0, 21.0, 19.0]
```

Square brackets and comma-separated values create a list. A list is an ordered
collection that can change after creation. It can contain different types, but
a measurement series is clearer when all elements have consistent meaning and
units. An empty list is written `[]`.

`len(temperature_list_c)` calls a built-in function that returns the number of items.
Here the result is 3, an integer. It counts entries, not bytes or physical size.

## Index individual elements

```python
print(temperature_list_c[0])
print(temperature_list_c[-1])
```

Putting an integer inside brackets after a list name selects an element.
Python indexing starts at zero: indices 0, 1, and 2 select the first, second,
and third values. Negative indices count from the end; `-1` selects the last.
For a nonempty list of length N, valid indices range from `-N` through `N-1`.
An out-of-range index raises `IndexError`. An empty list has no valid index.

These brackets are an operation on an existing list; brackets surrounding
comma-separated values create a new list. Context distinguishes the two uses.

## Select a slice

```python
print(temperature_list_c[0:2])
print(temperature_list_c[:2])
```

Both print `[20.0, 21.0]`. A slice selects a subsequence. The start is included
and the stop is excluded, just as with `range`. Omitting the start means the
beginning; omitting the stop means the end. `temperature_list_c[1:]` selects all
but the first value. Unlike an individual index, a stop beyond the end is
clipped; `temperature_list_c[:100]` is valid for this short list.

You can specify a stride, as in `temperature_list_c[::2]`, to take every second
item. A zero stride is invalid. Ordinary list slices create a new outer list.
NumPy arrays in lesson 8 often behave differently, so remember which type you
are using.

## Change a list

```python
temperature_list_c[0] = 18.5
temperature_list_c.append(22.0)
```

Assignment to an indexed position replaces that element. `.append(22.0)` adds
one item at the end. The example script appends but skips the replacement,
so its readings are `[20.0, 21.0, 19.0, 22.0]`. The dot selects a method, an
operation belonging to this object; parentheses call the method. `append`
changes the existing list and returns `None`, Python's value for "no result".
Therefore write
`temperature_list_c.append(22.0)`, not
`temperature_list_c = temperature_list_c.append(22.0)`; the latter replaces your list
name with `None`.

A list is mutable: its contents can change. A mutation differs from assigning
a name to a completely new list. This distinction matters when several names
refer to the same object.

## Iterate directly over values

```python
total_c = 0.0
for temperature_c in temperature_list_c:
    total_c = total_c + temperature_c
mean_c = total_c / len(temperature_list_c)
```

Lists are iterable, so `for` can supply each value directly without using
indices or `range`. This is clearer when you only need the values. The mean
requires at least one measurement; an empty list would cause division by zero.
Keep the same unit for every entry. The example's four temperatures sum to
82 °C, giving an arithmetic mean of 20.5 °C.

## Use a tuple for a fixed sequence

```python
position_m = (1.0, 2.0, 3.0)
print(position_m[2])
```

The commas create a tuple, usually enclosed in parentheses for readability.
A tuple preserves order, supports indexing and `len`, and cannot have elements
replaced or appended. Attempting `position_m[2] = 4.0` raises `TypeError`.
A one-element tuple needs a trailing comma, `(1.0,)`; `(1.0)` is just a number
in grouping parentheses. Tuples suit coordinates with a fixed agreed order.
Their immutability concerns the tuple's entries; a mutable object stored inside
a tuple can still change. This example contains only immutable numbers.

## Label fields with a dictionary

```python
metadata = {"sample": "trial A", "unit": "deg C", "count": 4}
print(metadata["sample"])
metadata["count"] = 5
```

Braces create a dictionary mapping keys to values. A colon separates each key
from its value, and commas separate entries. A key such as `"sample"` labels
a field; it is not a numerical position. Dictionaries are mutable. Assigning
to an existing key replaces its value; assigning to a new key adds an entry.
Looking up a missing key raises `KeyError`. Repeating a key during construction
keeps its last value, so use distinct keys for distinct fields.

`"sample" in metadata` is a Boolean membership test for a key. The same `in`
operator tests values in a list. Iterating `for key in metadata:` supplies keys
in insertion order. `len(metadata)` counts keys. A dictionary's field names
document meaning, but the values still require you to keep units consistent.
When Python prints a whole container, strings inside it keep their quotes,
as in `{'sample': 'trial A'}`, so the string `'4'` stays distinguishable from
the number `4`.

## Assignment shares; a copy separates

```python
reading_alias = temperature_list_c
reading_copy = temperature_list_c.copy()
reading_alias[0] = 99.0
```

The first line binds another name to the same list object. Changing that object
through either name is visible through both. It does not duplicate the list.
The `.copy()` method creates a new list with the same entries. Replacing an
entry in either list never affects the other. Because these entries are
immutable numbers, they cannot be changed in place either, so the two lists
are fully independent.

This is a shallow copy: nested mutable objects would remain shared. We do not
need nested containers here, but do not assume `.copy()` recursively duplicates
all data. It is the contents of an object, rather than the variable name, that
are mutable or immutable.

## Expected output

<!-- check-output: example.py -->
```text
Readings: [20.0, 21.0, 19.0, 22.0]
First reading: 20.0
Last reading: 22.0
First two readings: [20.0, 21.0]
Mean temperature: 20.50 deg C
Position (m): (1.0, 2.0, 3.0)
Sample: trial A
Count: 4
Original after alias change: [99.0, 21.0, 19.0, 22.0]
Copy retains old readings: [20.0, 21.0, 19.0, 22.0]
```

## Common mistakes

- The first entry is at index 0, and a slice excludes its stop index.
- Assigning a list to another name creates an alias, not an independent copy.
- List `+` concatenates lists rather than adding measurements elementwise.
- An empty measurement list cannot be averaged by dividing by `len`.
- Modifying a list's length while iterating over it can skip or repeat work.
  Build a separate result list when you need to transform its structure.

## Practice and recap

Try [the three exercises](exercise.md), then read [solution.py](solution.py).

```sh
uv run python lesson/04-collection/solution.py
```

You can now store and traverse measurements, represent coordinates and records,
and reason about shared mutable objects. Next, organize calculations into
functions with clear inputs and returned results.
