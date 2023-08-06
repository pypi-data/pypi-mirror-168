import pathlib
from textwrap import dedent, indent

import yaml


class BotError(RuntimeError):
    def __init__(self, message, snippet=None):
        self.message = message
        self.snippet = snippet
        super().__init__(message)

    def __str__(self):
        message = self.message
        cause = self.__cause__ or self.__context__
        if cause is not None and not isinstance(cause, self.__class__):
            klass = cause.__class__
            message = f"caused by {klass.__module__}.{klass.__qualname__}: {message}"
        if self.snippet is not None:
            message = f"{message}\n{self.snippet}"
        return message


class YamlSymbols:
    """
    Track yaml nodes for debugging purpose
    """

    _stores = {}

    @classmethod
    def cleanup(cls, document):
        cls._stores.pop(document, None)

    @classmethod
    def add(cls, source, node):
        if isinstance(source, (int, float, bool)):
            return
        if node.start_mark.buffer is not None:
            key = node.start_mark.buffer.rstrip("\0")
        else:
            key = node.start_mark.name
        store = cls._stores.setdefault(key, {})
        store[id(source)] = node

    @classmethod
    def lookup(cls, source):
        id_ = id(source)
        for store in cls._stores.values():
            if id_ in store:
                return store[id_]
        return None

    @classmethod
    def reference(cls, source, original):
        node = cls.lookup(original)
        if node:
            cls.add(source, node)


class YamlSnippet:
    """
    Format snippets from yaml mark with pointer to specific line and column
    """

    @staticmethod
    def format(source, *, key=None, line=None):
        node = YamlSymbols.lookup(source)
        if node is not None:
            if key is not None:
                node = YamlSnippet._node_get(node, key)
            ys = YamlSnippet(node.start_mark)
            if line is not None:
                return ys.with_offset(line - 1, node.style)
            else:
                return ys.at_mark()
        return None

    @staticmethod
    def _node_get(node, key):
        if isinstance(node, yaml.MappingNode):
            mapping = dict((k.value, v) for k, v in node.value)
            return mapping.get(key, node)
        if isinstance(node, yaml.SequenceNode):
            return node.value[key]
        return node

    max_lines = 1
    max_chars = 80

    def __init__(self, mark):
        if mark.buffer is not None:
            source_code = mark.buffer.rstrip("\0")
        else:
            source_code = pathlib.Path(mark.name).read_text()

        self.lines = source_code.splitlines()
        self.mark = mark

    def at_mark(self):
        name, line, column = self.mark.name, self.mark.line, self.mark.column
        snippet = self._format(line, column)
        return f'  in "{name}", line {line + 1}, column {column + 1}:\n{snippet}'

    def with_offset(self, offset, style):
        """
        When mark points to the multiline scalar
        we take into account a specific line offset inside it
        """
        mark = self.mark
        line = mark.line + offset
        if style in (None, "'", '"'):
            column = mark.column
        else:
            s = self.lines[line]
            column = len(s) - len(s.lstrip(" "))
        snippet = self._format(line, column)
        return f'  in "{mark.name}", line {line + 1}:\n{snippet}'

    def _format(self, line, column):
        start_line = max(line - self.max_lines, 0)
        end_line = min(line + self.max_lines + 1, len(self.lines))
        if start_line == end_line:
            end_line += 1

        head = "\n".join(self.lines[start_line:line])
        if len(head) > self.max_chars:
            head = "..." + head[-self.max_chars :]  # noqa: E203

        tail = "\n".join(self.lines[line + 1 : end_line])  # noqa: E203
        if len(tail) > self.max_chars:
            tail = tail[: self.max_chars] + "..."

        pointer = " " * column + "^^^"
        snippet = "\n".join([head, self.lines[line], pointer, tail])
        snippet = indent(dedent(snippet), "    ")
        return snippet
