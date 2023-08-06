import jinja2
from jinja2.ext import Extension
from jinja2.nodes import Assign, Call, ContextReference, Getattr, Keyword, Name


def create_jinja_env(options=None):
    options = dict(options) if options else {}
    # nosec note: autoescape is not actual when rendering yaml
    options.setdefault("autoescape", False)
    options.setdefault("extensions", []).append(VariablesExtension)
    env = jinja2.Environment(**options)  # nosec: B701
    return env


class VariablesExtension(Extension):

    tags = {"slot", "user"}

    def parse(self, parser):
        var = parser.stream.current.value
        lineno = next(parser.stream).lineno

        name = parser.stream.expect("name").value
        parser.stream.expect("assign")
        value = parser.parse_expression()

        # transform our custom statements into dict updates
        # {% user name = 'Bob' %}
        #   -> {% set _ = user.update({'name': 'Bob'}) %}
        # {% slot guests = entities.number %}
        #   -> {% set _ = slots.update({'guests': entities.number}) %}
        if var == "slot":
            var = "slots"
        method = Getattr(Name(var, "load"), "update", ContextReference())
        call = Call(method, [], [Keyword(name, value)], None, None)
        dummy = Name("_", "store")
        return Assign(dummy, call).set_lineno(lineno)
