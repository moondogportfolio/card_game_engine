def shortcut_enum_converter(value):
    try:
        return value.get_longhand()
    except AttributeError:
        return value