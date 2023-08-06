import importlib.resources
import logging
from functools import cached_property, partial
from pathlib import Path

from marshmallow import fields

logger = logging.getLogger(__name__)

from .channels import ChannelsSchema, load_builtin_channel_mixins, make_channel_class
from .context import TurnContext
from .extensions import ExtensionsSchema, get_entry_point_extensions
from .flows._base import FlowComponent, FlowResult
from .flows.dialog_tree import DialogTree, NodeSchema
from .jinja_env import create_jinja_env
from .nlu import EntitySchema, IntentSchema, Nlu
from .schemas import CommandSchema, ConfigSchema, DialogSchema, MessageSchema
from .state_tracker import SQLAlchemyStateTracker


class BotConfigSchema(ConfigSchema):

    extensions = fields.Raw()
    channels = fields.Raw()
    intents = fields.Raw()
    entities = fields.Raw()
    dialog = fields.Raw()


class _RawResources:
    def __init__(self, raw):
        self.raw = raw

    def load_extensions(self, schema):
        return schema.load(self.raw.get("extensions", {}))

    def load_channels(self, schema):
        return schema.load(self.raw.get("channels", {}))

    def load_intents(self, schema):
        return schema.load(self.raw.get("intents", []))

    def load_entities(self, schema):
        return schema.load(self.raw.get("entities", []))

    def load_dialog(self, schema):
        return schema.load(self.raw.get("dialog", []))


class InlineResources(_RawResources):
    def __init__(self, source):
        super().__init__(BotConfigSchema().loads(source))


class FileResources(_RawResources):
    def __init__(self, path):
        super().__init__(BotConfigSchema().load_file(path))


class DirectoryResources:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.botconfig = FileResources(self.base_dir / "bot.yaml")

    def load_extensions(self, schema):
        return self.botconfig.load_extensions(schema)

    def load_channels(self, schema):
        return self.botconfig.load_channels(schema)

    def load_intents(self, schema):
        intents = self.botconfig.load_intents(schema)
        path = self.base_dir / "intents.yaml"
        if path.exists():
            intents.extend(schema.load_file(path))
        dir_path = self.base_dir / "intents"
        for path in dir_path.glob("*.yaml"):
            intents.extend(schema.load_file(path))
        return intents

    def load_entities(self, schema):
        entities = self.botconfig.load_entities(schema)
        path = self.base_dir / "entities.yaml"
        if path.exists():
            entities.extend(schema.load_file(path))
        dir_path = self.base_dir / "entities"
        for path in dir_path.glob("*.yaml"):
            entities.extend(schema.load_file(path))
        return entities

    def load_dialog(self, schema):
        dialog = self.botconfig.load_dialog(schema)
        path = self.base_dir / "dialog.yaml"
        if path.exists():
            dialog.extend(schema.load_file(path))
        return dialog


class PackageResources(DirectoryResources):
    def __init__(self, import_name):
        super().__init__(importlib.resources.files(import_name))


