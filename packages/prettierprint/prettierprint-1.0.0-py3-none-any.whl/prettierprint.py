from typing import Any

OUTLIST = []


def print(data: Any, ind_char: str='\t', item_sep: str='\n', top_level_sep: str=None, depth: int=None, print_func=print):
    """
    Print data structures in a clean, easy to read format.

    :param data:            Any     The object to be clean-printed
    :param ind_char:        str     The string character for showing hierarchy depth. Default: '\t'
    :param item_sep:        str     The string character for separating individual items. Default: '\n'
    :param top_level_sep:   str     The string to use for visually separating items in a list, set, or tuple.
    :param depth:           int     The maximum level of hierarchy depth to display. Default: None (all levels)
    :param print_func:      func    The print function to use. Default is Python's built-in 'print'
    """
    output = format_output(data, ind_char=ind_char, item_sep=item_sep, top_level_sep=top_level_sep, depth=depth)
    print_func(output)


def format_output(data: Any, ind_char: str='\t', item_sep: str='\n', top_level_sep: str=None, depth: int=None) -> str:
    """
    Print data structures in a clean, easy to read format.

    :param data:            Any     The object to be clean-printed
    :param ind_char:        str     The string character for showing hierarchy depth. Default: '\t'
    :param item_sep:        str     The string character for separating individual items. Default: '\n'
    :param top_level_sep:   str     The string to use for visually separating items in a list, set, or tuple.
    :param depth:           int     The maximum level of hierarchy depth to display. Default: None (all levels)

    :return     str     Returns a formatted string
    """
    output = ''
    _format(data, ind_char=ind_char, top_level_sep=top_level_sep, depth=depth)
    for o in OUTLIST:
        output += (o + item_sep)
    return output


def _format(data: Any, _indent: int=0, ind_char: str='\t', top_level_sep: str=None, depth: int=None):
    """Recursive function to process an input object for printing"""
    if depth:
        if depth < _indent:
            OUTLIST.append(f'{ind_char * _indent} [...]')
            return
    if _isstr(data) or _isnum(data):
        OUTLIST.append(f'{ind_char * _indent}{data}')
    elif type(data) is dict:
        for k, v in data.items():
            if _isstr(v) or _isnum(v):
                OUTLIST.append(f'{ind_char * _indent}{k}: {v}')
            else:
                OUTLIST.append(f'{ind_char * _indent}{k}:')
                _format(v, _indent=(_indent+1), ind_char=ind_char, top_level_sep=top_level_sep, depth=depth)
    elif hasattr(data, '__dict__'):
        OUTLIST.append(f'{ind_char * _indent}{type(data).__name__}:')
        _format(data.__dict__, _indent=(_indent+1), ind_char=ind_char, top_level_sep=top_level_sep, depth=depth)
    elif type(data) in (list, set, tuple):
        for i in data:
            if _indent == 0 and top_level_sep:
                OUTLIST.append(top_level_sep)
            _format(i, _indent, ind_char=ind_char, top_level_sep=top_level_sep, depth=depth)
            OUTLIST.append('')
    else:
        OUTLIST.append(f'{ind_char * _indent}{data}')


def _isstr(data: Any) -> bool:
    return type(data) is str


def _isnum(data: Any) -> bool:
    if not _isstr(data):
        try:
            int(data)
            return True
        except TypeError:
            return False
    else:
        return False
