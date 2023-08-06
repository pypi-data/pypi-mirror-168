from pygments.formatters import HtmlFormatter, html
from pygments.token import Token, _TokenType
from collections.abc import Generator
import re, pathlib
from typing import Any

from . import templates
from .templates import Template, build_wrap_cssrules


__version__ = "0.1.0"


_OptsVal = str | int | bool | set[int]
_Opts = dict[str, _OptsVal]

_options_pass_to_HtmlFormatter = (
    'style', 'title', 'filename',
    'nobackground', 'cssclass', 'classprefix', 'linenostart', 'hl_lines',
    # 'full', 'noclobber_cssfile', 'cssfile',
)

class FormatterWithTemplate(HtmlFormatter):
    name = 'FormatterWithTemplate'
    aliases = ['fmtr_tmpl']

    def __init__(self, **options) -> None:
        xopts = {}
        for k in options:
            if k in _options_pass_to_HtmlFormatter:
                xopts[k] = options[k]
        HtmlFormatter.__init__(self, **xopts)

        self._line_counter = 0
        tmp_src = options.get('template', '')
        self.template = templates.from_src(tmp_src)

    def get_style_defs(self, arg=None) -> str:
        rules = self.get_wrap_style_rules(arg)
        rules += self.get_background_style_defs(arg)
        rules += self.get_token_style_defs(arg)
        return '\n'.join(rules)

    def get_wrap_style_rules(self, arg=None) -> list[str]:
        if self.template.name != 'default':
            return []

        if arg is None:
            arg = 'ol'
        wrap_selector_vals = {
            'wrap': self.get_css_prefix(arg)(''),
            'line': 'li',
            'token': 'code'
        }
        for ttype, rules in self.style:
            if ttype is Token.Name:
                break

        front_base_color = rules['color'] and html.webify(rules['color']) or None # type:ignore
        rules = []
        for sels, decl in build_wrap_cssrules(wrap_selector_vals,
                                              front_base_color=front_base_color,
                                              linenostart=self.linenostart -1):
            rules.append(
                ', '.join(sels) + '{ ' + '; '.join([
                    k + ':' + v for k, v in decl.items()
                ]) + ' }'
            )
        return rules
    
    def _token_properties(self, ttype: _TokenType) -> _Opts:
        return {
            'token_class': self._get_css_classes(ttype), # type:ignore
            'token_type': '.'.join(ttype)
        }
    
    def format_token(self, ttype: _TokenType, part: str, opts: _Opts) -> str:
        if ttype in Token.Text and re.fullmatch(r'[ \t]*', part):
            return part
        return self.template.render_token(
            ttype,
            self._translate_parts(part)[0],
            opts | self._token_properties(ttype)
        )

    def format_lines(self, tokensource, opts: _Opts) -> Generator[tuple[str, _Opts], None, None]:
        line = ''
        self.linecount = opts['linenostart']

        for ttype, value in tokensource:
            if ttype in Token.Text and value == '\n':
                _update_options_with_lineno(self.linecount, opts)
                
                if re.fullmatch(r'[ \t]*', line):
                    yield '', opts
                else:
                    yield line, opts
                line = ''
            elif '\n' in value:
                parts = value.split('\n')
                for i in range(len(parts) -1):
                    _update_options_with_lineno(self.linecount, opts)
                    
                    part = parts[i]
                    if i == 0:
                        if part:
                            yield line + self.format_token(ttype, part, opts), opts
                        else:
                            yield line, opts
                    else:
                        if part:
                            yield self.format_token(ttype, part, opts), opts
                        else:
                            yield '', opts

                line = self.format_token(ttype, parts[i+1], opts)
            else:
                line += self.format_token(ttype, value, opts)

        if line:
            _update_options_with_lineno(self.linecount, opts)
            yield line, opts

    def format_unencoded(self, tokensource, outfile) -> None:
        opts = {
            k:self.__getattribute__(k) for k in _options_pass_to_HtmlFormatter
        }
        if not self.title:
            opts['title'] = _filename_to_title(opts.get('filename', ''))

        outfile.write(self.template.render_lead(opts))
        #import pdb; pdb.set_trace()
        empties: list[str] = []
        for line, _opts in self.format_lines(tokensource, opts):
            if line:
                while empties:
                    outfile.write(empties.pop())
                outfile.write(self.template.render_line(line, _opts))
            else:
                empties.insert(0, self.template.render_line('', _opts))

        outfile.write(self.template.render_trail(opts))

    @property
    def linecount(self) -> int:
        self._line_counter += 1
        return self._line_counter - 1

    @linecount.setter
    def linecount(self, v: int) -> None:
        self._line_counter = v


def _update_options_with_lineno(lineno: int, opts: dict[str, Any]) -> dict[str, Any]:
    opts['lineno'] = lineno
    if 'hl_lines' not in opts:
        opts['highlighted'] = False
    else:
        opts['highlighted'] = lineno in opts['hl_lines']
    return opts


def _filename_to_title(filename: str) -> str:
    if not filename:
        return ''
    path = pathlib.Path(filename)
    return path.name

