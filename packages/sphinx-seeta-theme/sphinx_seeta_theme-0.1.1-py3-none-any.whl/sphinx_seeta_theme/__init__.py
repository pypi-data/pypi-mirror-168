# ------------------------------------------------------------
# Copyright (c) 2017-present, SeetaTech, Co.,Ltd.
#
# Licensed under the BSD 2-Clause License.
# You should have received a copy of the BSD 2-Clause License
# along with the software. If not, See,
#
#      <https://opensource.org/licenses/BSD-2-Clause>
#
# ------------------------------------------------------------
"""Sphinx seeta theme."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import commonmark
from sphinx.util.docfields import GroupedField
from sphinx.util.docfields import TypedField
from sphinx.writers.html import HTMLTranslator

from sphinx_seeta_theme.version import version as __version__


class HTMLTranslatorV2(HTMLTranslator):
    """Custom html translator."""

    def visit_desc_signature(self, node):
        self.body.append(self.starttag(node, 'dt', '', CLASS='descsignature'))

    def visit_desc_parameterlist(self, node):
        HTMLTranslator.visit_desc_parameterlist(self, node)
        self.num_params = self.required_params_left

    def depart_desc_parameterlist(self, node):
        if self.num_params > 1:
            self.body.append('<br>')
        HTMLTranslator.depart_desc_parameterlist(self, node)

    def visit_desc_parameter(self, node):
        if self.first_param:
            self.first_param = 0
            if self.num_params > 1:
                self.body.append('<br>&emsp;&emsp;')
        elif not self.required_params_left:
            self.body.append(self.param_separator)
        if self.optional_param_level == 0:
            self.required_params_left -= 1

    def depart_desc_parameter(self, node):
        if self.required_params_left:
            self.body.append(self.param_separator)
            self.body.append('<br>&emsp;&emsp;')

    def visit_desc_content(self, node):
        self.body.append(self.starttag(node, 'dd', '', CLASS='desccontent'))

    def visit_field(self, node):
        HTMLTranslator.visit_field(self, node)
        self.body[-1] = self.starttag(node, 'dl', '', CLASS='field')

    def depart_field(self, node):
        HTMLTranslator.depart_field(self, node)
        self.body[-1] = '</dl>\n'

    def visit_field_list(self, node):
        HTMLTranslator.visit_field_list(self, node)
        self.body.pop()
        self.body.pop()

    def depart_field_list(self, node):
        HTMLTranslator.depart_field_list(self, node)
        self.body.pop()

    def visit_field_name(self, node):
        HTMLTranslator.visit_field_name(self, node)
        atts = {}
        if self.in_docinfo:
            atts['class'] = 'docinfo-name'
        else:
            atts['class'] = 'field-name'
        if (self.settings.field_name_limit
                and len(node.astext()) > self.settings.field_name_limit):
            atts['colspan'] = 2
        self.body[-1] = self.starttag(node, 'dt', '', **atts)

    def depart_field_name(self, node):
        HTMLTranslator.depart_field_name(self, node)
        self.body[-2] = ':</dt>'

    def visit_field_body(self, node):
        HTMLTranslator.visit_field_body(self, node)
        self.body[-1] = self.starttag(node, 'dd', '', CLASS='field-body')

    def depart_field_body(self, node):
        HTMLTranslator.depart_field_body(self, node)
        self.body[-1] = '</dd>\n'


def get_html_theme_path():
    """Return list of HTML theme paths."""
    return [os.path.abspath(os.path.dirname(__file__))]


# Application API
def setup(app, custom_html_translater=None):
    """Custom application setup."""

    def docstring_with_markdown(app, what, name, obj, options, lines):
        """Parse and update the markdown code block in docstring."""
        languages = ['```cpp', '```python', '```shell']
        update_docstring = False
        enter_highlight_scope = False
        output_lines, highlight_lines = [], []
        for line in lines:
            if line in languages:
                highlight_lines.append(line)
                update_docstring = True
                enter_highlight_scope = True
            elif enter_highlight_scope:
                highlight_lines.append(line)
                if line == '```':
                    # Termination
                    highlight_content = '\n'.join(highlight_lines)
                    ast = commonmark.Parser().parse(highlight_content)
                    rst = commonmark.ReStructuredTextRenderer().render(ast)
                    for rst_line in rst.splitlines():
                        output_lines.append(rst_line)
                    highlight_lines.clear()
                    enter_highlight_scope = False
            else:
                output_lines.append(line)
        if update_docstring:
            lines.clear()
            for line in output_lines:
                lines.append(line)

    app.connect('autodoc-process-docstring', docstring_with_markdown)
    app.set_translator('html', custom_html_translater or HTMLTranslatorV2)

    add_html_theme = getattr(app, 'add_html_theme', None)
    if add_html_theme is not None:
        add_html_theme('seeta', get_html_theme_path()[0])

    return {'parallel_read_safe': True}


# Patching
def make_field_v2(self, *args, **kwargs):
    """Disable the collapse of arguments and raises."""
    self.can_collapse = False
    return self.make_field_v1(*args, **kwargs)


GroupedField.make_field_v1 = GroupedField.make_field
TypedField.make_field_v1 = TypedField.make_field
GroupedField.make_field = make_field_v2
TypedField.make_field = make_field_v2
