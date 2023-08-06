from hbutils.reflection import quick_import_object


def _import_object(item):
    retval, _, _ = quick_import_object(item)
    return retval


class PyImport:
    def __getattr__(self, item):
        return _import_object(item)

    def __getitem__(self, item):
        return _import_object(item)

    def __repr__(self):
        return f'<{type(self).__name__}>'
