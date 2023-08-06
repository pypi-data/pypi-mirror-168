import docutils.nodes
from docutils.parsers.rst import Directive, directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.util import ClassNotFound
import re, pathlib

from pygmentshtmltemplate import FormatterWithTemplate


class PygHtmlTmplRstDirective(Directive):
    """
    A syntax highlighting directive for reST with the Pygments html-formatter
    plugin `pygmentshtmltemplate`.
    This directive pygmetizes contents and passes through that html-tagged code.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'file': directives.path,
        'template': directives.path,
        'style': directives.unchanged,
        'title': directives.unchanged,
        'filename': directives.unchanged,
        'cssclass': directives.unchanged,
        'linenostart': directives.nonnegative_int,
        'hl_lines': directives.unchanged,
        'classprefix': directives.unchanged,
    }
    has_content = True

    def run(self):
        opts = {}
        code_fmt = self.arguments[0]

        if (idx := code_fmt.find(':')) >= 0:
            for m in re.finditer(r':([^:]+):\s*([^: ]*)', code_fmt[idx:]):
                opts[m.group(1)] = m.group(2)
            code_fmt = code_fmt[:idx].strip()
        if not code_fmt:
            raise self.error('Require a name of language as an argument')

        if 'template' not in opts:
            opts['template'] = self.options.get('template', '')

        if 'hl_lines' in self.options and self.options['hl_lines'].find(',') >= 0:
            try:
                opts['hl_lines'] = ' '.join([str(int(n)) for n in self.options['hl_lines'].split(',')])
            except ValueError:
                raise self.error('The value of :hl_lines: option should be formatted `<int> <int> ...`')
        opts = self.options | opts

        if self.content:
            code = '\n'.join(self.content)
        elif 'file' in opts:
            path = pathlib.Path(opts['file'])
            if not path.is_file():
                raise self.error(f'{path} is not a regular file')
            with open(path) as f:
                code = f.read()

            if 'filename' not in opts or not opts['filename']:
                opts['filename'] = path.name
        else:
            raise self.error('Requires a contents block or a :file: option')

        try:
            lexer = get_lexer_by_name(code_fmt)
        except ClassNotFound as cnf:
            if 'filename' in opts and opts['filename']:
                try:
                    lexer = get_lexer_for_filename(opts['filename'])
                except ClassNotFound:
                    pass
        finally:
            if not lexer:
                raise self.error(f'{cnf}')

        try:
            frmtr = FormatterWithTemplate(**opts)
            rawhtml = highlight(code, lexer, frmtr)
        except Exception as e:
            raise self.error(f'Failed highlighting: {e}')

        node = docutils.nodes.raw('', rawhtml, classes=opts.get('class', []), format='html')
        node.source, node.line = self.state_machine.get_source_and_line(self.lineno)
        return [node]
