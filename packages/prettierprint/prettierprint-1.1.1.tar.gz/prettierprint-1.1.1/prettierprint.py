from multiprocessing import parent_process
from typing import Any

OUTLIST = []


def print(data: Any, ind_char: str=' ', ind_incr: int=6, item_sep: str='\n', top_level_sep: str='', list_item_char: str=' - ', depth: int=None, print_func=print):
    """
    Print data structures in a clean, easy to read format.

    :param data:            Any     The object to be clean-printed
    :param ind_char:        str     The string character for showing hierarchy depth. Default: '\t'
    :param item_sep:        str     The string character for separating individual items. Default: '\n'
    :param top_level_sep:   str     The string to use for visually separating items in a list, set, or tuple.
    :param depth:           int     The maximum level of hierarchy depth to display. Default: None (all levels)
    :param print_func:      func    The print function to use. Default is Python's built-in 'print'
    """
    output = format_output(data, 
                        ind_char=ind_char, 
                        ind_incr=ind_incr,
                        item_sep=item_sep, 
                        top_level_sep=top_level_sep, 
                        list_item_char=list_item_char, 
                        depth=depth)
    print_func(output)


def format_output(data: Any, ind_char: str=' ', ind_incr: int=6, item_sep: str='\n', top_level_sep: str='', list_item_char: str=' - ', depth: int=None) -> str:
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
    _format(data, 
            ind_char=ind_char,
            ind_incr=ind_incr,
            top_level_sep=top_level_sep, 
            list_item_char=list_item_char, 
            depth=depth)
    for o in OUTLIST:
        if o == list_item_char:
            output += o
        else:
            output += (o + item_sep)
    return output


def _format(data: Any, _indent: int=0, ind_char: str=' ', ind_incr: int=6, top_level_sep: str='', list_item_char: str='- ', _parent_is_list: bool=None, depth: int=None):
    """Recursive function to process an input object for printing"""
    if depth:
        if depth < _indent:
            OUTLIST.append(f'{ind_char * _indent * ind_incr} [...]')
            return
    if _isstr(data) or _isnum(data):
        if _parent_is_list:
            OUTLIST.append(f'{ind_char * ((_indent * ind_incr) - len(list_item_char))}{list_item_char}{data}')
        else:
            OUTLIST.append(f'{ind_char * _indent * ind_incr}{data}')
    elif type(data) is dict:
        is_first = True
        for k, v in data.items():
            if is_first and _parent_is_list:
                if _isstr(v) or _isnum(v):
                    OUTLIST.append(f'{ind_char * ((_indent * ind_incr) - len(list_item_char))}{list_item_char}{k}: {v}')
                else:
                    OUTLIST.append(f'{ind_char * ((_indent * ind_incr) - len(list_item_char))}{list_item_char}{k}:')
                    _format(v, 
                            _indent=(_indent+1), 
                            ind_char=ind_char,
                            ind_incr=ind_incr,
                            top_level_sep=top_level_sep, 
                            list_item_char=list_item_char,
                            _parent_is_list=_parent_is_list,
                            depth=depth)
                is_first = False
            else:
                if _isstr(v) or _isnum(v):
                    OUTLIST.append(f'{ind_char * _indent * ind_incr}{k}: {v}')
                else:
                    OUTLIST.append(f'{ind_char * _indent * ind_incr}{k}:')
                    _format(v, 
                            _indent=(_indent+1), 
                            ind_char=ind_char,
                            ind_incr=ind_incr,
                            top_level_sep=top_level_sep, 
                            list_item_char=list_item_char,
                            _parent_is_list=_parent_is_list,
                            depth=depth)
    elif hasattr(data, '__dict__'):
        if _parent_is_list:
            OUTLIST.append(f'{ind_char * ((_indent * ind_incr) - len(list_item_char))}{list_item_char}{type(data).__name__}:')
            _parent_is_list = False
        else:
            OUTLIST.append(f'{ind_char * _indent * ind_incr}{type(data).__name__}:')
        _format(data.__dict__, 
                _indent=(_indent+1), 
                ind_char=ind_char,
                ind_incr=ind_incr,
                top_level_sep=top_level_sep, 
                list_item_char=list_item_char,
                _parent_is_list=_parent_is_list,
                depth=depth)
    elif type(data) in (list, set, tuple):
        _parent_is_list = True
        for i in data:
            if _indent == 0:
                OUTLIST.append(top_level_sep)
                _parent_is_list = False
            _format(i,
                     _indent, 
                     ind_char=ind_char,
                     ind_incr=ind_incr,
                     top_level_sep=top_level_sep, 
                     list_item_char=list_item_char,
                     _parent_is_list=_parent_is_list,
                     depth=depth)
    else:
        OUTLIST.append(f'{ind_char * _indent * ind_incr}{data}')


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
