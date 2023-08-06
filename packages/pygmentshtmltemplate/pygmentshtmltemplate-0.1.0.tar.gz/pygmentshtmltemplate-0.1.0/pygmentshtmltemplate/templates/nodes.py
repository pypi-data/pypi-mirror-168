from dataclasses import dataclass, field, InitVar
from pygments.token import _TokenType, string_to_tokentype
from pygments.token import Token as pygToken
import re, enum


@dataclass
class Node:
    name: str
    attrs: dict = field(default_factory=dict)
    content: str = field(init=False, default='')

    def start_tag(self) -> str:
        attrs = ''
        for p in self.attrs:
            if p.startswith('_'):
                continue
            attrs += f' {p}="{self.attrs[p]}"'
        return f'<{self.name}{attrs}>'

    def end_tag(self) -> str:
        return f'</{self.name}>'


@dataclass
class Line:
    lead_parts: str = ''
    trail_parts: str = ''
    test_keys: list[str] = field(init=False, default_factory=list)
    _end_lead_parts: bool = field(init=False, default=False)

    def end_lead_parts(self) -> None:
        self._end_lead_parts = True

    def wrap_parts_append(self, node: Node) -> None:
        if self._end_lead_parts:
            self.trail_parts += node.start_tag()
        else:
            self.lead_parts += node.start_tag()

    def wrap_parts_append_content(self, content: str) -> None:
        if not self.lead_parts and re.fullmatch(r'\s*', content):
            return
        
        if self._end_lead_parts:
            self.trail_parts += content
        else:
            self.lead_parts += content

    def wrap_parts_append_close(self, node: Node) -> None:
        if self._end_lead_parts:
            self.trail_parts += node.end_tag()
        else:
            self.lead_parts += node.end_tag()

    def add_test_keys(self, props: dict[str, str]) -> None:
        for p in props:
            for m in re.finditer(r'\$\{([^}]+)\}', props[p]):
                self.test_keys.append(m.group(1))


@dataclass
class TokenTests:
    fullmatch: str = '.*'
    match: str = '.'
    ttype: _TokenType = field(init=False, default_factory=_TokenType)
    
@dataclass
class Token:
    lead_parts: str = ''
    trail_parts: str = ''
    test_keys: list = field(init=False, default_factory=list)
    tests: TokenTests = field(init=False, default_factory=TokenTests)
    _end_lead_parts: bool = field(init=False, default=False)

    def end_lead_parts(self) -> None:
        self._end_lead_parts = True

    def wrap_parts_append(self, node: Node) -> None:
        if self._end_lead_parts:
            self.trail_parts += node.start_tag()
        else:
            self.lead_parts += node.start_tag()

    def wrap_parts_append_content(self, content: str) -> None:
        if not self.lead_parts and re.fullmatch(r'\s*', content):
            return
        
        if self._end_lead_parts:
            self.trail_parts += content
        else:
            self.lead_parts += content

    def wrap_parts_append_close(self, node: Node) -> None:
        if self._end_lead_parts:
            self.trail_parts += node.end_tag()
        else:
            self.lead_parts += node.end_tag()

    def add_test_keys(self, props: dict[str, str]) -> None:
        for p in props:
            for m in re.finditer(r'\$\{([^}]+)\}', props[p]):
                self.test_keys.append(m.group(1))

    def add_token_tests(self, props) -> None:
        if 'fullmatch' in props:
            self.tests.fullmatch = props['fullmatch']
            if 'match' in props:
                raise TokenPropertyException('`fullmatch` and `match` are mutually exclusive.')
        elif 'match' in props:
            self.tests.match = props['match']

        if 'type' in props:
            self.tests.ttype = string_to_tokentype(props['type'])

    def run_tests(self, ttype: _TokenType, value: str) -> bool:
        return all([
            ttype in self.tests.ttype,
            re.fullmatch(self.tests.fullmatch, value),
            re.match(self.tests.match, value),
        ])


class TokenPropertyException(ValueError):
    pass


@dataclass
class TemplateContext:
    _lead_parts: list[tuple[int, str]] = field(init=False, default_factory=list)
    _trail_parts: list[tuple[int, str]] = field(init=False, default_factory=list)
    _pre_wrapped: bool = field(init=False, default=False)
    _end_lead_parts: bool = field(init=False, default=False)

    lines: list[Line] = field(init=False, default_factory=list)
    tokens: list[Token] = field(init=False, default_factory=list)
    
    @property
    def lead_parts(self) -> str:
        return self._wrap_parts(self._lead_parts)

    @property
    def trail_parts(self) -> str:
        parts = self._wrap_parts(self._trail_parts)
        if self._pre_wrapped:
            return parts + '\n'
        return parts

    _wrap_offset_wp = '  '
    def _wrap_parts(self, parts_src: list[tuple[int, str]]) -> str:
        parts = ''
        if self._pre_wrapped:
            for _, part in parts_src:
                parts += part
            return parts

        ws = self.__class__._wrap_offset_wp
        for lv, part in parts_src:
            parts += ws*lv + part + '\n'
        return parts

    def line_offset(self) -> str:
        if not self._pre_wrapped and self._lead_parts:
            lv, _ = self._lead_parts[-1]
            return self.__class__._wrap_offset_wp * (lv + 1)
        return ''

    def end_lead_parts(self) -> None:
        self._end_lead_parts = True

    def wrap_parts_append(self, node: Node, level: int) -> None:
        if self._end_lead_parts:
            self._trail_parts.append((level, node.start_tag()))
        else:
            if node.name == 'pre':
                self._pre_wrapped = True
            self._lead_parts.append((level, node.start_tag()))

    def wrap_parts_append_content(self, content: str) -> None:
        if re.fullmatch(r'\s*', content):
            return
        if self._end_lead_parts:
            if self._trail_parts:
                pair = self._trail_parts[-1]
                self._trail_parts[-1] = (pair[0], pair[1] + content)
        else:
            if self._lead_parts:
                pair = self._lead_parts[-1]
                self._lead_parts[-1] = (pair[0], pair[1] + content)

    def wrap_parts_append_close(self, node: Node, level: int) -> None:
        if not self._end_lead_parts and node.name == 'pre':
            self._pre_wrapped = False

        parts = self._trail_parts if self._end_lead_parts else self._lead_parts
        if not parts:
            parts.append((level, node.end_tag()))
        elif parts[-1][1].startswith('</'):
            parts.append((level, node.end_tag()))
        elif re.search(r'</[^>]+>$', parts[-1][1]):
            parts.append((level, node.end_tag()))
        else:
            pair = parts[-1]
            parts[-1] = (pair[0], pair[1] + node.end_tag())
        
    def new_line(self) -> None:
        self.lines.append(Line())

    @property
    def last_line(self) -> Line:
        return self.lines[-1]
    
    def new_token(self) -> None:
        self.tokens.append(Token())

    @property
    def last_token(self) -> Token:
        return self.tokens[-1]
    
