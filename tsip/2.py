import types

class C(object):

    _attrs = ['the first value', 'second value', 'last value']
    _values = [1,2,3]

    def _find_value(self, key, exception=NameError):
        # TODO: return just the index so setting values can be done, too.

        # *key*
        indexes = filter(lambda (i,attr): attr.find(key) > -1, enumerate(self._attrs))
        if len(indexes) == 1:
            return self._values[indexes[0][0]]

        # key*
        indexes = filter(lambda (i,attr): attr.startswith(key), enumerate(self._attrs))
        if len(indexes) == 1:
            return self._values[indexes[0][0]]

        # *key
        indexes = filter(lambda (i,attr): attr.endswith(key), enumerate(self._attrs))
        if len(indexes) == 1:
            return self._values[indexes[0][0]]

        raise exception


    def __getitem__(self, key):
        if isinstance(key, types.IntType):
            return self._values[key]
        elif isinstance(key, types.SliceType):
            return self._values[key]
        elif isinstance(key, types.StringType):
            return self._find_value(key, KeyError)
        else:
            raise KeyError(str(key))


    def __getattr__(self, name):
        return self._find_value(name, NameError)


c = C()

assert c[0] == 1
assert c[1] == 2
assert c[2] == 3

assert c['the first value'] == 1
assert c['second value'] == 2
assert c['last value'] == 3
assert c['first'] == 1
assert c['second'] == 2
assert c['last'] == 3
assert c['the'] == 1

assert c.first == 1
assert c.second == 2
assert c.last == 3
assert c.the == 1

c.value



