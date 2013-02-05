from functools import wraps
import re
import tokenize

import pep8


def e201(line, cursor):
    """Fixes whitespace after character"""
    # Cursor points to the character
    return ''.join([line[:cursor], line[cursor:].lstrip()])


def e203(line, cursor):
    """Removes whitespace before character"""
    # Cursor points to the whitespace, not the character
    return ''.join([line[:cursor].rstrip(), line[cursor:].lstrip()])

e202 = e203

def e225(line, cursor):
    """fixes missing whitespace around operator."""
    return ' '.join([line[:cursor], line[cursor:]])

e226 = e225


def e231(line, cursor):
    """fixes missing white space after ','"""
    tokens = re.split(",(\S)", line)
    return "".join(", ".join(tokens[i:i + 2]) for i in range(0, len(tokens), 2))


def e261(line, cursor):
    """fixes at least two spaces before inline comment"""
    return line[:cursor].rstrip() + "  " + line[cursor:]


def e262(line, cursor):
    """fixes inline comment should start with '# '"""
    i = cursor + 1
    return line[:i] + " " + line[i:].lstrip()


def e302(line, cursor):
    """fixes expected 2 lines, found 1."""
    return "\n" + line


'''
def e303(line):
    """fixes too many blank lines (2)"""
    return ""
'''

def e401(line, cursor):
    """Fixes multiple imports on a single line"""
    imports = line.strip()[len('import '):].split(',')
    return "\n".join("import " + _import.strip() for _import in imports)


'''
def e701(line):
    """fixes multiple statements on one line (colon)"""
    i = line.index(":")
    return line[:i] + "\n" + line[i:]
'''


def w191(line, cursor):
    """fixes W191 indentation contains tabs."""
    return line.expandtabs()


def w291(line, cursor):
    """fixes trailing whitespace."""
    return line.rstrip() + "\n"


def w292(line, cursor):
    """Fixes missing blank line at the end of the file"""
    return line + "\n"


def w293(line, cursor):
    """fixes blank line contains whitespace."""
    return "\n"


def w391(line, cursor):
    """Removes blank lines at the ends of files"""
    return ''



if __name__ == "__main__":
    import doctest
    doctest.testmod()
