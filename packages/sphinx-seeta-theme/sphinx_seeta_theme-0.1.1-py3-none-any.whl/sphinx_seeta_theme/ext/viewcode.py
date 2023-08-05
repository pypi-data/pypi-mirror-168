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
"""Add links to module code in Python object descriptions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from docutils import nodes

import sphinx
from sphinx import addnodes
from sphinx.locale import _, __
from sphinx.pycode import ModuleAnalyzer
from sphinx.util import get_full_modname
from sphinx.util import import_module
from sphinx.util import status_iterator
from sphinx.util.nodes import make_refnode


def doctree_read(app, doctree):
    env = app.builder.env
    if app.builder.name == "singlehtml":
        return
    if app.builder.name.startswith("epub") and \
            not env.config.viewcode_enable_epub:
        return

    if not hasattr(env, '_viewcode_modules'):
        env._viewcode_modules = {}

    def has_tag(modname, fullname, docname, refname):
        entry = env._viewcode_modules.get(modname, None)
        if entry is False:
            return False
        code_tags = app.emit_firstresult('viewcode-find-source', modname)
        if code_tags is None:
            try:
                analyzer = ModuleAnalyzer.for_module(modname)
                analyzer.find_tags()
            except Exception:
                env._viewcode_modules[modname] = False
                return False
            code = analyzer.code
            tags = analyzer.tags
        else:
            code, tags = code_tags
        if entry is None or entry[0] != code:
            entry = code, tags, {}, refname
            env._viewcode_modules[modname] = entry
        _, tags, used, _ = entry
        if fullname in tags:
            used[fullname] = docname
            return fullname
        else:
            module = import_module(refname)
            value = module
            try:
                for attr in fullname.split('.'):
                    if attr:
                        value = getattr(value, attr)
                if hasattr(value, '__self__'):
                    # Maybe code is the alias of a method.
                    fullname = value.__self__.__name__ + '.' + fullname
                    if fullname in tags:
                        used[fullname] = docname
                        return fullname
                elif hasattr(value, '__name__'):
                    # Maybe code is the alias of a function.
                    fullname_v2 = value.__name__
                    if fullname_v2 in tags:
                        used[fullname_v2] = (docname, fullname)
                        return fullname
            except AttributeError:
                print('Source is not found for "{}"'.format(fullname))
        return None

    for objnode in doctree.traverse(addnodes.desc):
        if objnode.get('domain') != 'py':
            continue
        names = set()
        for signode in objnode:
            if not isinstance(signode, addnodes.desc_signature):
                continue
            modname = signode.get('module')
            fullname = signode.get('fullname')
            refname = modname
            if env.config.viewcode_follow_imported_members:
                new_modname = app.emit_firstresult(
                    'viewcode-follow-imported', modname, fullname)
                if not new_modname:
                    new_modname = get_full_modname(modname, fullname)
                modname = new_modname
            if not modname:
                continue
            fullname = signode.get('fullname')
            fullname = has_tag(modname, fullname, env.docname, refname)
            if fullname is None:
                continue
            if fullname in names:
                continue  # Only one link per name
            names.add(fullname)
            pagename = '_modules/' + modname.replace('.', '/')
            inline = nodes.inline('', _('[source]'), classes=['viewcode-link'])
            onlynode = addnodes.only(expr='html')
            onlynode += addnodes.pending_xref(
                '', inline,
                reftype='viewcode',
                refdomain='std',
                refexplicit=False,
                reftarget=pagename,
                refid=fullname,
                refdoc=env.docname,
            )
            signode += onlynode


def env_merge_info(app, env, docnames, other):
    if not hasattr(other, '_viewcode_modules'):
        return
    if not hasattr(env, '_viewcode_modules'):
        env._viewcode_modules = {}
    env_modules = env._viewcode_modules
    other_modules = other._viewcode_modules
    for k, v in other_modules.items():
        if k not in env_modules:
            env_modules[k] = v
        else:
            env_modules[k][2].update(other_modules[k][2])


def missing_reference(app, env, node, contnode):
    if node['reftype'] == 'viewcode':
        return make_refnode(
            app.builder,
            node['refdoc'],
            node['reftarget'],
            node['refid'],
            contnode)
    return None


def collect_pages(app):
    env = app.builder.env
    if not hasattr(env, '_viewcode_modules'):
        return

    highlighter = app.builder.highlighter
    urito = app.builder.get_relative_uri
    modnames = set(env._viewcode_modules)

    for modname, entry in status_iterator(
            sorted(env._viewcode_modules.items()),
            __('highlighting module code... '), "blue",
            len(env._viewcode_modules),
            app.verbosity, lambda x: x[0]):
        if not entry:
            continue
        code, tags, used, refname = entry
        # Construct a page name for the highlighted source.
        pagename = '_modules/' + modname.replace('.', '/')
        # Highlight the source using the builder's highlighter.
        if env.config.highlight_language in ('python3', 'default', 'none'):
            lexer = env.config.highlight_language
        else:
            lexer = 'python'
        highlighted = highlighter.highlight_block(code, lexer, linenos=False)
        # Split the code into lines.
        lines = highlighted.splitlines()
        # Split off wrap markup from the first line of the actual code.
        before, after = lines[0].split('<pre>')
        lines[0:1] = [before + '<pre>', after]
        # Nothing to do for the last line.
        # It always starts with </pre> anyway.
        # Now that we have code lines (starting at index 1), insert anchors for
        # the collected tags (HACK: this only works if the tag boundaries are
        # properly nested!).
        maxindex = len(lines) - 1
        for name, docname in used.items():
            type, start, end = tags[name]
            if isinstance(docname, tuple):
                docname, name = docname
            backlink = urito(pagename, docname) + '#' + refname + '.' + name
            lines[start] = (
                '<div class="viewcode-block" id="%s"><a class="viewcode-back" '
                'href="%s">%s</a>' % (name, backlink, _('[docs]')) +
                lines[start])
            lines[min(end, maxindex)] += '</div>'
        # Try to find parents (for submodules).
        parents = []
        parent = modname
        while '.' in parent:
            parent = parent.rsplit('.', 1)[0]
            if parent in modnames:
                parents.append({
                    'link': urito(pagename, '_modules/' + parent.replace('.', '/')),
                    'title': parent})
        parents.append({'link': urito(pagename, '_modules/index'),
                        'title': _('Module code')})
        parents.reverse()
        # Putting it all together.
        context = {
            'parents': parents,
            'title': modname,
            'body': (_('<h1>Source code for %s</h1>') % modname +
                     '\n'.join(lines)),
        }
        yield pagename, context, 'page.html'

    if not modnames:
        return

    html = ['\n']
    # The stack logic is needed for using nested lists for submodules.
    stack = ['']
    for modname in sorted(modnames):
        if modname.startswith(stack[-1]):
            stack.append(modname + '.')
            html.append('<ul>')
        else:
            stack.pop()
            while not modname.startswith(stack[-1]):
                stack.pop()
                html.append('</ul>')
            stack.append(modname + '.')
        html.append('<li><a href="%s">%s</a></li>\n' % (
            urito('_modules/index', '_modules/' + modname.replace('.', '/')),
            modname))
    html.append('</ul>' * (len(stack) - 1))
    context = {
        'title': _('Overview: module code'),
        'body': (_('<h1>All modules for which code is available</h1>') +
                 ''.join(html)),
    }
    yield '_modules/index', context, 'page.html'


def setup(app):
    app.add_config_value('viewcode_import', None, False)
    app.add_config_value('viewcode_enable_epub', False, False)
    app.add_config_value('viewcode_follow_imported_members', True, False)
    app.connect('doctree-read', doctree_read)
    app.connect('env-merge-info', env_merge_info)
    app.connect('html-collect-pages', collect_pages)
    app.connect('missing-reference', missing_reference)
    app.add_event('viewcode-find-source')
    app.add_event('viewcode-follow-imported')
    return {
        'version': sphinx.__display_version__,
        'env_version': 1,
        'parallel_read_safe': True,
    }
