import inspect
import pkgutil
from abc import ABC, abstractmethod

from marshmallow import Schema, fields, pre_load

from ..errors import BotError, YamlSnippet
from ..schemas import ConfigSchema

BUILTIN_CHANNELS = {
    "telegram": "maxbot.channels.telegram:TelegramChannel",
}


def load_builtin_channel_mixins(builder):
    for name, import_spec in BUILTIN_CHANNELS.items():
        try:
            builder.add_channel_mixin(pkgutil.resolve_name(import_spec), name)
        except ImportError:
            pass


def make_channel_class(name, mixins):
    name = "".join(w.capitalize() or "_" for w in name.split("_"))
    return type(f"GeneratedChannel_{name}", tuple(reversed(mixins)) + (Channel,), {})


class ChannelsSchema(ConfigSchema):

    extra_required = "Extra dependencies are required to use the {name!r} channel. Try `pip install -U maxbot[{name}]`."

    @classmethod
    def from_classes(cls, channel_classes):
        return cls.from_dict(
            {
                n: fields.Nested(getattr(c, "ConfigSchema", Schema))
                for n, c in channel_classes.items()
            }
        )

    @pre_load
    def check_extra_required(self, data, **kwargs):
        for name in data:
            if name not in self._declared_fields and name in BUILTIN_CHANNELS:
                raise BotError(self.extra_required.format(name=name), YamlSnippet.format(name))
        return data


class Channel(ABC):
    """The channel is used by the bot to communicate with the user through various instant messengers and voice assistants.

        * The channel receives a message from the user in a messenger-specific format and converts it into a format
    understandable by the bot.
        * The channel receives bot commands and sends them in a messenger-specific format to the user.
        * The channel provides the bot with a user ID in the messenger and other useful information in the form of
    an instance of :class:`maxbot.context.ChannelInfo`.
        * The channel maintains a configuration object that can be used establish connection with the messenger.

    To implement your own channel, you should

        * create a subclass of :class:`maxbot.bot.BaseChannel`,
        * define channel :attr:`name` used in project to configure channel,
        * define a schema to channel config,
        * implement :meth:`create_context` factory for :class:`maxbot.context.ChannelInfo`,
        * implement messages receivers and commands senders.

    Each channel uses its own channel-specific set of arguments.
    These arguments are determined by the library and protocol used to interact with the messenger.
    Usually, they include an object that represents the received message, user information
    and an object that allows you to request additional information and send messages to the messenger.
    Channel-specific arguments are passed through calls of channel methods as keyword arguments that we call `chargs`.
    See :class:`maxbot.channels.TelegramChannel` for examples of using `chargs` to receive messages and send commands.

    For each `message` you need to add a receiver function that will receive message data from channel-specific arguments.
    For generic messages you can define receivers as methods of your channel class. The name of such method must
    consist of two parts: prefix `receive_` and the name of the message to be receided.
    See :meth:`maxbot.channels.TelegramChannel.receive_text` for example of receiving :class:`maxbot.schemas.TextMessage`.
    For custom messages you can add receivers by using method :meth:`maxbot.bot.BaseChannel.add_receiver` or
    :meth:`maxbot.bot.BaseChannel.receiver` decorator.

    Along with a `message` channel creates a context object :class:`maxbot.context.ChannelInfo` that contains common
    information and does not changes during conversation. This information must include channel name and user ID and may be extended
    depending on the channel needs.

    The channel creates `message` and `channel_context` from the user request. Maxbot processes them and returns a list of commands.
    The channel sends this commands back to the user.

    For each `command` you need to add a sender function that will send this command.
    Sender function takes a command object, channel context and channel specific arguments and sends passed command to te user.
    For generic commands you can define senders as methods of your channel class. The name of such method must
    consist of two parts: prefix `send_` and the name of the command to be sent.
    See :meth:`maxbot.channels.TelegramChannel.send_text` for example of sending :class:`maxbot.schemas.TextCommand`.
    For custom commands you can add senders by using method :meth:`maxbot.bot.BaseChannel.add_sender` or
    :meth:`maxbot.bot.BaseChannel.sender` decorator.
    """

    def __init__(self, bot, config):
        self._bot = bot
        self.config = config
        self._receive_hooks = dict(self._get_member_hooks("receive_"))
        self._send_hooks = dict(self._get_member_hooks("send_"))

    def _get_member_hooks(self, prefix):
        prefix_len = len(prefix)
        for name, hook in inspect.getmembers(self, inspect.ismethod):
            if name.startswith(prefix):
                yield name[prefix_len:], _HookWrapper(hook)

    @abstractmethod
    def create_dialog(self, **chargs):
        pass

    @abstractmethod
    def receive_text(self, **chargs):
        pass

    @abstractmethod
    def send_text(self, command: dict, channel: dict, **chargs):
        pass

    def call_receivers(self, **chargs):
        """Called to transform channel-specific arguments to bot message . Calls receive hooks in
        sequence until one of them returns a message.

        See :class:`~maxbot.schemas.MessageSchema` for more information about bot messages.

        :param dict chargs: channel-specific arguments
        """
        for name, hook in self._receive_hooks.items():
            message = hook(**chargs)
            if message is not None:
                return message

    def call_senders(self, command, context, **chargs):
        """Called to send command to the user. The hook corresponding to the command name is used.

        See :class:`~maxbot.schemas.CommandSchema` for more information about commands.

        :param dict command: a command to be sent
        :param ChannelInfo context: contains information about the user to whom we send the command
        :param dict chargs: channel-specific arguments useful to pass some messenger connection information
        """
        for name, hook in self._send_hooks.items():
            if name in command:
                hook(command, context, **chargs)
                break
        else:
            raise ValueError(f"Could not execute command {command!r}")

    def simple_adapter(self, **chargs):
        message = self.call_receivers(**chargs)
        if message is None:
            return
        dialog = self.create_dialog(**chargs)
        for command in self._bot.process_message(message, dialog):
            self.call_senders(command, dialog, **chargs)


class _HookWrapper:
    """Utility wrapper that passes only those keyword arguments to the wrapped function that it declares.

    :param: callable f: a function to be wrapped
    """

    def __init__(self, f):
        self.f = f
        self.parameters = inspect.signature(f).parameters

    def __call__(self, *args, **kwargs):
        kwargs = {k: kwargs[k] for k in kwargs if k in self.parameters}
        return self.f(*args, **kwargs)
