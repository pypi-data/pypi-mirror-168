import pathlib, enum, re
import xml.sax as SAX
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl

from pygmentshtmltemplate.templates.nodes import Line, Token, Node, TemplateContext, TokenPropertyException


def parse(src: pathlib.Path) -> TemplateContext:
    parser = SAX.make_parser()
    context = TemplateContext()
    handler = TemplateHandler(context)
    parser.setContentHandler(handler)
    parser.parse(src)
    return context


class Status(enum.Enum):
    INIT = ''
    WRAP = 'Pygmentshtmltemplate'
    LINE = 'Line'
    TOKENS = 'Tokens'
    TOKEN = 'Token'

    def __init__(self, container_name) -> None:
        self.container_name = container_name
        self.nodes: list[Node] = []
        self.path: list[str] = ['INIT']

    def popnode(self) -> Node:
        return self.nodes.pop()

    @property
    def parent(self) -> 'Status':
        return Status[self.path[-2]]

    def clear_path(self) -> None:
        self.path = ['INIT']


class TemplateHandler(ContentHandler):
    def __init__(self, context: TemplateContext) -> None:
        self.context = context
        self.status = Status.INIT

    def descend_status(self, status: Status) -> None:
        status.path = self.status.path[:] + [status.name]
        self.status = status

    def ascend_status(self) -> None:
        parent = self.status.parent
        self.status.clear_path()
        self.status = parent

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        if self.status is Status.INIT:
            if name == Status.WRAP.container_name:
                self.descend_status(Status.WRAP)
                return
            raise ParseException(f'A root must be `{Status.WRAP.container_name}`, but got `${name}`.')
        
        elif self.status is Status.WRAP:
            if name == Status.LINE.container_name:
                self.descend_status(Status.LINE)
                self.context.end_lead_parts()
                return
            elif name == Status.TOKENS.container_name:
                self.descend_status(Status.TOKENS)
                return
            elif name == Status.TOKEN.container_name:
                raise ParseException(f'`{name}` must be a decendant of `{Status.LINE.container_name}`.')

            node = Node(name, {k:v for k,v in attrs.items()})
            self.context.wrap_parts_append(node, len(self.status.nodes))
                
        elif self.status is Status.LINE:
            if not self.status.nodes:
                self.context.new_line()

            if name == Status.TOKENS.container_name:
                self.descend_status(Status.TOKENS)
                self.context.last_line.end_lead_parts()
                return
            elif name == Status.TOKEN.container_name:
                raise ParseException(f'`{name}` must be a decendant of `{Status.TOKENS.container_name}`.')
            
            attr_d = {k:v for k,v in attrs.items()}
            self.context.last_line.add_test_keys(attr_d)

            node = Node(name, attr_d)
            self.context.last_line.wrap_parts_append(node)

        elif self.status is Status.TOKENS:
            if not self.status.nodes:
                self.context.new_token()

            attr_d = {k:v for k,v in attrs.items()}
            if name == Status.TOKEN.container_name:
                try:
                    self.context.last_token.add_token_tests(attr_d)
                except TokenPropertyException as e:
                    raise ParseException(str(e))

                self.descend_status(Status.TOKEN)
                self.context.last_token.end_lead_parts()
                return

            self.context.last_token.add_test_keys(attr_d)
            node = Node(name, attr_d)
            self.context.last_token.wrap_parts_append(node)

        self.status.nodes.append(node)

    def characters(self, content: str) -> None:
        if self.status is Status.WRAP and self.status.nodes:
            self.context.wrap_parts_append_content(content)

        elif self.status is Status.LINE and self.status.nodes:
            self.context.last_line.wrap_parts_append_content(content)

        elif self.status is Status.TOKENS and self.status.nodes:
            self.context.last_token.wrap_parts_append_content(content)

    def endElement(self, name: str) -> None:
        if name[0].isupper():
            if name != self.status.container_name:
                raise ParseException(f'Mismatched end-tag `{name}`')
            self.ascend_status()
        else:
            node = self.status.popnode()
            if self.status is Status.WRAP:
                self.context.wrap_parts_append_close(node, len(self.status.nodes))

            elif self.status is Status.LINE:
                self.context.last_line.wrap_parts_append_close(node)

            elif self.status is Status.TOKENS:
                self.context.last_token.wrap_parts_append_close(node)


class ParseException(ValueError):
    pass
