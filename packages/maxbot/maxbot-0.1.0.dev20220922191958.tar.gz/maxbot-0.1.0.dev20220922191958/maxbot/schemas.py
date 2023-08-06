import re

import marshmallow.exceptions
import yaml
from marshmallow import Schema, fields, post_load, pre_load

from .errors import BotError, YamlSnippet, YamlSymbols


class LoaderFactory(yaml.SafeLoader):
    @classmethod
    def new_loader(cls):
        return type("ConcreteLoader", (cls,), {})

    @classmethod
    def load(cls, data):
        try:
            # nosec note: actualy we derive a safe loader
            return yaml.load(data, Loader=cls)  # nosec B506
        except yaml.MarkedYAMLError as exc:
            raise YamlParsingError(exc)

    @classmethod
    def register_scenario_syntax(cls):
        def jinja_syntax(syntax):
            def constructor(loader, node):
                content = loader.construct_scalar(node)
                YamlSymbols.add(content, node)
                rv = {"content": content, "syntax": syntax}
                YamlSymbols.add(rv, node)
                return rv

            if syntax == "raw":
                # raw syntax is default
                cls.add_constructor("!jinja", constructor)
            cls.add_constructor(f"!jinja/{syntax}", constructor)

        jinja_syntax("raw")
        jinja_syntax("yaml")

    @classmethod
    def register_variable_substitution(cls, variables):
        variables = variables or {}
        VARIABLE = re.compile(r".*?\$\{([^}{:]+)(:([^}]+))?\}.*?")

        def substitute_variables(loader, node):
            string = loader.construct_scalar(node)
            for name, with_colon, default in VARIABLE.findall(string):
                if with_colon:
                    value = variables.get(name, default)
                else:
                    value = variables[name]
                string = string.replace(f"${{{name}{with_colon}}}", value, 1)
            return string

        cls.add_constructor("!ENV", substitute_variables)

    @classmethod
    def register_debug_watcher(cls):
        def watch_mapping(loader, node):
            rv = loader.construct_mapping(node)
            YamlSymbols.add(rv, node)
            return rv

        def watch_sequence(loader, node):
            rv = loader.construct_sequence(node)
            YamlSymbols.add(rv, node)
            return rv

        def watch_string(loader, node):
            rv = loader.construct_scalar(node)
            YamlSymbols.add(rv, node)
            return rv

        cls.add_constructor("tag:yaml.org,2002:map", watch_mapping)
        cls.add_constructor("tag:yaml.org,2002:seq", watch_sequence)
        cls.add_constructor("tag:yaml.org,2002:str", watch_string)


class YamlParsingError(BotError):
    def __init__(self, exc):
        lines = []
        if exc.context:
            lines.append(exc.context)
        if exc.context_mark:
            lines.append(YamlSnippet(exc.context_mark).at_mark())
        if exc.problem:
            lines.append(exc.problem)
        if exc.problem_mark:
            lines.append(YamlSnippet(exc.problem_mark).at_mark())
        if exc.note:
            lines.append(exc.note)
        super().__init__("\n".join(lines))


class RenderBase:
    def __init__(self):
        self.Loader = LoaderFactory.new_loader()
        self.Loader.register_debug_watcher()

    def loads(self, data):
        return self.Loader.load(data)


class RenderConfig:
    def loads(self, data, variables=None):
        Loader = LoaderFactory.new_loader()
        Loader.register_scenario_syntax()
        Loader.register_variable_substitution(variables)
        Loader.register_debug_watcher()
        return Loader.load(data)


class BaseSchema(Schema):
    class Meta:
        render_module = RenderBase()

    def handle_error(self, exc, data, **kwargs):
        """
        Raise only the first error with corresponding source data
        from marshmallow's normalized error messages

        Contains some workarounds for the correct output of the snippet.
        """

        def first_error(errors, source):
            field, messages = next(iter(errors.items()))
            if isinstance(messages, dict):
                # go deeper, an error occured in nested schema
                return first_error(messages, source[field])
            if isinstance(messages, list):
                # several messages for one field
                messages = "\n".join(messages)
            if field == marshmallow.exceptions.SCHEMA:
                # actualy not a field in schema but schema itself
                field = None
            if messages == fields.Field.default_error_messages["required"]:
                # add missing field name
                messages = f"Missing required field {field!r}."
            if messages == self.error_messages["unknown"]:
                # add missing field name
                messages = f"Unknown field {field!r}."
                # point to the field itself, not to its value
                source = field
                field = None
            # source = field
            return BotError(messages, YamlSnippet.format(source, key=field))

        raise first_error(exc.normalized_messages(), data) from exc


class ConfigSchema(BaseSchema):
    class Meta:
        render_module = RenderConfig()

    def load_file(self, path, **kwargs):
        with open(path) as f:
            return self.loads(f, **kwargs)

    @post_load(pass_original=True)
    def create(self, data, original_data, **kwargs):
        for name in self._declared_fields:
            if name in data and name in original_data:
                YamlSymbols.reference(data[name], original_data[name])
        YamlSymbols.reference(data, original_data)
        return data


class DialogSchema(ConfigSchema):
    channel_name = fields.String()
    user_id = fields.Integer()


class ImageMessage(Schema):
    url = fields.Url(required=True)
    size = fields.Integer(required=True)
    caption = fields.Str()


class MessageSchema(BaseSchema):
    text = fields.Str()
    image = fields.Nested(ImageMessage)

    @pre_load
    def short_syntax(self, data, **kwargs):
        """
        Short syntax for text message.

        You can write

            message: Hello world

        instead of

            message:
                text: Hello world

        Useful mostly for writing stories.
        """
        if isinstance(data, str):
            data = {"text": data}
        return data


class ImageCommand(Schema):
    url = fields.Url(required=True)
    caption = fields.Str()


class CommandSchema(BaseSchema):
    text = fields.Str()
    image = fields.Nested(ImageCommand)

    @pre_load(pass_many=True)
    def short_syntax_list(self, data, **kwargs):
        """
        Short syntax single text command instead of command list.

        You can write

            response: Hello world

        instead of

            response:
              - text: Hello world

        Widly used in scenarios and stories.
        """
        if isinstance(data, str):
            data = [{"text": data}]
        return data
