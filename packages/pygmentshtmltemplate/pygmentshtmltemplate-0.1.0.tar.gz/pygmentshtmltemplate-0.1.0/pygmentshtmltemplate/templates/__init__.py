import mako.template as MT
import string
from pathlib import Path
from typing import Any
from pygments.token import _TokenType

from pygmentshtmltemplate.parsers import parse
from .nodes import Line, Token, TemplateContext


Opts = dict[str, Any]

class Template:
    def __init__(self, context: TemplateContext, name: str='') -> None:
        self.context = context
        self.name = name
        
    def render_lead(self, data: Opts) -> str:
        return MT.Template(self.context.lead_parts).render(**data)

    def render_trail(self, data: Opts) -> str:
        return MT.Template(self.context.trail_parts).render(**data)

    def select_line_parts(self, data: Opts) -> tuple[str, str]:
        for line in self.context.lines:
            found = _test_keys_and_values(line.test_keys, data)
            if found:
                break
        if found:
            return line.lead_parts, line.trail_parts
        raise TemplateException('Cannot select a line')

    def render_line(self, line: str, data: Opts) -> str:
        lead, trail = self.select_line_parts(data)
        offset = self.context.line_offset()
        tmpl = MT.Template(offset + lead + line + trail)
        return tmpl.render(**data) + '\n'

    def select_token_parts(self, ttype: _TokenType, value: str, data: Opts) -> tuple[str, str]:
        for token in self.context.tokens:
            found = _test_keys_and_values(token.test_keys, data) and token.run_tests(ttype, value)
            if found:
                break
        if found:
            return token.lead_parts, token.trail_parts
        return '', ''

    def render_token(self, ttype: _TokenType, value: str, data: Opts) -> str:
        lead, trail = self.select_token_parts(ttype, value, data)
        tmpl = MT.Template(lead + value + trail)
        return tmpl.render(**data)

def _test_keys_and_values(keys: list[str], data: Opts) -> bool:
    for key in keys:
        if key not in data:
            return False
        value = data[key]
        if type(value) is int:
            value = str(value)
        if not value:
            return False
    return True
    

class TemplateException(ValueError):
    pass


DEFAULT_TEMPLATE_NAME = 'default.xml'

def from_src(src: str) -> Template:
    name = ''
    if not src:
        path = Path(__file__).parent / DEFAULT_TEMPLATE_NAME
        name = 'default'
    else:
        path = Path(src)
    return from_path(path, name)

def from_path(path: Path, name: str='') -> Template:
    if not path.is_file():
        raise ValueError(f'{path} is not a regular file')
    context = parse(path)
    return Template(context, name)


_Decl = dict[str, str]
_Selc = list[str]
_Rule = tuple[_Selc, _Decl]
WRAP_CSSRULES: list[_Rule] = [
    (['${wrap}'], {
        'counter-reset': 'li ${linenostart}',
        'padding': '.5em',
    }),
    (['${wrap} ${line}', '${wrap} ${line} ${token}'], {
        'font-family': 'Menlo, monospace',
    }),
    (['${wrap} ${line}'], {
        'white-space': 'pre-wrap',
        'list-style': 'none',
    }),
    (['${wrap} ${token}'], {
        'background-color': 'transparent',
    }),
    (['${wrap} ${line}::before'], {
        'display': 'inline-block',
        'width': '${leadpadding}em',
        'padding-right': '1em',
        'text-align': 'right',
        'content': 'counter(li)',
        'counter-increment': 'li',
        'font-size': '.8em',
        'opacity': '.6',
    }),
]

def build_wrap_cssrules(selector_vals, **opts) -> list[_Rule]:
    setback = len(str(opts['linenostart'] + 1)) / 2 + .5
    opts = opts | {'leadpadding': max(2, setback)}
    results = []
    for sels, decl in WRAP_CSSRULES:
        sels_ = []
        for sel in sels:
            sel_vals_copies = []
            for k,v in selector_vals.items():
                if v.find(',') > 0:
                    for val in filter(str.strip, v.split(',')):
                        copied = selector_vals.copy()
                        copied[k] = val.strip()
                        sel_vals_copies.append(copied)
            if sel_vals_copies:
                for sel_vals in sel_vals_copies:
                    sels_.append(string.Template(sel).substitute(sel_vals))
            else:
                sels_.append(string.Template(sel).substitute(selector_vals))

        sels_ = [s.replace('  ', ' ') for s in sels_]
        decl_ = {}
        for p,v in decl.items():
            decl_[p] = string.Template(v).substitute(opts)
        results.append((sels_, decl_))

    if 'front_base_color' in opts and opts['front_base_color']:
        for sels, decl in results:
            if filter(lambda sel: sel.find('::before') > 0, sels):
                decl['color'] = opts['front_base_color']
                
    return results
