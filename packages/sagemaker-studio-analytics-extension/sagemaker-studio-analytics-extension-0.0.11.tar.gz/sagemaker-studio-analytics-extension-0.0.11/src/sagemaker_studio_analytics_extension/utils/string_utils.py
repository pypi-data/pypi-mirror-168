def is_not_blank(string):
    return bool(string and string.strip())


def is_blank(string):
    return not is_not_blank(string)
