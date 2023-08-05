# ------------------------------------------------------------
# Copyright (c) 2017-present, SeetaTech, Co.,Ltd.
#
# Licensed under the BSD 2-Clause License.
# You should have received a copy of the BSD 2-Clause License
# along with the software. If not, See,
#
#     <https://opensource.org/licenses/BSD-2-Clause>
#
# ------------------------------------------------------------
"""Add external links to module code in Python object descriptions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from sphinx.pycode import ModuleAnalyzer
from sphinx.util import get_full_modname
from sphinx.util import import_module


def linkcode_resolve_impl(domain, info):
    """Return an url for the given code."""
    if domain != 'py':
        return None
    if not info['module']:
        return None
    get_code_url = info.get('get_code_url', None)
    if get_code_url is None:
        return None
    modname, fullname = info['module'], info['fullname']
    full_modname = get_full_modname(modname, fullname)
    if full_modname is None:
        return None
    try:
        analyzer = ModuleAnalyzer.for_module(full_modname)
        analyzer.find_tags()
        _, tags = analyzer.code, analyzer.tags
    except Exception:
        return None
    code_location = tags.get(fullname, (None, None, None))[1:3]
    if code_location[0] is None:
        module = import_module(modname)
        value = module
        try:
            for attr in fullname.split('.'):
                if attr:
                    value = getattr(value, attr)
            if hasattr(value, '__self__'):
                # Maybe code is the alias of a method
                fullname = value.__self__.__name__ + '.' + fullname
                code_location = tags.get(fullname, (None, None, None))[1:3]
            elif hasattr(value, '__name__'):
                # Maybe code is the alias of a function
                fullname = value.__name__
                code_location = tags.get(fullname, (None, None, None))[1:3]
        except AttributeError:
            pass
    if code_location[0] is None:
        return None
    return get_code_url(full_modname, code_location)