class BotBuilder:
    """The maxbot acts as a central object of application. Once it is created it will act as a registry for the
    messages, commands, channels, nlu, conversation flow and template configuration.

    The maxbot object implements a simple message handling protocol. It receives a user's message from the channel,
    processes it, and sends a list of commands to the channel as a response to the user.

    While processing a message bot uses

        * :attr:`nlu` component to recognize intent and entities from user's utterance,
        * :attr:`state_tracker` to maintain necessary dialog state variables,
        * :attr:`dialog` manager to execute the flow, render templates and get a list of resulting commands.

    Basic example:

        bot = MaxBot().load_inline_project("...")
        telegram_adapter = bot.create_adapter(TelegramChannel)
        telegram_adapter(update=update, bot=bot)

    Bot customization example:

        bot = MaxBot()
        bot.state_tracker.engine = sqlalchemy.create_engine(...)
        bot.add_command(CustomCommand, 'custom')
        bot.add_template_filter(custom_filter)
        bot = MaxBot().load_inline_project("...")
        telegram_adapter = bot.create_adapter(TelegramChannel)
        telegram_adapter(update=update, bot=bot)

    Extensions are a convenient way to customize bot. They allows reuse and groupin of custom logic.
    An extension is a callable the accepts an instance of the bot and a configuration dictionary and performs customization.
    An example of the extension that customizes sqlalchemy engine for state tracker.

            def SqlAlchemyExtension(bot, config):
                bot.state_tracker.engine = sqlalchemy.engine_from_config(config, prefix="")

    Now you can simply call the extension after creating the bot.

            bot = MaxBot()
            SqlAlchemyExtension(bot, config={"url": "sqlite:///./somedb.db"})

    Or your can configure the extension from the project data in the following way

        bot = MaxBot(
            available_extensions={'sqlalchemy': SqlAlchemyExtension}
        )
        bot.load_inline_project('''
            extensions:
                sqlalchemy:
                    url: "sqlite:///./somedb.db"
            dialog: []
        ''')

    Finally, you can create the python package and add the extension to the entry points group called "maxbot_extensions".
    For example, by using setup.cfg

        [options.entry_points]
        maxbot_extensions =
            sqlalchemy = my_module:SqlAlchemyExtension

    In this way after installing the extension package

        pip install maxbot-extensions-sqlalchemy

    bot can automaticaly discover and load the extension

        bot = MaxBot()
        bot.load_inline_project('''
            extensions:
                sqlalchemy:
                    url: "sqlite:///./somedb.db"
            dialog: []
        ''')
    """

    # Options that are passed to the Jinja environment in :attr:`jinja_env`. Changing these options after the environment
    # is created (accessing :attr:`jinja_env`) will have no effect.
    jinja_options = {}

    def __init__(self, *, available_extensions={}):
        self._extensions = {**available_extensions, **get_entry_point_extensions()}
        self._bot_created = False
        self._resources = _RawResources({})
        self._state_tracker = None
        self._nlu = None
        self._message_schemas = {}
        self._command_schemas = {}
        self._before_turn_hooks = []
        self._after_turn_hooks = []
        self._channel_mixins = {}

        load_builtin_channel_mixins(self)

    def add_message(self, schema, name):
        """Register a custom message. Example:

            class LocationMessage(Schema):
                longitude = fields.Float()
                latitude = fields.Float()

            bot.add_message(LocationMessage, 'location')

        :param type schema: a subclass of :class:`~marshmallow.Schema` schema
        :param str name: the name of the message
        """
        self._message_schemas[name] = schema
        return schema

    def message(self, name):
        """A decorator that is used to register custom message. Example:

            @bot.message('location')
            class LocationMessage(Schema):
                longitude = fields.Float()
                latitude = fields.Float()

        :param str name: the name of the message
        """
        return partial(self.add_message, name=name)

    def add_command(self, schema, name):
        """Register a custom command. Example:

            class PollCommand(Schema):
                question = fields.String()
                options = fields.List(fields.String)

            bot.add_message(PollCommand, 'poll')

        :param type schema: a subclass of :class:`~marshmallow.Schema` schema
        :param str name: the name of the command
        """
        self._command_schemas[name] = schema
        return schema

    def command(self, name):
        """A decorator that is used to register custom command. Example:

            @bot.command('poll')
            class PollCommand(Schema):
                question = fields.String()
                options = fields.List(fields.String)

        :param str name: the name of the command
        """
        return partial(self.add_command, name=name)

    @property
    def state_tracker(self):
        """The state tracker used to maintain state variables.
        See default implementation :class:`~maxbot.state_tracker.SQLAlchemyStateTracker` for more information.
        You can use this property to configure default state tracker:

            bot.state_tracker.engine = sqlalchemy.create_engine(...)

        or set your own implementation:

            class CustomStateTracker:
                @contextmanager
                def __call__(self, channel_info):
                    # load variables...
                    yield StateVariables(...)
                    # save variables...

            bot.state_tracker = CustomStateTracker()
        """
        if self._state_tracker is None:
            self._state_tracker = SQLAlchemyStateTracker()
        return self._state_tracker

    @state_tracker.setter
    def state_tracker(self, value):
        self._state_tracker = value

    @property
    def nlu(self):
        """The nlu component used to recognize intent and entities from user's utterance.
        See default implementation :class:`~maxbot.nlu.NLU` for more information.
        You can use this property to configure nlu component:

            bot.nlu.threshold = 0.6

        or set your own implementation:

            class CustomNlu:
                def load(self, intents, entities):
                    ...

                def __call__(self, message):
                    ...
                    return NluResult(...)

            bot.nlu = CustomNlu()
        """
        if self._nlu is None:
            self._nlu = Nlu()
        return self._nlu

    @nlu.setter
    def nlu(self, nlu):
        self._nlu = nlu

    def before_turn(self, f):
        """Register a function to run before each dialog turn.

        The function is called with one argument
            :param TurnContext ctx: information about the current turn

        For example, this can be used to provide custom user profile to scenario context.

            @bot.before_turn
            def load_profile(ctx):
                resp = requests.get('http://example.com/profile/' + ctx.dialog.user_id)
                ctx.extend_scenario_context(profile=resp.json())
        """
        self._before_turn_hooks.append(f)
        return f

    def after_turn(self, f):
        """Register a function to run after each dialog turn.

        The function is called with two arguments
            :param TurnContext ctx: information about the current turn
            :param bool listening: whether the bot is waiting for the user's response

        For example, this can be used to journal all the conversation messages

            @bot.after_turn
            def journal_conversation(ctx):
                requests.post('http://example.com/journal/, json_data={
                    'user_id': ctx.dialog.user_id,
                    'message': ctx.message,
                    'commands': ctx.commands,
                })
        """
        self._after_turn_hooks.append(f)
        return f

    @cached_property
    def jinja_env(self):
        """The Jinja environment used to render templates. You can use this property to configure the environment:

            bot.jinja_env.add_extension(MyJinjaExtension)

        Also you can use convenient bot methods to add filters, tests and globals to the environment.
        The environment is created the first time this property is accessed. Changing :attr:`jinja_options` after that
        will have no effect.
        """
        return create_jinja_env(self.jinja_options)

    def add_template_filter(self, f, name=None):
        """Register a custom jinja template filter.

        Example:

            bot.add_template_filter(lambda s: s[::-1], 'reverse')

        :param callable f: the filter function.
        :param str name: the optional name of the filter, otherwise the function name will be used.
        """
        self.jinja_env.filters[name or f.__name__] = f
        return f

    def template_filter(self, name=None):
        """A decorator that is used to register a custom jinja template filter. Example:

            @bot.template_filter()
            def reverse(s):
                return s[::-1]

        :param str name: the optional name of the filter, otherwise the function name will be used.
        """
        return partial(self.add_template_filter, name=name)

    def add_template_test(self, f, name=None):
        """Register a custom jinja template test. Example:

            def greeting(s):
                return any(h in s for h in ["hello", "hey"])

            bot.add_template_test(greeting)

        :param callable f: the test function.
        :param str name: the optional name of the test, otherwise the function name will be used.
        """
        self.jinja_env.tests[name or f.__name__] = f
        return f

    def template_test(self, name=None):
        """A decorator that is used to register a custom jinja template test. Example:

            @bot.template_test()
            def greeting(s):
                return any(h in s for h in ["hello", "hey"])

        :param str name: the optional name of the test, otherwise the function name will be used.
        """
        return partial(self.add_template_test, name=name)

    def add_template_global(self, f, name=None):
        """Register a custom function in the jinja template global namespace. Example

            def say_hello(name):
                return f"Hello, {name}!"

            bot.add_template_global(say_hello, 'hello')

        :param callable f: the function to be registered.
        :param str name: the optional name in the global namespace, otherwise the function name will be used.
        """
        self.jinja_env.globals[name or f.__name__] = f
        return f

    def template_global(self, name=None):
        """A decorator that is used to register a custom function in the jinja template global namespace. Example:

            @bot.template_global('hello')
            def say_hello(name):
                return f"Hello, {name}!"

        :param str name: the optional name in the global namespace, otherwise the function name will be used.
        """
        return partial(self.add_template_global, name=name)

    def add_channel_mixin(self, mixin, name):
        self._channel_mixins.setdefault(name, []).append(mixin)

    def channel_mixin(self, name):
        return partial(self.add_channel_mixin, name=name)

    def use_file_resources(self, bot_file):
        """Load resources from file.

        :param str|Path bot_file
        """
        self.use_resources(FileResources(bot_file))

    def use_directory_resources(self, bot_dir):
        """Load resources from directory.

        :param str|Path bot_dir
        """
        self.use_resources(DirectoryResources(bot_dir))

    def use_inline_resources(self, source):
        """Load resources from yaml string.

        :param str source: yaml string
        """
        self.use_resources(InlineResources(source))

    def use_package_resources(self, import_name):
        """Load resources from package directory.

        :param str import_name: the name of the package or nested module
        """
        self.use_resources(PackageResources(import_name))

    def use_resources(self, resources):
        self._resources = resources

    def build(self):
        """Load a collection of all the data and code necessary to build a conversational bot.

        :param Resources resources
        """
        if self._bot_created:
            raise RuntimeError("Bot already created")
        self._bot_created = True

        # extensions
        Schema = ExtensionsSchema.from_classes(self._extensions)
        extensions = self._resources.load_extensions(Schema())
        for name, config in extensions.items():
            extension = self._extensions[name]
            extension(self, config)

        message_schema = MessageSchema.from_dict(
            {n: fields.Nested(s) for n, s in self._message_schemas.items()}
        )

        command_schema = CommandSchema.from_dict(
            {n: fields.Nested(s) for n, s in self._command_schemas.items()}
        )

        # nlu
        self.nlu.load(
            self._resources.load_intents(IntentSchema(many=True)),
            self._resources.load_entities(EntitySchema(many=True)),
        )

        # dialog
        schema = NodeSchema(
            many=True,
            context={
                "schema": command_schema,
                "jinja_env": self.jinja_env,
            },
        )
        dialog = FlowComponent("ROOT", DialogTree(self._resources.load_dialog(schema)))

        bot = MaxBot(
            self.nlu,
            dialog,
            self.state_tracker,
            message_schema,
            command_schema,
            self._before_turn_hooks,
            self._after_turn_hooks,
        )
        self._build_channels(bot)
        return bot

    def _build_channels(self, bot):
        channel_classes = {
            name: make_channel_class(name, mixins) for name, mixins in self._channel_mixins.items()
        }
        Schema = ChannelsSchema.from_classes(channel_classes)
        configs = self._resources.load_channels(Schema())
        for name, config in configs.items():
            channel = channel_classes[name](bot, config)
            bot._channels[name] = channel


