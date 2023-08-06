from dataclasses import dataclass, field
from typing import Callable

import jinja2
from marshmallow import ValidationError, fields, validate

from .errors import BotError, YamlSnippet, YamlSymbols
from .jinja_env import create_jinja_env
from .schemas import CommandSchema, ConfigSchema

DEFAULT_JINJA_ENV = create_jinja_env()

JINJA_ERRORS = (
    TypeError,
    ValueError,
    LookupError,
    ArithmeticError,
    AttributeError,
    jinja2.TemplateError,
)


class ExpressionField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (str, bool, int, float)):
            return Expression(value, self.context.get("jinja_env", DEFAULT_JINJA_ENV))
        raise ValidationError("Invalid expression. Must be one of: str, bool, number")


class TemplateSchema(ConfigSchema):
    content = fields.Str(required=True)
    syntax = fields.Str(required=True, validate=validate.OneOf(["raw", "yaml"]))


class ScenarioField(fields.Field):
    def __init__(self, controls_schema, many=False, **kwargs):
        super().__init__(**kwargs)
        self.controls_schema = controls_schema

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        Schema = _union_commands(self.context.get("schema", CommandSchema), self.controls_schema)
        if isinstance(value, dict):
            template = TemplateSchema().load(value)
            return Template(
                template["syntax"],
                template["content"],
                Schema,
                self.context.get("jinja_env", DEFAULT_JINJA_ENV),
            )
        else:
            return Commands(Schema(many=True).load(value, partial=partial))


def _union_commands(Commands, Controls):
    return type("Union" + Controls.__name__, (Controls, Commands), {})


@dataclass
class Expression:

    source: str
    jinja_env: jinja2.Environment = field(default=DEFAULT_JINJA_ENV)

    expr: Callable = field(init=False)

    def __post_init__(self):
        try:
            self.expr = self.jinja_env.compile_expression(self.source)
        except jinja2.TemplateSyntaxError as exc:
            raise BotError(exc.message, YamlSnippet.format(self.source, line=exc.lineno))

    def __call__(self, ctx, **params):
        try:
            return self.expr(ctx.create_scenario_context(params))
        except JINJA_ERRORS as exc:
            # jinja always treats expressions as on line
            raise BotError(str(exc), YamlSnippet.format(self.source, line=1))


@dataclass
class Template:

    syntax: str
    content: str
    Schema: type = field(default=CommandSchema)
    jinja_env: jinja2.Environment = field(default=DEFAULT_JINJA_ENV)

    tpl: Callable = field(init=False)

    def __post_init__(self):
        try:
            self.tpl = self.jinja_env.from_string(self.content)
        except jinja2.TemplateSyntaxError as exc:
            raise BotError(exc.message, YamlSnippet.format(self.content, line=exc.lineno))

    def __call__(self, ctx, **params):
        try:
            document = self.tpl.render(ctx.create_scenario_context(params))
        except jinja2.TemplateSyntaxError as exc:
            raise BotError(exc.message, YamlSnippet.format(self.content, line=exc.lineno))
        except JINJA_ERRORS as exc:
            raise BotError(str(exc), YamlSnippet.format(self.content, line=_extract_lineno(exc)))

        if isinstance(document, str) and document.strip():
            try:
                return self._create_commands(document)
            except BotError as exc:
                # wrap original error to include template snippet
                raise BotError(str(exc), YamlSnippet.format(self.content, line=1))
            finally:
                # cleanup globally stored data to avoid memory leaks
                YamlSymbols.cleanup(document)
        else:
            return []

    def _create_commands(self, document):
        schema = self.Schema(many=True)
        if self.syntax == "raw":
            return schema.load(document)
        elif self.syntax == "yaml":
            return schema.loads(document)
        else:
            raise ValueError(f"Unknown content syntax {self.syntax!r}")


@dataclass
class Commands:

    commands: list

    def __call__(self, ctx, **params):
        return self.commands


def _extract_lineno(exc):
    """
    Extract line where template error is occured
    assuming that traceback was rewritten by jinja
    @see jinja2.debug.rewrite_traceback_stack
    """
    tb = exc.__traceback__
    lineno = None
    while tb:
        if tb.tb_frame.f_code.co_filename == "<template>":
            lineno = tb.tb_lineno
        tb = tb.tb_next
    return lineno
