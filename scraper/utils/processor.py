import inspect

try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest


class BaseProcessor(object):
    def __init__(self):
        super(BaseProcessor, self).__init__()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self))

    def __str__(self):
        argspec = inspect.getargspec(self.__init__)
        args = argspec.args
        defaults = argspec.defaults or []
        joined = reversed(list(izip_longest(reversed(args), reversed(defaults), fillvalue=object())))
        next(joined)  # Skip self
        values = []
        for attribute, default in joined:
            value = getattr(self, attribute)
            if value == default:
                continue
            values.append(repr(value))
        return ', '.join(values)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(str(self))


class Field(BaseProcessor):
    def __init__(self, name, selector, processors=None, required=False):
        super().__init__()
        if processors is None:
            processors = []
        self.name = name
        self.selector = selector
        self.processors = processors
        self.required = required


class Item(BaseProcessor):
    def __init__(self, item, name, selector, fields):
        super().__init__()
        self.item = item
        self.name = name
        self.selector = selector
        self.fields = fields