class MaxBot:
    def __init__(
        self, nlu, dialog, state_tracker, message_schema, command_schema, before_turn, after_turn
    ):
        self._nlu = nlu
        self._dialog = dialog
        self._state_tracker = state_tracker
        self.MessageSchema = message_schema
        self.CommandSchema = command_schema
        self._before_turn_hooks = before_turn
        self._after_turn_hooks = after_turn
        self._channels = dict()

    @classmethod
    def builder(cls, **kwargs):
        return BotBuilder(**kwargs)

    @classmethod
    def inline(cls, source, **kwargs):
        builder = cls.builder(**kwargs)
        builder.use_inline_resources(source)
        return builder.build()

    @classmethod
    def from_file(cls, bot_file, **kwargs):
        builder = cls.builder(**kwargs)
        builder.use_file_resources(bot_file)
        return builder.build()

    @classmethod
    def from_directory(cls, bot_dir, **kwargs):
        builder = cls.builder(**kwargs)
        builder.use_directory_resources(bot_dir)
        return builder.build()

    def process_message(self, message, dialog):
        """Handles a message received from a user through a channel.
        For simple applications you should not use this method directly.

        :param dict message: a message received from the dialog
        :param dict dialog: information about the dialog from which the message was received
        :return List[dict]: a list of commands to respond to the user.
        """

        logger.debug(f"dialog {message}, {dialog}")
        dialog = DialogSchema().load(dialog)
        message = self.MessageSchema().load(message)
        intents, entities = self._nlu(message)
        with self._state_tracker(dialog) as state:
            ctx = TurnContext(message, dialog, intents, entities, state)
            for func in self._before_turn_hooks:
                func(ctx)
            result = self._dialog(ctx)
            if result == FlowResult.DONE:
                ctx.state.slots.clear()
            for func in self._after_turn_hooks:
                func(ctx, listening=result == FlowResult.LISTEN)
        return ctx.commands

    def get_channel(self, name):
        if name in self._channels:
            return self._channels[name]
        else:
            raise ValueError(f"Unknown channel {name!r}")

    def __getattr__(self, name):
        try:
            return self.get_channel(name)
        except ValueError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute {name!r}")
